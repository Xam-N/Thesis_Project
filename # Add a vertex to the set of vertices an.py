import re

class DAG:
    def __init__(self):
        self.nodes = []
        self.adj_matrix = []

    def add_node(self, unit):
        if unit not in self.nodes:
            self.nodes.append(unit)
            # Expand the adjacency matrix
            for row in self.adj_matrix:
                row.append(0)
            self.adj_matrix.append([0] * len(self.nodes))
        else:
            print("Node already exists in the graph.")

    def add_edge(self, src_unit, dest_unit):
        if src_unit in self.nodes and dest_unit in self.nodes:
            src_index = self.nodes.index(src_unit)
            dest_index = self.nodes.index(dest_unit)
            self.adj_matrix[src_index][dest_index] = 1
        else:
            print("One or both units do not exist in the graph.")

    def display_graph(self):
        print("Graph Nodes:")
        print(self.nodes)
        print("Adjacency Matrix:")
        for row in self.adj_matrix:
            print(row)

def parse_requirement(expression):
    # Split the expression into tokens
    tokens = re.findall(r'\b\w+\b|\(|\)', expression)
    return tokens

# Example usage:
dag = DAG()

# Adding units to the graph
dag.add_node('COMP1000')
dag.add_node('COMP1050')
dag.add_node('COMP1100')
dag.add_node('ENGG1000')
dag.add_node('ENGG1050')

# Parse the boolean requirement expression
requirement = "COMP1000 and COMP1050 and COMP1100 and (ENGG1000 or ENGG1050)"
tokens = parse_requirement(requirement)
print(tokens)

# Add edges based on the parsed requirement
for i in range(len(tokens)-1):
    if tokens[i] != '(' and tokens[i+1] != ')':
        dag.add_edge(tokens[i], tokens[i+1])

# Display the graph
dag.display_graph()