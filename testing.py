import numpy as np



def addNode(adj_matrix: list, new_node):

    # Check if the nodes of the edge exist in the node list
    if adj_matrix is None:
      adj_matrix = np.array([['',new_node],[new_node,0]])
      return adj_matrix

    if new_node in adj_matrix[0]:
        print(new_node + "The node is already in the matrix")
        return adj_matrix
      
    arr = np.zeros(adj_matrix.shape[0])
    print(arr)

    #adj_matrix[1][1] edge weights are at this
    print(adj_matrix)

    adj_matrix = np.append(adj_matrix,arr, axis= 0 ) #adds to the row unit list
    adj_matrix = np.append(adj_matrix,arr, axis= 1) # adds to the column unit list
    
    for i in range(1,len(adj_matrix)-1):
      print(adj_matrix[i][len(adj_matrix)-1])
      adj_matrix[i][len(adj_matrix)-1] = 0
      
    for j in range(1,len(adj_matrix)-1):
      adj_matrix[len(adj_matrix)-1][j] = 0

    return adj_matrix
 
def addEdge(adj_matrix:list, sourceNode, endNode, weight):
     
    # Check if the nodes of the edge exist in the node list
  if sourceNode not in adj_matrix[0]:
    addNode(adj_matrix,sourceNode)
  
  if endNode not in adj_matrix[0]:
    addNode(adj_matrix,endNode)
    
    # Get the indices of the source and destination nodes
  srcIndex = adj_matrix[0].index(sourceNode)
  destIndex = adj_matrix[0].index(endNode)
  
  
    # Update the adjacency matrix with the weight
  print(srcIndex)
  print(destIndex)
  print(len(adj_matrix))
  print(len(adj_matrix[srcIndex]))

  adj_matrix[srcIndex][destIndex] = weight
  adj_matrix[destIndex][srcIndex] = weight
    
  return adj_matrix    



adj = None
adj = addNode(adj  , "A")
adj = addNode(adj,"B")
print(adj)