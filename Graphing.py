from POS_Tagging import sample, custom_tags, requirement_word_tag
from Phrase_Types import phraseTags, requirement_tag
import re
import numpy as np

def createMatrix(data):
    
    adjMatrix = None
    desired = ["ENGG1000","ENGG1050","ENGG2000","ENGG3000","COMP1000","ENGG2050","MATH1015","MATH1007","MATH1007","MATH1000","MATH1010"]    
    for index,row in data.iterrows():
      #print("Here")
      if row['Academic Item'] in desired:
        adjMatrix = addNode(adjMatrix, row['Academic Item'])
      #print("there")
    
    #I think for brackets I should run the requirement recursively for how many brackets that I need to do.
    #essentially create a parse tree only when brackets are involved.
    #this could also maybe be used for And relations
    
    
    
    
    #np.savetxt('EmptyAdjMatrix.txt', adjMatrix)
    
    #counter = 0
    for index,row in data.iterrows():
      if row['Academic Item'] in desired:
        #print("Is this bugged : ", row['Academic Item'])
        adjMatrix = addNode(adjMatrix, row['Academic Item'])
        wordTagPre = requirement_word_tag(row['Pre-requisite'])
        requirementTypePre = requirement_tag(row['Pre-requisite'])
        print("This is the requirement type : ",requirementTypePre)
        #if requirementTypePre == 'Boolean':
        #  counter = counter + 1
        #  print("This workded??????")
        #if requirementTypePre == '':
          #print(row['Pre-requisite'])
        #  print("Help")
        #print("Adj Matrix is equal to : ", adjMatrix)
        adjMatrix = addRequirementEdges(adjMatrix, row['Academic Item'], wordTagPre, requirementTypePre,data,1)
        #print("Adj Matrix is equal to : ", adjMatrix, wordTagPre, row['Academic Item'])
        wordTagCo = requirement_word_tag(row['Co-requisite'])
        requirementTypeCo = requirement_tag(row['Co-requisite'])
        print("This is the requirement type : ",requirementTypeCo)
        adjMatrix = addRequirementEdges(adjMatrix, row['Academic Item'], wordTagCo, requirementTypeCo,data,-1)
        #if index > 5:
         # break
    
    #print(counter)
    return adjMatrix



def addRequirementEdges(adjMatrix, unit, wordTags, requirementType,data, Pre):
  
      
  
  
  if requirementType == "":
    return adjMatrix
  
  if requirementType == "Credit_Point":
    for word,wordTag in wordTags.items(): # loop through each requirements words
      if wordTag == 'creditPoints':
        weight = 10/(int(re.findall(r'\d+',word)[0])) # 10/number of credit points required
      if wordTag == 'unitYear': 
        unitYear = (re.findall(r'\d',word))[0]
      if wordTag == 'inequal':
        above = True
      if wordTag == 'subjectArea':
        unitSubject = word
        
    
    for row in adjMatrix: # must change this to the adjacency matrix cause otherwise this code will never finishfire
      my_regex = re.escape(unitYear) + r"[0-9]{3}"
      print("My Regex: ",my_regex)
      print(row[0])
      
      if re.findall(my_regex,row[0]) != None:
        print("This matched")
        print(re.findall(my_regex,row[0]))
        if Pre == False:
          weight = weight * -1
        adjMatrix = addEdge(adjMatrix,unit, row[0],weight)
  
  if requirementType == "Boolean":
    weight = 1
    andCounter = 0
    tempUnitCode = ''
    for word,wordTag in wordTags.items():
      #print("Word is : ",word)
      #print("Word Tag is : ",wordTag)
      if wordTag == 'lbracket' or wordTag == 'rbracket':
        print("Bracket Alert")
        return adjMatrix
      if wordTag == 'unitCode':
        tempUnitCode = word
      if wordTag == 'bool':
        if word == 'or':
          #print("if or : ", adjMatrix)
          adjMatrix = addEdge(adjMatrix,unit,tempUnitCode,weight*Pre)
          #print("if or : ", adjMatrix)
          tempUnitCode = ''
        if word =='and':
          andCounter = andCounter + 1
    if tempUnitCode != '':
      #print(tempUnitCode)
      #print(unit)
      #print(weight)
      #print("if temp unit code : ", adjMatrix)
      adjMatrix = addEdge(adjMatrix,unit,tempUnitCode,weight*Pre)
      #print("if temp unit code : ", adjMatrix)
    if andCounter != 0:
      #print("Here")
      #print("andCounter is equal to: ", andCounter)
      weight = weight/(andCounter+1)
      #print("Weight is equal to: ",weight)
      for word,wordTag in wordTags.items():
        if wordTag == 'unitCode':
          #print("and garbage: ", adjMatrix)
          adjMatrix = addEdge(adjMatrix,unit,word,weight*Pre)
          #print("and garbage: ", adjMatrix)
    
    return adjMatrix  
    #weight is 1/AND counter
  
def addNode(adj_matrix: list, new_node):

    # Check if the nodes of the edge exist in the node list
    if adj_matrix is None:
      #print("New Matrix")
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
    #print(adj_matrix)
    return adj_matrix
 
def addEdge(adj_matrix:list, sourceNode, endNode, weight):
     
  print("Adding Edges")
  #print(adj_matrix)
  #print("Source Node is: ",sourceNode)
  if adj_matrix is None:
    print("Matrix is none for some reason???")
    adj_matrix = addNode(adj_matrix, None)
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
  
  #print(sourceNode)
  #print("Here ", endNode)
  
  srcIndex = np.where(adj_matrix[0]==sourceNode)[0]
  #print("srcIndex is: ",srcIndex)
  destIndex = np.where(adj_matrix[0]==endNode)[0]
  #print("destIndex is: ",destIndex)
  #print(adj_matrix)
  #print(len(adj_matrix))
  #print(len(adj_matrix[0]))
  #print(adj_matrix[srcIndex][5])
  
  
    # Update the adjacency matrix with the weight
  """  
  print(srcIndex)
  print(destIndex)
  print(len(adj_matrix))
  print(len(adj_matrix[srcIndex]))
  print(adj_matrix)
  """
  print("Before the weight assignments: ",adj_matrix)
  adj_matrix[srcIndex,destIndex] = weight
  adj_matrix[destIndex,srcIndex] = weight
  print("After the weight assignments: ",adj_matrix)
  #print(adj_matrix)
  return adj_matrix
