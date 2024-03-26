import networkx as nx
import matplotlib.pyplot as plt
import re

def parse_requirement(requirement):
    # Remove spaces and split the requirement based on logical operators
    units = re.split(r'\s*(?:and|or)\s*', requirement)
    
    # Create a directed graph
    G = nx.DiGraph()
    
    # Add nodes for the units
    for unit in units:
        if unit.isalpha():
            G.add_node(unit)
    
    # Add edges representing the requirements
    for unit in units[1:]:
        G.add_edge(units[0], unit)
    
    return G

def draw_requirement_graph(requirement):
    G = parse_requirement(requirement)
    
    # Draw the graph
    pos = nx.spring_layout(G)
    nx.draw(G, pos, with_labels=True, node_size=3000, node_color='skyblue', font_size=12, font_weight='bold', arrowsize=20)
    plt.title("Unit Requirements DAG")
    plt.show()

# Example usage
requirement = "COMP3010 requires (COMP3100 or COMP3000) and (ENGG3000 or ENGG3050)"
draw_requirement_graph(requirement)