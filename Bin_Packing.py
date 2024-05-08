import numpy as np

def binPacking(preReqAdjMatrix,coReqAdjMatrix, data,desiredUnits):
  
  result = []
  currentSession = 1
  completedUnits = [] #list of completed/scheduled units
  
  while True:
    
    print("Starting")
    
    while True:
      takeablePreUnits = findTakeablePreUnits(preReqAdjMatrix,completedUnits)[0]
      fakePreUnits = findTakeablePreUnits(preReqAdjMatrix,completedUnits)[1]
      notTakeablePreUnits = findTakeablePreUnits(preReqAdjMatrix,completedUnits)[2]
      if len(fakePreUnits) != 0: #if this list contains bad units
        counter = 0
        for unit in fakePreUnits:
          if unit not in completedUnits:
            counter = counter + 1
            completedUnits.append(unit)
        if counter == 0:
          break
      else:
        break
      
    while True:
      takeableCoUnits = findTakeablePreUnits(coReqAdjMatrix,completedUnits)[0]
      fakeCoUnits = findTakeablePreUnits(coReqAdjMatrix,completedUnits)[1]
      notTakeableCoUnits = findTakeablePreUnits(coReqAdjMatrix,completedUnits)[2]
      if len(fakeCoUnits) != 0: #if this list contains bad units
        counter = 0
        for unit in fakeCoUnits:
          temp = unit + "&"
          if temp not in completedUnits:
            counter = counter + 1
            completedUnits.append(temp)
        if counter == 0:
          break
      else:
        break
    
    
    possibleCo = generateCoReqs(coReqAdjMatrix,takeablePreUnits,notTakeablePreUnits, takeableCoUnits, notTakeableCoUnits,completedUnits)
    print("This is the important Shit \n",possibleCo)
                
    #print("Completed units is equal to: ",completedUnits)
    
    #print("Takeable units is equal to: ",takeablePreUnits)
    
    if len(takeablePreUnits) == 0:
      break

    sortedUnits = sortUnits(preReqAdjMatrix,coReqAdjMatrix,takeablePreUnits,desiredUnits,data,possibleCo)
  
    #print("Sorted units is equal to: ",sortedUnits)
  
    availableUnits = availability(data,sortedUnits,currentSession)
    
    if len(availableUnits) == 0:
      print("No units can be done")
      break
    
    #print("Available units is equal to: ",availableUnits)
    
    
    noAvail = []
    
    for units in desiredUnits:
      if units not in availableUnits and units not in completedUnits:
        noAvail.append(units)
    
    
    #print("Not Available units is equal to: ",noAvail)
    
    completedUnit4 = []
    
    for index,unit in enumerate(availableUnits):
      #print("Available unit is : ", unit)
      if index >= 4:
        break
      completedUnits.append(unit)
      completedUnit4.append(unit)
      
    result = f"{result} Chosen units for Session {currentSession} is : {completedUnit4}\n"
    
    currentSession = currentSession + 1
  notScheduled = []
  for units in desiredUnits:
    if units not in completedUnits:
      notScheduled.append(units)
  result = f"{result} The not completed units are: \n{notScheduled}\n"
  return result    

#def checkWeirds(completedUnits):
 # for unit in 

def find_combinations(names_weights, target_sum, partial=[], start=0):
    result = []
    
    # Check if the partial sum equals the target sum
    if sum(name_weight[1] for name_weight in partial) >= target_sum:
        result.append([name_weight[0] for name_weight in partial])
    
    # Base case: If the partial sum exceeds the target sum or the list is empty, return
    if sum(name_weight[1] for name_weight in partial) >= target_sum or start == len(names_weights):
        return result
    
    # Recursively find combinations including and excluding the current name
    for i in range(start, len(names_weights)):
        name, weight = names_weights[i]
        result.extend(find_combinations(names_weights, target_sum, partial + [[name, weight]], i + 1))
    
    return result

def generateCoReqs(coReqAdjMatrix,takeablePreUnits,notTakeablePreUnits, takeableCoUnits, notTakeableCoUnits,completedUnits):
  incomingWeight = 0
  conditionalIncomingWeight = []
  for unit in notTakeableCoUnits:
    if unit not in notTakeablePreUnits:
      for column in range(1,len(coReqAdjMatrix)): #loop through each unit
        if coReqAdjMatrix[0][column] == unit:
          for row in coReqAdjMatrix:
            if row[column] != "0":
              if row[0] in completedUnits:
                incomingWeight += float(row[column])
              elif row[0] in takeablePreUnits or row[0] in takeableCoUnits:
                temp = []
                temp.append(row[0])
                temp.append(float(row[column]))
                conditionalIncomingWeight.append(temp)
          if incomingWeight >= 0.99:
            print("Why is this not already takable?")
          weightTotal = 0
          for weights in conditionalIncomingWeight:
            weightTotal = weightTotal + weights[1]
          if weightTotal + incomingWeight >= 0.99: #is it possible to do this unit this semester, yes or no
            goal = 0.99 - incomingWeight
            unitCombinations = find_combinations(conditionalIncomingWeight,goal)
            for i in range(len(unitCombinations)):
              unitCombinations[i].insert(0,coReqAdjMatrix[0][column])
            return unitCombinations #needs to return the unit too
  return None



def availability(data,takeableUnits,currentSession): #returns a list of available units from the currently takeable units
  availableUnits = []
  #print(takeableUnits)
  print(takeableUnits)
  if takeableUnits is None:
    #print("Help there is no takeable units")
    return None
  for unit in takeableUnits:
    for index,row in data.iterrows():
      #print("The unit is : ",unit)
      #print("The row is : ",row)
      if unit in row['Academic Item']:
        if currentSession % 2 == 1:
          if row['Session 1'] == True: #check this is string and not boolean
            availableUnits.append(unit)
        if currentSession % 2 == 0:
          if row['Session 2'] == True:
            availableUnits.append(unit)
  return availableUnits

#credit point and or units/nodes break this, because I need to include code to count them as completed whenever their weight goes high enough
def findTakeablePreUnits(adjMatrix, completedUnits): #need to change to work for co-req
  fakeUnits = []
  takeableUnits = [] #change this to a dictionary, unit: creditpoints
  notTakeableUnits = []
  #I can then conjoin co-requisites into a single unit maybe
  #print("Completed Units is: ",completedUnits)
  for column in range(1,len(adjMatrix)): #loop through each unit
    #print("This is the current unit : ",adjMatrix[0][column])
    incomingWeight = 0
    counter = 0 #counter of how many units have an edge going to this unit, if this is 0 then unit is immediately takeable
    if adjMatrix[0][column] in completedUnits: #dont schedule already done units
        #print("This unit has already been completed : ",adjMatrix[0][column])
        continue
    
    else:
      for index,row in enumerate(adjMatrix):
        
        if row[column] != "0" and index != 0: #if unit has edge to unit
          #print("Row[0] is : ",row[0])
          #print("here")
          counter += 1
          
          if row[0] in completedUnits: #if incoming edge originates at a completed unit
            #print("String to int check")
            incomingWeight += float(row[column])  #add weight of edge to incomingWeight
            
    #print("The number of incoming edges is: ",counter)
    #print("Incoming weight is equal to: ",incomingWeight)
    if ("#" in adjMatrix[0][column] or "!" in adjMatrix[0][column]) and (incomingWeight>=0.99 or counter == 0):
      fakeUnits.append(adjMatrix[0][column])
    elif incomingWeight >= 0.99 or counter == 0:  #if weight >=1
      #print("I am here")
      takeableUnits.append(adjMatrix[0][column]) #unit is takeable
    else:
      notTakeableUnits.append(adjMatrix[0][column])
  
  
  return takeableUnits,fakeUnits,notTakeableUnits
  
def nodeIndexFinder(adjMatrix, node):
  
  for index in range(len(adjMatrix)):
    if adjMatrix[0][index] == node:
      return index

def matrixNodeRemoval(adjMatrix,node):
  
  nodeIndex = nodeIndexFinder(adjMatrix,node)
    
  adjMatrix = np.delete(adjMatrix,nodeIndex, axis=1)
  
  return adjMatrix


def initialTopologicalSort(adjMatrix):
  
  nodeList = []
  
  for index in range(1,len(adjMatrix)):
    for rowIndex,row in enumerate(adjMatrix):
      if row[index] != 0:
        break
      elif rowIndex > len(adjMatrix)-1:
        nodeList.append(adjMatrix[0][index])
  
  return nodeList

def sessionFinder(data,unit):
  result = 0
  row = data[data['Academic Item']==unit] # should give row of unit
  #print("This prints what ",row['Academic Item'])
  if "True" in row['Session 1']:
    result -= 1
  if "True" in row['Session 2']:
    result -= 1
  return result

def sessionSort(depSort, data):
  result = []
  sortAgain = []
  highest = -1
  counter = 0
  for unit,dep in depSort.items():
    if highest == -1:
      highest = dep
      sortAgain.append(unit)
    elif highest == dep:
      sortAgain.append(unit)
    elif highest > dep or counter == len(depSort):
      sortAgain.sort(key=lambda unit: sessionFinder(data, unit))
      result += sortAgain
      sortAgain = []
      sortAgain.append(unit)
      #do something because this means that I have found all the values that are the same
    counter += 1
  
  if len(sortAgain) != 0:
    result += sortAgain
    
  return result
  
def garbage(depSort,possibleCo):
      for unit,value in depSort.items():
        for row in possibleCo:
          for column in row:
            if unit == column:
              depSort[possibleCo[0][0]] == value
              depSort = sorted(depSort.items(), key=lambda x:x[1], reverse=True)
              depSort = dict(depSort)
              return depSort
          
def sortUnits(preReqAdjMatrix,coReqAdjMatrix,takeableUnits,desiredUnits,data,possibleCo):

  #trial and error must do here
  
  depSort = dependencyLengthGeneration(preReqAdjMatrix,coReqAdjMatrix,takeableUnits,desiredUnits)
  
  if possibleCo != None and possibleCo[0][0] not in depSort:
    garbage(depSort,possibleCo)
    
  

  sesSort = sessionSort(depSort,data)

  return sesSort

def dependencyLengthGeneration(preReqAdjMatrix,coReqAdjMatrix,takeableUnits,desiredUnits):
  depDict = {}
  #print("Takeable Units is: ",takeableUnits)
  for unit in preReqAdjMatrix:
    if "#" not in unit[0] and "!" not in unit[0] and unit[0] != "" :
      if unit[0] in takeableUnits:
        if unit[0] in desiredUnits:
          higher = unitDependencyLength(preReqAdjMatrix,unit)
          temp = unitDependencyLength(coReqAdjMatrix,unit)
          if temp > higher:
            higher = temp
          depDict[unit[0]] = higher
  
  depDict = sorted(depDict.items(), key=lambda x:x[1], reverse=True)
  depDict = dict(depDict)
  #print(depDict)
  return depDict
  
  
def unitDependencyLength(adjMatrix, unitRow):
  highest = 0
  temp = 0
  for index,column in enumerate(unitRow):
    if column.isnumeric(): #if the column is an edge column and not a unit name
      if column != "0": #if the column contains an edge
        newUnitRow = adjMatrix[index] #should make the new unit row the appropriate row
        #print(newUnitRow)
        if "?" in unitRow[0] or "!" in unitRow[0]: # if unitcode is an OR node or a Credit Point node do not add 1 to the length as these are fake/dummy units
          return unitDependencyLength(adjMatrix,newUnitRow)
        temp = 1 + unitDependencyLength(adjMatrix,newUnitRow) #assign a variable to the edges dependency length
        if temp>highest: #if this units dep len is higher than the current highest
          highest = temp #make unit dep len the highest
  #for each units edge (any edge that leaves the unit)
  #check the dependency length of that unit and if it is higher than the current highest dependency length
  return highest

def testing(inputMatrix):
   
  adjMatrix = [["","A","B","C","D!","D" ],["A","0","1","1","1","0"],["B","0","0","1","1","0"],["C","0","0","0","1","0"],["D!","0","0","0","0","1"],["D","0","0","0","0","0"]]
  #SHOULD RETURN 2
  
  #print(unitDependencyLength(adjMatrix,adjMatrix[1]))
  #print(dependencyLengthGeneration(inputMatrix))

#testing()