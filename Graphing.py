from POS_Tagging import sample, custom_tags, requirement_word_tag
from Phrase_Types import phraseTags, requirement_tag
import re

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
    adj_matrix.append([new_node])
    return adj_matrix
  
  if new_node in adj_matrix[0]:
    print(new_node + "The node is already in the matrix")
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