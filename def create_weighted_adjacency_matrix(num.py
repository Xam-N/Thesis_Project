def create_weighted_adjacency_matrix(num_nodes, edges, weights):
    adjacency_matrix = [[float('inf')] * num_nodes for _ in range(num_nodes)]
    for edge, weight in zip(edges, weights):
        node1, node2 = edge
        adjacency_matrix[node1][node2] = weight
        adjacency_matrix[node2][node1] = weight  # If the graph is undirected
    for i in range(num_nodes):
        adjacency_matrix[i][i] = 0  # Set diagonal elements to 0
    return adjacency_matrix

# Example usage
num_nodes = 5
edges = [(0, 1), (0, 2), (1, 3), (2, 4)]
weights = [2, 3, 1, 4]
adj_matrix = create_weighted_adjacency_matrix(num_nodes, edges, weights)
for row in adj_matrix:
    print(row)
    
    
def add_edge_with_weight(adjacency_matrix, node1, node2, weight):
    adjacency_matrix[node1][node2] = weight
    adjacency_matrix[node2][node1] = weight  # If the graph is undirected

# Example usage
num_nodes = 5
adj_matrix = [[float('inf')] * num_nodes for _ in range(num_nodes)]

add_edge_with_weight(adj_matrix, 0, 1, 2)
add_edge_with_weight(adj_matrix, 0, 2, 3)

for row in adj_matrix:
    print(row)
    
      