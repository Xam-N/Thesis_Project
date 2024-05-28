from POS_Tagging import sample, custom_tags, requirement_word_tag
from Phrase_Types import phraseTags, requirement_tag
import re
import numpy as np
import pandas as pd


def createCoReqMatrix(data,desired):
    coReqAdjMatrix = None 
    for index,row in data.iterrows(): #iterate through all the data
      if  row['Academic Item'] in desired: #check to see if the current node is in the desired list of units
        
        coReqAdjMatrix = addNode(coReqAdjMatrix,row['Academic Item'])

  
    for index,row in data.iterrows(): #iterate through all the data
         
      if row['Academic Item'] in coReqAdjMatrix[0]: #check to see if the current node is in the desired list of units
        
        if row['Co-requisite'] != "":
          wordTagCo = requirement_word_tag(row['Co-requisite'])
          coReqAdjMatrix = parse_statement(coReqAdjMatrix,row['Academic Item'],wordTagCo)
   
    return coReqAdjMatrix

def createPreReqMatrix(data,desired):
    counter = 0
    preReqAdjMatrix = None 
    for index,row in data.iterrows(): #iterate through all the data
      
      if  row['Academic Item'] in desired: #check to see if the current node is in the desired list of units
        
        preReqAdjMatrix = addNode(preReqAdjMatrix,row['Academic Item'])
    
    for index,row in data.iterrows(): #iterate through all the data
      if row['Academic Item'] in desired: #check to see if the current node is in the desired list of units
        if row['Pre-requisite'] != "":
          counter = counter + 1
          wordTagPre = requirement_word_tag(row['Pre-requisite'])# tag the pre-requisite words with a tag
          preReqAdjMatrix = parse_statement(preReqAdjMatrix, row['Academic Item'],wordTagPre)

    #print("Counter is equal to: ",counter)
    return preReqAdjMatrix

def addRequirementEdges(adjMatrix, unit, wordTags, requirementType,weight):
  
  #print("This is the word list inputed for unit ", unit ,": ", wordTags)
  #print(requirementType)
  
  if "fake_credit_point" in requirementType: #make sure this is needed, it may/may not be i dont remember what it does lol
    
    print("here")
    adjMatrix = addCreditBooleanEdges(adjMatrix,unit,wordTags,weight)
    
    
  elif requirementType == "Credit_Point": 
    
    adjMatrix = addCreditPointEdges(adjMatrix,unit,wordTags,weight)
    
  
  elif requirementType == "Boolean":
    
    adjMatrix = addBooleanEdges(adjMatrix,unit,wordTags,weight)
    
  return adjMatrix

def addCreditBooleanEdges(adjMatrixFake,unit,wordTags,weight):
  #print("Never_Used")
  for index,word in enumerate(wordTags): # loop through each requirements words
    if word[1] == 'creditPoints':
      creditWeight = 10/(int(re.findall(r'\d+',word[0])[0])) # 10/number of credit points required
    if word[1] == 'lbracket':
      requirementType = requirement_tag(wordTags[index+1:len(wordTags)-1])
      adjMatrixFake = addRequirementEdges(adjMatrixFake,unit,wordTags[index+1:len(wordTags)-1],requirementType,weight/creditWeight)
  
  return adjMatrixFake

def addBooleanEdges(adjMatrixBool,unit,wordTags,weight):
      
    requisiteList = []
    andCounter = 0
    orCounter = 0
    for index, word in enumerate(wordTags):
      if word[1] == 'unitCode':
        requisiteList.append(word[0])
      if word[1] == 'bool':
        if word[0] == "and":
          andCounter = andCounter + 1
        if word[0] == "or":
          orCounter = orCounter + 1
          #i dont know what to do here
    
    if andCounter != 0 and orCounter != 0:
      #print("I dont know what to do")
      return adjMatrixBool
      
    elif andCounter != 0:
      weight = weight/(andCounter + 1)
      for requisite in requisiteList:
        #print("Adding Edge ",unit,"",requisiteList[0],"",weight)
        adjMatrixBool = addEdge(adjMatrixBool,unit,requisite,weight)
    
    elif orCounter != 0:
      if len(requisiteList) == 1:
        #print("Adding Edge ",unit,"",requisiteList[0],"",weight)
        adjMatrixBool = addEdge(adjMatrixBool,unit,requisiteList[0],weight)
      else:
        for requisite in requisiteList:
          #print("Adding Edge ",unit,"",requisiteList[0],"",weight)
          adjMatrixBool = addOrEdge(adjMatrixBool,unit,requisite,weight)
    
    elif andCounter == 0 and orCounter == 0:
      for requisite in requisiteList:
        #print("Adding Edge ",unit,"",requisiteList[0],"",weight)
        adjMatrixBool = addEdge(adjMatrixBool,unit,requisite,weight) 
    
    return adjMatrixBool
   
def addCreditPointEdges(adjMatrixCredit,unit,wordTags,weight):

  above = False #
  unitSubject = ""#holds the subject code required for units to count for the credit point e.g. engg
  creditWeight = 1 #number of credit points required e.g. 10cp = 1
  unitYear = ""
  
  for word in wordTags: # loop through each requirements words
    if word[1] == 'creditPoints':
      creditWeight = 10/(int(re.findall(r'\d+',word[0])[0])) # 10/number of credit points required
    if word[1] == 'unitYear': 
      unitYear = (re.findall(r'\d',word[0]))[0] #year of required units
    if word[1] == 'inequal':
      above = True #if or above is present
    if word[1] == 'subjectArea':
      unitSubject = word[0] #if units from a certain area are required
    
  
  my_regex = r"[0-9]{3}" #checks for 000 or 131 or etc.
  plus = ""
  
  if unitYear != "": #if the unit year is required in the credit point
    plus = "(" + unitYear + ")" #makes the current plus equal to (unitYear)[0-9]{3}
    
  else:
    plus = "[0-9]" #makes the current plus equal to [0-9]{4}
    
  if above == True and unitYear != "": #include units higher than the given year
    plus = "[" + unitYear + "-9]"
  
  if unitSubject != "":
    plus = "(" + unitSubject + ")" + plus #place the subject/facult of the unit

  my_regex = plus + my_regex #regex to determine which units within the matrix are part of this
  #print("This is the credit point regex : ",my_regex)
      
  for row in adjMatrixCredit:
    if row[0] == "" or row[0] == unit or "#" in row[0] or "!" in row[0]:
      pass
    else:
      if len(re.findall(my_regex,row[0])) != 0: #if there is a regex match
        adjMatrixCredit = addCreditPointNode(adjMatrixCredit,unit,row[0],weight,creditWeight)
  
  return adjMatrixCredit
   
def addNode(adj_matrix: list, new_node):
  #print("Adding Node")  

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
 
def addOrEdge(adj_matrixOrEdge,sourceNode,endNode,weight): #to do
  
  #print("Adding OR edge")
  newNode = sourceNode + "#"
  
  if sourceNode not in adj_matrixOrEdge:
    return adj_matrixOrEdge
  
  if endNode not in adj_matrixOrEdge:
    return adj_matrixOrEdge
  
  
  while newNode in adj_matrixOrEdge:
    newNode = newNode + "1"
    
  if newNode not in adj_matrixOrEdge:
    ##print("Here")
    adj_matrixOrEdge = addEdge(adj_matrixOrEdge,sourceNode,newNode,weight)
  
  adj_matrixOrEdge = addEdge(adj_matrixOrEdge,newNode,endNode,1)
    
  return adj_matrixOrEdge

def addCreditPointNode(adjMatrixCreditNode,sourceNode,endNode,weight,creditWeight): #to do
  
  #print("Adding Credit edge node")
  newNode = sourceNode + "!"
  
  if newNode not in adjMatrixCreditNode:
    #print("Here")
    adjMatrixCreditNode = addEdge(adjMatrixCreditNode,sourceNode,newNode,weight) #adds credit point node if it does not already exist
  
  adjMatrixCreditNode = addEdge(adjMatrixCreditNode,newNode,endNode,creditWeight)#adds the edge from the credit point node to the end node
    
  return adjMatrixCreditNode
  
def addEdge(adjMatrixEdge, sourceNode, endNode, weight):

  if sourceNode not in adjMatrixEdge[0]:
    pass
    #print("No a relevant unit ", sourceNode)
  if endNode not in adjMatrixEdge[0]:
    if "!" in endNode or "#" in endNode:
      adjMatrixEdge = addNode(adjMatrixEdge,endNode)
    
  
  
  ##print("Adding_edge")
  if adjMatrixEdge is None:
    ##print("The fuck")
    adjMatrixEdge = addNode(adjMatrixEdge, None)

  srcIndex = np.where(adjMatrixEdge[0]==sourceNode)
  ##print(adj_matrix[0])

  destIndex = np.where(adjMatrixEdge[0]==endNode)
  
  if len(srcIndex[0]) == 0 or len(destIndex[0]) == 0 : #if one of the nodes does not exist
    return adjMatrixEdge

  if weight < float(adjMatrixEdge[destIndex[0],srcIndex[0]]):#if there is a higher weight already connecting the 2 nodes
    return adjMatrixEdge
  
  adjMatrixEdge[destIndex[0],srcIndex[0]] = weight #assign a weight/edge between dest and src
  #print("Adding_edge")
  
  return adjMatrixEdge

def findWeight(wordTags,startIndex,stopIndex): 
  
    leftDict = leftAndSearch(wordTags,startIndex)
    rightDict = rightAndSearch(wordTags,stopIndex)

    weightDict = rightDict
    
    for height,value in leftDict.items():
        if height not in weightDict.keys():
            weightDict[height] = value
        else:
            weightDict[height] = weightDict[height] + value
    weight = 1
    for value in weightDict.values():
        weight = weight/(value+1)
    
    return weight
    
def leftAndSearch(wordTags,startIndex):
    tempDict = {}
    height = 0
    andCounter = 0 
    skip = False
    skipQuantity = 0
    if startIndex == 0:
      return tempDict
    for uselessIndex,word in enumerate(reversed(wordTags[:startIndex-1])):
        if skip == True: 
            if word[1] == "rbracket":
                skipQuantity = skipQuantity + 1
                continue
            if word[1] == "lbracket" and skipQuantity == 0:
                skip = False
                continue
            if word[1] == "lbracket" and skipQuantity != 0:
                skipQuantity = skipQuantity - 1
                continue
            continue
        if word[1] == "bool":
            if word[0] == "and":
                andCounter = andCounter + 1
        if word[1] == "rbracket":
            skip = True
        if word[1] == "lbracket":
            tempDict[height] = andCounter
            height = height + 1
            andCounter = 0
    if andCounter != 0:
        tempDict[height] = andCounter
    return tempDict

def rightAndSearch(wordTags,stopIndex):
    tempDict = {}
    height = 0
    andCounter = 0 
    skip = False
    skipQuantity = 0
    for index,word in enumerate(wordTags[stopIndex+1:]):
        if skip == True: 
            if word[1] == "lbracket":
                skipQuantity = skipQuantity + 1
                continue
            if word[1] == "rbracket" and skipQuantity == 0:
                skip = False
                continue
            if word[1] == "rbracket" and skipQuantity != 0:
                skipQuantity = skipQuantity - 1
                continue
            continue
        if word[1] == "bool":
            if word[0] == "and":
                andCounter = andCounter + 1
        if word[1] == "lbracket":
            skip = True
        if word[1] == "rbracket":
            tempDict[height] = andCounter
            height = height + 1
            andCounter = 0
    if andCounter != 0:
        tempDict[height] = andCounter
        
    return tempDict          

def parse_statement(adjMatrixParse,unit,statement): 
    if unit == "MTRN3026":
      words1 = "MTRN2060"
      wordTag1 = requirement_word_tag(words1)
      requirementTag1 = requirement_tag(wordTag1)
      words2 = "130cp at 1000 level or above"
      wordTag2 = requirement_word_tag(words2)
      requirementTag2 = requirement_tag(wordTag2)
      adjMatrixParse = addRequirementEdges(adjMatrixParse,unit,wordTag1,requirementTag1,0.5)
      adjMatrixParse = addRequirementEdges(adjMatrixParse,unit,wordTag2,requirementTag2,0.5)
      return adjMatrixParse
    if unit == "MECH3001":
      words1 = "MECH2002 or MECH202"
      wordTag1 = requirement_word_tag(words1)
      requirementTag1 = requirement_tag(wordTag1)
      words2 = "20cp at 2000 level or above"
      wordTag2 = requirement_word_tag(words2)
      requirementTag2 = requirement_tag(wordTag2)
      adjMatrixParse = addRequirementEdges(adjMatrixParse,unit,wordTag1,requirementTag1,0.5)
      adjMatrixParse = addRequirementEdges(adjMatrixParse,unit,wordTag2,requirementTag2,0.5)
      return adjMatrixParse
    if unit == "AHIS3000":
      words1 = "130cp at 1000 level or above"
      wordTag1 = requirement_word_tag(words1)
      requirementTag1 = requirement_tag(wordTag1)
      words2 = "40cp from AHIS2130 or or AHIS2210 or AHIS2211 or AHIS2225 or AHIS2250 or AHIS2251 or AHIS2301 or AHIS2302"
      wordTag2 = requirement_word_tag(words2)
      requirementTag2 = requirement_tag(wordTag2)
      adjMatrixParse = addRequirementEdges(adjMatrixParse,unit,wordTag1,requirementTag1,1)
      adjMatrixParse = addRequirementEdges(adjMatrixParse,unit,wordTag2,requirementTag2,1)
      return adjMatrixParse
    lbracketIndex = -1
    rbracketIndex = False
    for index,word in enumerate(statement):
        if word[1] == "lbracket" or word[1] == "rbracket":
            if len(statement[lbracketIndex+1:index]) != 0:
              
              rbracketIndex = True
              ##print("These words used to call function, : ",statement[lbracketIndex+1:index])
              ##print(findWeight(statement,lbracketIndex+1,index))
              wordTags = statement[lbracketIndex+1:index]
              weight = findWeight(statement,lbracketIndex+1,index)
              requirementTag = requirement_tag(wordTags)
              #maybe somehow check if I should be added an or edge or not????
              #maybe check fi unit is a fake credity point, i might need to change this somehow if that is the case
              adjMatrixParse = addRequirementEdges(adjMatrixParse,unit,wordTags,requirementTag,weight)
              ##print(adjMatrix)
            lbracketIndex = index
        if word[0] == "including":
          wordTags = statement[lbracketIndex+1:index]
          requirementTag = requirement_tag(wordTags)
          #maybe somehow check if I should be added an or edge or not????
          #maybe check fi unit is a fake credity point, i might need to change this somehow if that is the case
          adjMatrixParse = addRequirementEdges(adjMatrixParse,unit,wordTags,requirementTag)
          break
    if lbracketIndex == -1 and rbracketIndex == False:
      weight = 1
      requirementTag = requirement_tag(statement)
      adjMatrixParse = addRequirementEdges(adjMatrixParse,unit,statement,requirementTag,weight)
              
    return adjMatrixParse