import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

# Read the adjacency matrix from CSV file
adjacency_df = pd.read_csv('matrix.csv')

# Get course labels from the first row of the DataFrame
course_labels = list(adjacency_df.columns)

# Convert any non-numeric values to NaN
adjacency_df = adjacency_df.apply(pd.to_numeric, errors='coerce')

# Create a directed graph from the adjacency matrix
G = nx.DiGraph()
for i in range(len(adjacency_df)):
    for j in range(len(adjacency_df.columns)):
        if pd.notnull(adjacency_df.iloc[i, j]) and adjacency_df.iloc[i, j] > 0:
            G.add_edge(course_labels[i], course_labels[j], weight=adjacency_df.iloc[i, j])

# Draw the graph with arrows indicating edge direction
pos = nx.spring_layout(G)  # Position nodes using Fruchterman-Reingold force-directed algorithm
nx.draw_networkx_nodes(G, pos, node_color='lightblue', node_size=1500)
nx.draw_networkx_labels(G, pos)
nx.draw_networkx_edges(G, pos, arrows=True, arrowstyle='->', arrowsize=10, edge_color='gray', width=[d['weight']*5 for (u, v, d) in G.edges(data=True)])
labels = nx.get_edge_attributes(G, 'weight')
nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)
plt.title('Course Network')
plt.show()