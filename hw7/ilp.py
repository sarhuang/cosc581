import sys
import networkx as nx
import gurobipy as gp
from gurobipy import GRB
import time


def read_dimacs_graph(file_path):
    G = nx.Graph()
    with open(file_path, 'r') as f:
        for line in f:
            line = line.strip()                
            parts = line.split()

            if parts[0] == 'c':
                continue

            elif parts[0] == 'p':
                if len(parts) < 4 or parts[1].lower() != 'edge':
                    raise ValueError(f"Invalid problem line: {line}")
                n_vertices = int(parts[2])
                G.add_nodes_from(range(1, n_vertices + 1))
           
            elif parts[0] == 'e':
                if len(parts) >= 3:
                    v1 = int(parts[1])
                    v2 = int(parts[2])
                    G.add_edge(v1, v2)
                else:
                    raise ValueError(f"Invalid edge line: {line}")
    return G



def max_clique_ilp(G):
    curr_max_clique = greedy_clique(G)
    curr_clique_size = len(curr_max_clique)
    other_max_cliques = []

    vertices = sorted(G.nodes(), key=lambda v: G.degree[v], reverse=True)
    #Try different starting vertices
    for i in range(0, len(vertices), 100):
        start_vertices = vertices[i:i+10]
        
        for v in start_vertices:
            #Create a subgraph of vertex and neighbors
            neighbors = set(G.neighbors(v))
            subgraph_nodes = neighbors.union({v})
            subgraph = G.subgraph(subgraph_nodes).copy()
            
            #Break down problem (good for 1000 vertice graph)
            model = gp.Model("MaxCliqueSubproblem")
            model.setParam('OutputFlag', 0)
            model.setParam("MIPFocus", 1)
            model.setParam("Heuristics", 0.5)
            model.setParam("MIPGap", 0.0)
            model.setParam("Threads", 8)
            
            
            x = {}
            for v in subgraph.nodes():
                x[v] = model.addVar(vtype=GRB.BINARY, name=f"x_{v}")
            
            model.setObjective(gp.quicksum(x[v] for v in subgraph.nodes()), GRB.MAXIMIZE)
            for u in subgraph.nodes():
                for v in subgraph.nodes():
                    if u < v and not subgraph.has_edge(u, v):
                        model.addConstr(x[u] + x[v] <= 1)
            
            model.addConstr(x[v] == 1)
            model.optimize()
            
            if model.status in [GRB.OPTIMAL, GRB.SUBOPTIMAL, GRB.INTERRUPTED]:
                clique = [v for v in subgraph.nodes() if x[v].X > 0.5]
                if len(clique) == curr_clique_size:
                    other_max_cliques.append(clique)
                
                elif len(clique) > curr_clique_size:
                    #Make sure it's a clique
                    if all(subgraph.has_edge(u, v) for u in clique for v in clique if u != v):
                        curr_max_clique = clique
                        curr_clique_size = len(clique)
                        other_max_cliques = []
    
    if other_max_cliques:
        if curr_max_clique in other_max_cliques:
            return curr_max_clique
        else:
            return other_max_cliques[0]
        
    return curr_max_clique

    
#Find a starting clique so ILP doesn't completely start from scratch
def greedy_clique(G):
    good_clique = []
    for node in G.nodes():
        clique = [node]
        potentials = set(G.neighbors(node))
        
        while potentials:
            valid = [n for n in potentials if all(G.has_edge(n, v) for v in clique)]
            if not valid:
                break
                
            next_node = max(valid, key=lambda n: G.degree[n])
            clique.append(next_node)
            potentials = potentials.intersection(G.neighbors(next_node)) - {next_node}
        
        if len(clique) > len(good_clique):
            good_clique = clique

    clique = max(list(nx.find_cliques(G)), key=len)
    if set(good_clique) != set(clique):
        good_clique = clique
    
    return good_clique




def scope():
    if len(sys.argv) != 2:
        print("Usage: python script.py graph.txt")
        sys.exit(1)
    
    file_path = sys.argv[1]
    G = read_dimacs_graph(file_path)

    start_time = time.time()
    max_clique = max_clique_ilp(G)
    end_time = time.time()
    
    print(f"Max clique: {max_clique}")
    #print(f"Runtime: {end_time - start_time:.4f} seconds")
    
scope()