import sys
import networkx as nx
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


#Bron-Kerbosch algorithm
def bron_kerbosch(G, r, p, x, max_clique):
    #if P and X are both empty then
    if not p and not x:
        #report R as a maximal clique
        if len(r) > len(max_clique[0]):
            max_clique[0] = r.copy()
        return
    
    p_copy = p.copy()
    #for each vertex v in P do
    for v in p_copy:
        neighbors = set(G.neighbors(v))

        #BronKerbosch1(R ⋃ {v}, P ⋂ N(v), X ⋂ N(v))
        bron_kerbosch(G, r | {v}, p & neighbors, x & neighbors, max_clique)
        
        # Move v from p to x
        #P := P \ {v}
        #X := X ⋃ {v}
        p.remove(v)
        x.add(v)


def find_maximum_clique(G):
    vertices = set(G.nodes())
    max_clique = [[]] 
    bron_kerbosch(G, set(), vertices, set(), max_clique)
    return sorted(max_clique[0])  



def scope():
    if len(sys.argv) != 2:
        print("Usage: python script.py graph.txt")
        sys.exit(1)
    
    file_path = sys.argv[1]
    G = read_dimacs_graph(file_path)
    
    start_time = time.time()
    max_clique = find_maximum_clique(G)
    end_time = time.time()

    print(f"Max clique: {max_clique}")
    print(f"Runtime: {end_time - start_time:.4f} seconds")

scope()