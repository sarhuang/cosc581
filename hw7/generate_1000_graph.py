import networkx as nx

def write_dimacs_graph(G, filename):
    with open(filename, 'w') as f:
        n_vertices = G.number_of_nodes()
        n_edges = G.number_of_edges()
        
        f.write(f"c DIMACS graph generated for max clique problem\n")
        f.write(f"p edge {n_vertices} {n_edges}\n")
        
        for u, v in G.edges():
            f.write(f"e {u+1} {v+1}\n")


def generate_test_graph(n, p, filename):
    G = nx.gnp_random_graph(n, p)
    write_dimacs_graph(G, filename)
    return G


# Create a 1000-vertex graph
n = 1000  # Number of vertices
p = 0.05  # Probability of edge creation between any two vertices
filename = "examples/graph_1000_vertices5.txt"
G = generate_test_graph(n, p, filename)
print(f"Created graph with {G.number_of_nodes()} vertices and {G.number_of_edges()} edges")