'''
Network Flow: Write an algorithm in a language of your choice that takes as input
a flow network in modified DIMACS format and prints all flow augmenting paths.
Ensure infinite looping isn't possible. I will try to break your code.
Ex. File (tab separated values)

5 6         The first row is the vertex count and then the arc count
0 1 4       The remaining rows are the arcs: vertex 1, vertex 2, and arc weight
0 2 3
0 3 5
1 4 7
2 4 18
3 4 6

0 will always be the source vertex, and the vertex with the largest id will always be the sink. 
In the above example that makes 0 the source and 4 the sink.
'''

import sys

#Read a flow network from a file in modified DIMACS format
def read_flow_network(filename):
    with open(filename, 'r') as f:
        lines = f.readlines()
    
    vertex_count, arc_count = map(int, lines[0].split())
    graph = [[] for i in range(vertex_count)]
    capacity = [[0] * vertex_count for j in range(vertex_count)]
    
    #Parse arcs
    for i in range(1, arc_count + 1):
        if i < len(lines):
            vertex_one, vertex_two, arc_weight = map(int, lines[i].split())
            graph[vertex_one].append(vertex_two)

            #Add reverse edge for residual graph
            if vertex_two not in graph[vertex_one]:
                graph[vertex_two].append(vertex_one)
            capacity[vertex_one][vertex_two] = arc_weight
    
    source = 0
    sink = vertex_count - 1
    return graph, capacity, source, sink


#Find an augmenting path using BFS
def find_augmenting_path(graph, capacity, flow, source, sink):
    visited = [False] * len(graph)
    visited[source] = True
    queue = [source]
    parent = [-1] * len(graph)
    
    while queue:
        u = queue.pop(0)
        for v in graph[u]:
            if not visited[v] and capacity[u][v] - flow[u][v] > 0:
                visited[v] = True
                parent[v] = u
                queue.append(v)
                
                if v == sink:
                    path = []
                    current = sink
                    while current != -1:
                        path.append(current)
                        current = parent[current]
                    return path[::-1]  #Reverse to get source-to-sink path
    return None  

#Find all augmenting paths in the flow network using BFS 
def find_augmenting_pathss(graph, capacity, source, sink):
    flow = [[0] * len(graph) for i in range(len(graph))]
    augmenting_paths = []
    
    #Keep finding paths until no more
    while True:
        path = find_augmenting_path(graph, capacity, flow, source, sink)
        if not path:
            break
        
        path_flow = float('inf')
        for i in range(len(path) - 1):
            u = path[i]
            v = path[i + 1]
            path_flow = min(path_flow, capacity[u][v] - flow[u][v])
        
        for i in range(len(path) - 1):
            u = path[i]
            v = path[i + 1]
            flow[u][v] += path_flow
            flow[v][u] -= path_flow
        
        augmenting_paths.append(path)
    return augmenting_paths




#---Main program---
if len(sys.argv) < 2:
    print("Usage: python network_flow.py <input_file>")
    sys.exit(1)

file = sys.argv[1]
try:
    graph, capacity, source, sink = read_flow_network(file)
    augmenting_paths = find_augmenting_pathss(graph, capacity, source, sink)
    
    if not augmenting_paths:
        print("No augmenting paths found.")
    else:
        print(f"Found {len(augmenting_paths)} augmenting paths:")
        for i, path in enumerate(augmenting_paths):
            path_str = " -> ".join(map(str, path))
            print(f"Path {i}: {path_str}")

except Exception as e:
    print(f"Error: {e}")