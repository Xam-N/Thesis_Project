from POS_Tagging import sample, custom_tags, requirement_word_tag
from Phrase_Types import phraseTags, requirement_tag
import re
import numpy as np

def createMatrix(data,desired):
    
    adjMatrix = None 
    for index,row in data.iterrows(): #iterate through all the data
      
      if row['Academic Item'] in desired: #check to see if the current node is in the desired list of units
        
        adjMatrix = addNode(adjMatrix,row['Academic Item'])
        
        #print(adjMatrix)
        #if index > 5:
         # break
    #print(adjMatrix)
    for index,row in data.iterrows(): #iterate through all the data
         
      if row['Academic Item'] in desired: #check to see if the current node is in the desired list of units
        
        if row['Pre-requisite'] != "":
          adjMatrix = addNode(adjMatrix, row['Academic Item']) # add the current unit of the requirement doc to the graph
          wordTagPre = requirement_word_tag(row['Pre-requisite'])# tag the pre-requisite words with a tag
          requirementTypePre = requirement_tag(wordTagPre)#tag the requirement with a phrase type
          print("This is the Pre-requirement type : ",requirementTypePre)
          adjMatrix = addRequirementEdges(adjMatrix, row['Academic Item'], wordTagPre, requirementTypePre,data,1,1)

        #repeat for co-requisites
        if row['Co-requisite'] != "":
          wordTagCo = requirement_word_tag(row['Co-requisite'])#this also seems useless here
          requirementTypeCo = requirement_tag(wordTagCo) #this seems useless here
          print("This is the Co-requirement type : ",requirementTypeCo)
          adjMatrix = addRequirementEdges(adjMatrix, row['Academic Item'], wordTagCo, requirementTypeCo,data,1,1)
      
        
        #if index > 5:
         # break

    return adjMatrix

def findWeight(wordTags,weight): #finds the number of and thingys to determine the weight each edge of a nested requirement should be added with
  
  andCounter = 0
  
  inside = False
  
  for word in wordTags:
    
    if word[0] == "(": #make sure the ands are not within brackets of their own
      inside = True

    if word[0] == ")":
      inside = False
      
    if word[0] == "and" and inside == False: #if an and is present increment the AND counter to reflect as such
      andCounter += 1 
  
  weight = weight / (andCounter+1) #1 and has 2 nodes of weight 0.5 therefore divide weight by andCounter + 1
  
  print("The weight of the new edge should be: ",weight," andCounter is : ",andCounter)
  return weight

def addRequirementEdges(adjMatrix, unit, wordTags, requirementType,data, Pre,weight): #if adding an OR boolean relation I have to add an extra node I believe, is this true.
  
  print("This is the word list inputed : ", wordTags)
  
  if requirementType == "Credit_Point": #this is broken, only works with things already in the 
    above = False
    unitSubject = ""
    for word in wordTags: # loop through each requirements words
      if word[1] == 'creditPoints':
        weight = weight*10/(int(re.findall(r'\d+',word[0])[0])) # 10/number of credit points required
      if word[1] == 'unitYear': 
        unitYear = (re.findall(r'\d',word[0]))[0]
      if word[1] == 'inequal':
        above = True
      if word[1] == 'subjectArea':
        unitSubject = word[0]
    
    my_regex = r"[0-9]{3}"
    plus = ""
    subject = ""
    if unitSubject != "":
      subject = unitSubject
    if above == True:
      plus = "[" + unitYear + "-9]"
      my_regex = plus + my_regex
      #print("Above is true this is the regex : ",my_regex)
    
    my_regex = plus + my_regex
      #print("Above is not true this is the regex : ",my_regex)
    
    for row in adjMatrix:
      if row[0] == "" or row[0] == unit or "#" in row[0]:
        pass
      else:
        #print("I am here ",row)
        if len(re.findall(my_regex,row[0])) != 0:
          print("This matched ",print(re.findall(my_regex,row[0])))
          #print(len(re.findall(my_regex,row[0])))
          if Pre == False:
            weight = weight * -1
          adjMatrix = addEdge(adjMatrix,unit, row[0],weight)
        else:
          print("This did not match")
  
  if requirementType == "Boolean":
    andCounter = 0
    tempUnitCode = ''
    for word in wordTags:
      #print("Word is : ",word)
      #print("Word Tag is : ",wordTag)
      if word[1] == 'lbracket' or word[1] == 'rbracket':
        print("This is the current requirement for a bracket alert : ",wordTags)
        print("The unit is : ",unit)
        return adjMatrix
      if word[1] == 'unitCode':
        tempUnitCode = word[0]
      if word[1] == 'bool' and tempUnitCode != '':
        if word[0] == 'or':
          #print("if or : ", adjMatrix)
          #adjMatrix = addEdge(adjMatrix,unit,tempUnitCode,weight*Pre) #change this later
          print("the weight prior to the function being called is : ",weight)
          adjMatrix = addOrEdge(adjMatrix,unit,tempUnitCode,weight*Pre) 
          #print("if or : ", adjMatrix)
          tempUnitCode = ''
        if word[0] =='and':
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
      
      #weight = weight/(andCounter+1)
      #trialling here
      weight = findWeight(wordTags,weight)
      
      #print("Weight is equal to: ",weight)
      for word in wordTags:
        if word[1] == 'unitCode':
          #print("and garbage: ", adjMatrix)
          adjMatrix = addEdge(adjMatrix,unit,word[0],weight*Pre)
          #print("and garbage: ", adjMatrix)
    
    return adjMatrix  
    #weight is 1/AND counter
  
  lbracketIndex = 0
  rbracketIndex = 0
  for index,word in enumerate(wordTags):
    if word[1] == "lbracket":
      lbracketIndex = index
    if word[1] == "rbracket":
      rbracketIndex = index
      newWords = wordTags[lbracketIndex+1:rbracketIndex] #adjust the word list to be after the section of brackets ends
      print("newWords = ",newWords)
      newTags = requirement_tag(newWords) 
      print("newTags = ",newTags)
      weight = findWeight(wordTags,weight) #figure out how to find the weight before I run this code
      adjMatrix = addRequirementEdges(adjMatrix,unit,newWords,newTags,data,Pre,weight)
  
  if requirementType == "Composite": #im unsure if I need this anymore
    pass

  return adjMatrix
  
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
 
def addOrEdge(adj_matrix,sourceNode,endNode,weight): #to do
  
  newNode = sourceNode + "#"
  
  if newNode not in adj_matrix:
    print("Here")
    adj_matrix = addEdge(adj_matrix,sourceNode,newNode,weight)
  
  adj_matrix = addEdge(adj_matrix,newNode,endNode,1)
  
  
  
  
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
  #adj_matrix[srcIndex,destIndex] = weight
  if(adj_matrix[destIndex,srcIndex]!='0'):
    print("This is not 0 why? : ",adj_matrix[destIndex,srcIndex])
  adj_matrix[destIndex,srcIndex] = weight
  print("After the weight assignments: ",adj_matrix)
  #print(adj_matrix)
  return adj_matrix
