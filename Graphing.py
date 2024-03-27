from POS_Tagging import sample, custom_tags, requirement_word_tag
from Phrase_Types import phraseTags, requirement_tag

def createMatrix(data):
    adjMatrix = []
    
    for unit, unitRequirements in data.items():
        addNode(adjMatrix, unit)
        wordTags = requirement_word_tag(unitRequirements)
        requirementType = requirement_tag(unitRequirements)
        #addRequirementEdges(adjMatrix, unit, wordTags, requirementType)
    
def addNode(adj_matrix: list, new_node):

    # Check if the nodes of the edge exist in the node list
  if new_node not in adj_matrix[0]:
    print("The node is already in the matrix")
    return adj_matrix
      
  # Add new column and row to the matrix
  for row in adj_matrix:
      row.append(0)
      adj_matrix[0].append(1* len(adj_matrix[0]))
    
    # Populate the node edges as 0
  adj_matrix[0].append(new_node)
  for i in range(1, len(adj_matrix)):
      adj_matrix[i][-1] = 0
    
  return adj_matrix
 
def addEdge(adj_matrix:list, sourceNode, endNode, weight):
    
    # Check if the nodes of the edge exist in the node list
  if sourceNode not in adj_matrix[0] or endNode not in adj_matrix[0]:
    print("Error: One or both nodes of the edge do not exist.")
    return adj_matrix
    
    # Get the indices of the source and destination nodes
  src_index = adj_matrix[0].index(sourceNode)
  dest_index = adj_matrix[0].index(endNode)
    
    # Update the adjacency matrix with the weight
  adj_matrix[src_index][dest_index] = weight
  adj_matrix[dest_index][src_index] = weight
    
  return adj_matrix
  
