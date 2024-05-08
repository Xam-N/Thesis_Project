from POS_Tagging import sample, custom_tags, requirement_word_tag
from Phrase_Types import phraseTags, requirement_tag
import re
import numpy as np


def createCoReqMatrix(data,desired):
    coReqAdjMatrix = None 
    for index,row in data.iterrows(): #iterate through all the data
      if  row['Academic Item'] in desired: #check to see if the current node is in the desired list of units
        
        coReqAdjMatrix = addNode(coReqAdjMatrix,row['Academic Item'])
        #print(adjMatrix)
          
          #print(adjMatrix)
        #if index > 500:
        #  break
  #print(adjMatrix)
  
    for index,row in data.iterrows(): #iterate through all the data
         
      if row['Academic Item'] in desired: #check to see if the current node is in the desired list of units
        
        if row['Co-requisite'] != "":
          wordTagCo = requirement_word_tag(row['Co-requisite'])
          requirementTypeCo = requirement_tag(wordTagCo) 
          print("This is the Co-requirement type : ",requirementTypeCo)
          coReqAdjMatrix = addRequirementEdges(coReqAdjMatrix, row['Academic Item'], wordTagCo, requirementTypeCo,data,1)
        

    return coReqAdjMatrix


def createPreReqMatrix(data,desired):
    
    preReqAdjMatrix = None 
    for index,row in data.iterrows(): #iterate through all the data
      if  row['Academic Item'] in desired: #check to see if the current node is in the desired list of units
        
        preReqAdjMatrix = addNode(preReqAdjMatrix,row['Academic Item'])
        #print(adjMatrix)
          
          #print(adjMatrix)
        #if index > 500:
        #  break
  #print(adjMatrix)
    for index,row in data.iterrows(): #iterate through all the data
         
      if row['Academic Item'] in desired: #check to see if the current node is in the desired list of units
        
        if row['Pre-requisite'] != "":
          preReqAdjMatrix = addNode(preReqAdjMatrix, row['Academic Item']) # add the current unit of the requirement doc to the graph
          wordTagPre = requirement_word_tag(row['Pre-requisite'])# tag the pre-requisite words with a tag
          requirementTypePre = requirement_tag(wordTagPre)#tag the requirement with a phrase type
          print("This is the Pre-requirement type : ",requirementTypePre)
          preReqAdjMatrix = addRequirementEdges(preReqAdjMatrix, row['Academic Item'], wordTagPre, requirementTypePre,data,1)

    return preReqAdjMatrix

def findWeight(wordTags,weight): #finds the number of and thingys to determine the weight each edge of a nested requirement should be added with
  
  andCounter = 0.0
  
  lBracketCounter = 0
  
  for index,word in enumerate(wordTags):
    if index == 0 and (word[0] == "and" or word[0] == "includes" or word[0] == "including"):
      andCounter -= 1
      
    if word[0] ==  "(":
      lBracketCounter = lBracketCounter + 1

    if word[0] == ")":
      lBracketCounter = lBracketCounter - 1
      
    if (word[0] == "and" or word[0] == "includes" or word[0] == "including") and lBracketCounter == 0: #if an and is present increment the AND counter to reflect as such
      andCounter += 1 
  
  #print("The given word list is: ",wordTags)
  print("The weight before is: ",weight)
  print(wordTags)
  
  
  weight = weight / (andCounter+1) #1 and has 2 nodes of weight 0.5 therefore divide weight by andCounter + 1
  
  print("The weight after is: ",weight)
  print("The weight of the new edge should be: ",weight," andCounter is : ",andCounter)
  return weight

def addRequirementEdges(adjMatrix, unit, wordTags, requirementType,data,weight):
  
  if unit == "ENGG2000":
    print("Aloha")
    for word in wordTags:
      if word[1] == "unitCode":
        adjMatrix = addEdge(adjMatrix,unit,word[0],1)
    return adjMatrix
  
  print("This is the word list inputed for unit ", unit ,": ", wordTags)
  print(requirementType)
    
  if "fake_credit_point" in requirementType:
    print("Never")
    for index,word in enumerate(wordTags): # loop through each requirements words
      if word[1] == 'creditPoints':
        creditWeight = 10/(int(re.findall(r'\d+',word[0])[0])) # 10/number of credit points required
      if word[1] == 'lbracket':
        requirementType = requirement_tag(wordTags[index+1:len(wordTags)-1])
        adjMatrix = addRequirementEdges(adjMatrix,unit,wordTags[index+1:len(wordTags)-1],requirementType,data,weight/creditWeight)
        return adjMatrix
    
    
  if requirementType == "Credit_Point": #this is broken, only works with things already in the 
    
    above = False
    unitSubject = ""#holds the subject code required for units to count for the credit point e.g. engg
    creditWeight = 1 #number of credit points required e.g. 10cp = 1
    unitYear = ""
    
    for word in wordTags: # loop through each requirements words
      if word[1] == 'creditPoints':
        creditWeight = 10/(int(re.findall(r'\d+',word[0])[0])) # 10/number of credit points required
      if word[1] == 'unitYear': 
        unitYear = (re.findall(r'\d',word[0]))[0]
      if word[1] == 'inequal':
        above = True
      if word[1] == 'subjectArea':
        unitSubject = word[0]
      
    
    my_regex = r"[0-9]{3}" #checks for 000 or 131 or etc.
    plus = ""
    
    if unitYear != "":
      plus = "(" + unitYear + ")"
      
    else:
      plus = "[0-9]"
      
    if above == True: 
      plus = "[" + unitYear + "-9]"
    
    if unitSubject != "":
      plus = "(" + unitSubject + ")" + plus

    my_regex = plus + my_regex
    print("This is the credit point regex : ",my_regex)
        
    for row in adjMatrix:
      if row[0] == "" or row[0] == unit or "#" in row[0] or "!" in row[0]:
        pass
      else:
        if len(re.findall(my_regex,row[0])) != 0: #if there is a regex match
          adjMatrix = addCreditPointEdge(adjMatrix,unit,row[0],weight,creditWeight)
        else:
          pass
  
  if requirementType == "Boolean":
    andCounter = 0
    tempUnitCode = ''
    for index,word in enumerate(wordTags):
      if word[1] == 'lbracket' or word[1] == 'rbracket': #?????
        pass
      if word[1] == 'unitCode':
        tempUnitCode = word[0]
      if word[1] == 'bool' and tempUnitCode != '':
        if word[0] == 'or':
          adjMatrix = addOrEdge(adjMatrix,unit,tempUnitCode,weight) 

          tempUnitCode = ''
        if word[0] =='and' or word[0] == "includes" or word[0] == "including":
          andCounter = andCounter + 1
    if tempUnitCode != '':

      adjMatrix = addEdge(adjMatrix,unit,tempUnitCode,weight)

    if andCounter != 0:

      weight = findWeight(wordTags,weight)
      
      for word in wordTags:
        if word[1] == 'unitCode':

          adjMatrix = addEdge(adjMatrix,unit,word[0],weight)

    return adjMatrix  


  #change this asap rocky

  lbracketIndex = 0
  rbracketIndex = 0
  
  for index,word in enumerate(wordTags):
    if word[1] == "lbracket":
      lbracketIndex = index
    if word[1] == "rbracket":
      rbracketIndex = index
      newWords = wordTags[lbracketIndex+1:rbracketIndex] #adjust the word list to be after the section of brackets ends
      #print("newWords = ",newWords)
      newTags = requirement_tag(newWords) 
      #print("newTags = ",newTags)
      weight = findWeight(wordTags,weight)
       #figure out how to find the weight before I run this code
      
      adjMatrix = addRequirementEdges(adjMatrix,unit,newWords,newTags,data,weight)
  
  return adjMatrix
  
def addNode(adj_matrix: list, new_node):
  print("Adding Node")  

  if adj_matrix is None: #if matrix does not exist, then build it
      adj_matrix = np.array([['',new_node],[new_node,0]])
      return adj_matrix

  if new_node in adj_matrix[0]:

      return adj_matrix
    
  arr = np.empty(adj_matrix.shape[1],dtype='U25')
  arr[0] = new_node
  for i in range(1, arr.size):
    arr[i] = 0

  adj_matrix = np.insert(adj_matrix, adj_matrix.shape[0], arr, axis=0)

  arr2 = np.empty(adj_matrix.shape[0], dtype='U25')
  arr2[0] = new_node
  for i in range(1, arr2.size):
    arr2[i] = 0
  adj_matrix = np.insert(adj_matrix, adj_matrix.shape[1], arr2,axis=1)

  return adj_matrix
 
def addOrEdge(adj_matrix,sourceNode,endNode,weight): #to do
  
  print("Adding OR edge")
  newNode = sourceNode + "#"
  
  while newNode in adj_matrix:
    newNode = newNode + "1"
    
  if newNode not in adj_matrix:
    #print("Here")
    adj_matrix = addEdge(adj_matrix,sourceNode,newNode,weight)
  
  adj_matrix = addEdge(adj_matrix,newNode,endNode,1)
    
  return adj_matrix

def addCreditPointEdge(adj_matrix,sourceNode,endNode,weight,creditWeight): #to do
  
  print("Adding Credit edge and node")
  newNode = sourceNode + "!"
  
  if newNode not in adj_matrix:
    #print("Here")
    adj_matrix = addEdge(adj_matrix,sourceNode,newNode,weight) #adds credit point node if it does not already exist
  
  adj_matrix = addEdge(adj_matrix,newNode,endNode,creditWeight)#adds the edge from the credit point node to the end node
    
  return adj_matrix
  
def addEdge(adj_matrix:list, sourceNode, endNode, weight):

  print("Adding edge")
  if adj_matrix is None:

    adj_matrix = addNode(adj_matrix, None)

  #if sourceNode not in adj_matrix:

   # adj_matrix = addNode(adj_matrix,sourceNode)

  #if endNode not in adj_matrix:

  #  adj_matrix = addNode(adj_matrix,endNode)

  srcIndex = np.where(adj_matrix[0]==sourceNode)[0]

  destIndex = np.where(adj_matrix[0]==endNode)[0]

  if(adj_matrix[destIndex,srcIndex]!='0'):
    if weight < float(adj_matrix[destIndex,srcIndex]):
      pass
  
  adj_matrix[destIndex,srcIndex] = weight
  
  return adj_matrix
