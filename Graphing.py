from POS_Tagging import sample, custom_tags, requirement_word_tag
from Phrase_Types import phraseTags, requirement_tag
import re
import numpy as np

def createMatrix(data):
    
    adjMatrix = None
    
    #for index,row in data.iterrows():
      #print("Here")
     # adjMatrix = addNode(adjMatrix, row['Academic Item'])
      #print("there")
    
    
    #np.savetxt('EmptyAdjMatrix.txt', adjMatrix)
        
    for index,row in data.iterrows():
      
      wordTags = requirement_word_tag(row['Description'])
      requirementType = requirement_tag(row['Description'])
      addRequirementEdges(adjMatrix, row['Academic Item'], wordTags, requirementType,data)
      if index > 1000: 
        break

    return adjMatrix



def addRequirementEdges(adjMatrix, unit, wordTags, requirementType,data):
  if requirementType == "Credit_Point":
    for word,wordTag in wordTags.items(): # loop through each requirements words
      if wordTag == 'creditPoints':
        weight = 10/(int(re.findall(r'\d+',word)[0])) # 10/number of credit points required
      if wordTag == 'unitYear': 
        unitYear = (re.findall(r'\d',word))[0]
      if wordTag == 'inequal':
        unitYear = unitYear + "+"
      if wordTag == 'subjectArea':
        unitSubject = word
    for index,row in data.iterrows():
      my_regex = re.escape(unitYear) + r"[0-9]{3}"
      print("My Regex: ",my_regex)
      print(row['Academic Item'])
      
      if re.findall(my_regex,row['Academic Item']) != None:
        print("This matched")
        print(re.findall(my_regex,row['Academic Item']))
        addEdge(adjMatrix,unit, row['Academic Item'],weight)
  
  if requirementType == "Boolean":
    weight = 1
    andCounter = 0
    for word,wordTag in wordTags.items():
      if wordTag == 'unitCode':
        tempUnitCode = word
      if wordTag == 'bool':
        if word == 'or':
          addEdge(adjMatrix,unit,tempUnitCode,weight)
          tempUnitCode = ''
        if word =='and':
          andCounter = andCounter + 1
    if tempUnitCode != '':
      addEdge(adjMatrix,unit,tempUnitCode,weight)
    if andCounter != 0:
      weight = weight/andCounter
      for word,wordTag in wordTags.items():
        if wordTag == 'unitCode':
          addEdge(adjMatrix,unit,word,weight)
      
    #weight is 1/AND counter
  
def addNode(adj_matrix: list, new_node):

    # Check if the nodes of the edge exist in the node list
    if adj_matrix is None:
      adj_matrix = np.array([['',new_node],[new_node,0]])
      return adj_matrix

    #print(new_node)
    #print(adj_matrix)
    if new_node in adj_matrix[0]:
        #print(new_node + "The node is already in the matrix")
        return adj_matrix
      
    arr = np.empty(adj_matrix.shape[1],dtype='U25')
    arr[0] = new_node
    for i in range(1, arr.size):
      arr[i] = 0
    #adj_matrix[1][1] edge weights are at this
    adj_matrix = np.insert(adj_matrix, adj_matrix.shape[0], arr, axis=0)
    #print(adj_matrix, "After inserting row")
    arr2 = np.empty(adj_matrix.shape[0], dtype='U25')
    arr2[0] = new_node
    for i in range(1, arr2.size):
      arr2[i] = 0
    adj_matrix = np.insert(adj_matrix, adj_matrix.shape[1], arr2,axis=1)
    #print(adj_matrix, " After inserting column")
    print(adj_matrix)
    return adj_matrix
 
def addEdge(adj_matrix:list, sourceNode, endNode, weight):
     
  print("Adding Edges")
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
  
  print(sourceNode)
  print("Here ", endNode)
  
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
  print(adj_matrix)  
  return adj_matrix
