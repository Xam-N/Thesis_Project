from POS_Tagging import sample, custom_tags, requirement_word_tag
from Phrase_Types import phraseTags, requirement_tag
import re
import numpy as np

def createMatrix(data):
    adjMatrix = []  
    
    for index,row in data.iterrows():
      addNode(adjMatrix, row['Academic Item'])
        
    for index,row in data.iterrows():
        wordTags = requirement_word_tag(row['Description'])
        requirementType = requirement_tag(row['Description'])
        addRequirementEdges(adjMatrix, row['Academic Item'], wordTags, requirementType,data)
  
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
    for dataUnitCode,datarequirements in data.items():
      my_regex = re.escape(unitYear) + r"[0-9]{3}"
      if re.findall(my_regex,unit) != None:
        addEdge(adjMatrix,unit, dataUnitCode,weight)
  
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
    if not adj_matrix:
      adj_matrix = np.array([['',new_node],[new_node,0]])
      return adj_matrix

    if new_node in adj_matrix[0]:
        print(new_node + "The node is already in the matrix")
        return adj_matrix

    #adj_matrix[1][1] edge weights are at this
    adj_matrix[0].append(new_node) # adds to the column unit list
    adj_matrix.append(new_node) #adds to the row unit list
    
    for i in range(1,len(adj_matrix)-1):
      adj_matrix[i][len(adj_matrix)-1] = 0
      
    for j in range(1,len(adj_matrix)-1):
      adj_matrix[len(adj_matrix)-1][j] = 0

    # Add a new row for the new node
    adj_matrix.append([0] * len(adj_matrix[0]))
    adj_matrix[-1][0] = new_node

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