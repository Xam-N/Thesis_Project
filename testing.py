import numpy as np



def addNode(adj_matrix: list, new_node):

    # Check if the nodes of the edge exist in the node list
    if adj_matrix is None:
      adj_matrix = np.array([['',new_node],[new_node,0]])
      return adj_matrix

    if new_node in adj_matrix[0]:
        #print(new_node + "The node is already in the matrix")
        return adj_matrix
      
    arr = np.empty(adj_matrix.shape[1],str)
    arr[0] = new_node
    for i in range(1, arr.size):
      arr[i] = 0
    #adj_matrix[1][1] edge weights are at this
    adj_matrix = np.insert(adj_matrix, adj_matrix.shape[0], arr, axis=0)
    #print(adj_matrix, "After inserting row")
    arr2 = np.empty(adj_matrix.shape[0], dtype='U25')
    arr2[0] = new_node
    print(new_node)
    print(arr2[0])
    print("Testing")
    for i in range(1, arr2.size):
      arr2[i] = 0
    adj_matrix = np.insert(adj_matrix, adj_matrix.shape[1], arr2,axis=1)
    #print(adj_matrix, " After inserting column")
    return adj_matrix
 
def addEdge(adj_matrix:list, sourceNode, endNode, weight):
     
    # Check if the nodes of the edge exist in the node list
  if sourceNode not in adj_matrix:
    #print(sourceNode, " This does not exist within the array yet")
    adj_matrix = addNode(adj_matrix,sourceNode)
  
  #print(len(np.where(adj_matrix[0]==sourceNode)))
  
  if endNode not in adj_matrix:
    #print(sourceNode, " This does not exist in the array yet")
    adj_matrix = addNode(adj_matrix,endNode)
    #print(adj_matrix, " This is the new matrix")
  #print(len(np.where(adj_matrix[0]==endNode)))
    # Get the indices of the source and destination nodes
  srcIndex = np.where(adj_matrix[0]==sourceNode)[0][0]
  destIndex = np.where(adj_matrix[0]==endNode)[0][0]
  
  
    # Update the adjacency matrix with the weight
  """  
  print(srcIndex)
  print(destIndex)
  print(len(adj_matrix))
  print(len(adj_matrix[srcIndex]))
  print(adj_matrix)
  """
  adj_matrix[srcIndex][destIndex] = weight
  adj_matrix[destIndex][srcIndex] = weight
    
  return adj_matrix    



adj = None
adj = addNode(adj  , "And")
adj = addNode(adj,"Ban")
print(adj)
adj = addEdge(adj, "And","Ban",1)
print(adj)