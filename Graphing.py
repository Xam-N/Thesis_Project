# from POS_Tagging import *
# from Phrase_Types import *
# from Data_Processing import *

def createAdjacencyMatrix(requirementData):
    # Create an empty adjacency matrix
    adjMatrix = create_adjacency_matrix([], [])
    
    # For each unit listed within the requirement data, add it to the adjacency matrix
    for unit, unitRequirements in requirementData.items():
        addNode(adjMatrix, unit)
        wordTags = requirement_word_tag(unitRequirements)
        requirementType = requirement_tag(unitRequirements)
        addRequirementEdges(adjMatrix, unit, wordTags, requirementType)
         
    return adjMatrix
        
def addRequirementEdges(adj_matrix, unitCode, wordTags, requirementType):
    if requirementType == "Boolean":  # Use '==' for string comparison
        i = 0
        while i < len(wordTags)-1:
            if wordTags[i] == "lbracket":
                # Handle bracket logic
                bracket_count = 1
                j = i + 1
                while j < len(wordTags):
                    if wordTags[j] == "lbracket":
                        bracket_count += 1
                    elif wordTags[j] == "rbracket":
                        bracket_count -= 1
                    if bracket_count == 0:
                        break
                    j += 1
                # Now j points to the matching rbracket

            if wordTags[i] == "unitCode":
                if (i < len(wordTags) - 1) and (wordTags[i+1] == "bool" and wordTags[i+1] == "or"):
                    adj_matrix = addEdge(adj_matrix, (unitCode, wordTags[i]), 1)
                if (i < len(wordTags) - 1) and (wordTags[i+1] == "bool" and wordTags[i+1] == "and"):
                    andCounter = 0
                    j = i + 1
                    while j < len(wordTags) - 1:
                        if wordTags[j] == "bool" and wordTags[j+1] == "and":
                            andCounter += 1
                            j += 1  # Increment j to avoid infinite loop
                        else:
                            break
                    weight = 1.0 / (andCounter + 1)
                    adj_matrix = addEdge(adj_matrix, (unitCode, wordTags[i]), weight)

            i += 1
    return adj_matrix

# Assuming these functions are implemented or imported correctly
def requirement_word_tag(unitRequirements):
    pass

def requirement_tag(unitRequirements):
    pass

def addEdge(adj_matrix, edge, weight):
    src, dest = edge
    
    # Check if the nodes of the edge exist in the node list
    if src not in adj_matrix[0] or dest not in adj_matrix[0]:
        print("Error: One or both nodes of the edge do not exist.")
        return adj_matrix
    
    # Get the indices of the source and destination nodes
    src_index = adj_matrix[0].index(src)
    dest_index = adj_matrix[0].index(dest)
    
    # Update the adjacency matrix with the weight
    adj_matrix[src_index][dest_index] = weight
    adj_matrix[dest_index][src_index] = weight
    
    return adj_matrix

def addNode(adj_matrix, new_node):
    # Add new column and row to the matrix
    for row in adj_matrix:
        row.append(0)
    adj_matrix.append([0] * len(adj_matrix[0]))
    
    # Update the node list
    adj_matrix[0].append(new_node)
    for i in range(1, len(adj_matrix)):
        adj_matrix[i][-1] = 0
    return adj_matrix

def create_adjacency_matrix(nodes, edges):
    # Initialize an empty matrix filled with zeros
    matrix = [[0] * len(nodes) for _ in range(len(nodes))]
    
    # Create a dictionary to map node names to indices
    node_index = {node: index for index, node in enumerate(nodes)}
    
    # Fill in the matrix based on edges
    for edge in edges:
        src, dest = edge
        src_index = node_index[src]
        dest_index = node_index[dest]
        # Assuming it's an undirected graph, so filling both src->dest and dest->src
        matrix[src_index][dest_index] = 1
        matrix[dest_index][src_index] = 1
    
    # Add row and column headers
    matrix_with_headers = [[''] + nodes]  # First row with column headers
    for i, row in enumerate(matrix):
        matrix_with_headers.append([nodes[i]] + row)  # Add row headers
    return matrix_with_headers

