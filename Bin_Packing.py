import numpy as np

def binPacking(preReqAdjMatrix,coReqAdjMatrix, data,desiredUnits):
  
  result = []
  currentSession = 1
  completedUnits = [] #list of completed/scheduled units
  
  coReqs = generateCoReqs(coReqAdjMatrix)
  
  while True:
  
    
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
      #print("Here")
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
    
    takeableUnits = []
    for unit in takeablePreUnits:
      if unit in takeableCoUnits:
        #print("Doing this")
        takeableUnits.append(unit)
        
    if len(takeableUnits) == 0:
      pass
      #print("Why is this empty" , takeablePreUnits)
      #print(takeableCoUnits)

    sortedUnits = sortUnits(preReqAdjMatrix,coReqAdjMatrix,takeableUnits,desiredUnits,data)
    
    
  
    availableUnits = availability(data,sortedUnits,currentSession)
    
    if len(availableUnits) == 0:
      #print("No units can be done")
      break
    
   
    
    elif len(coReqs) != 0:
      #print("Before ",availableUnits)
      for unit in coReqs: #unit is a unitcode of the unit who's coreqs im a currently checking
        if unit[0][0] not in completedUnits and unit[0][0] not in takeableUnits: #unit is not already completed and unit is not already takeable
          #check if unit is available in current session and calculate the dep length of this unit
          for avail in availableUnits[:3]: #change this if I have time to a more dynamic version aka if a unit is that this unit depends on 
            if avail in unit: #if avail unit is a coreq of unit
              if len(unit) == 2: #add functionality for more than 1 co-req later, this code only works for 1 simultaneous unit
                #check the dependency length of the unit to check if this unit is worth scheduling
                depLength = 0
                for row in preReqAdjMatrix:
                  if row[0] == unit[0][0]:
                    depLength = unitDependencyLength(preReqAdjMatrix,row[0])
                  if row[0] == avail:
                    oldUnitLength = unitDependencyLength(preReqAdjMatrix,row[0])
                temp = 0
                for row in coReqAdjMatrix:
                  if row[0] == unit[0][0]:
                    temp = unitDependencyLength(coReqAdjMatrix,row[0])
                  if row[0] == avail:
                    tempOldUnitLength = unitDependencyLength(coReqAdjMatrix,row[0])
                if temp>depLength:
                    depLength=temp
                if tempOldUnitLength > oldUnitLength:
                  oldUnitLength = tempOldUnitLength
                
                
                available = False
                
                if depLength > oldUnitLength:
                  for index,row in data.iterrows():
                    #print("The unit is : ",unit)
                    #print("The row is : ",row)
                    if unit[0][0] in row['Academic Item']:
                      if currentSession % 2 == 1:
                        if row['Session 1'] == True: #check this is string and not boolean
                          available = True
                      if currentSession % 2 == 0:
                        if row['Session 2'] == True:
                          available = True
              
                if available == True:
                  #print("wtf")
                  availableUnits.insert(4,unit[0][0])

          
      #print("After ", availableUnits)
      #return availableUnits
      
    #print("Available units is equal to: ",availableUnits)
    
    
    noAvail = []
    
    for units in desiredUnits:
      if units not in availableUnits and units not in completedUnits:
        noAvail.append(units)
    
    
    #print("Not Available units is equal to: ",noAvail)
    
    scheduledUnits = []
    
    
    
    
    for index,unit in enumerate(availableUnits):
      #print("Available unit is : ", unit)
      if index >= 4:
        break
      completedUnits.append(unit)
      #print("scheduled: ", unit)
      #print("Takeableunits is: ",availableUnits)
      scheduledUnits.append(unit)
      
    result = f"{result} Chosen units for Session {currentSession} is : {scheduledUnits}\n"
    
    currentSession = currentSession + 1
  
  notScheduled = []
  for units in desiredUnits:
    if units not in completedUnits:
      notScheduled.append(units)
      
  result = f"{result} The not completed units are: \n{notScheduled}\n"
  return result    

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

def generateCoReqs(coReqAdjMatrix):
  result = []
  for column in range(1,len(coReqAdjMatrix)):
    coReqEdges = []
    for index,row in enumerate(coReqAdjMatrix):
      if row[column] != "0" and index != 0: #matrix[0][column] has a co req of row[0]
        #print("here")
        coReqEdges.append((row[0],float(row[column])))
    if len(coReqEdges) != 0: #if unit has a co-req
      #print(coReqEdges)
      #print(type(coReqEdges))
      unitCombinations = find_combinations(coReqEdges,1)
      unitCombinations.insert(0,coReqAdjMatrix[0][column])
      result.append(unitCombinations)
        
  return result



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
            if unit in availableUnits:
              pass
              #print("Fixing Stuff")
            else:
              availableUnits.append(unit)
        if currentSession % 2 == 0:
          if row['Session 2'] == True:
            if unit in availableUnits:
              pass
              #print("Fixing Stuff")
            else:
              availableUnits.append(unit)
  return availableUnits

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
          
def sortUnits(preReqAdjMatrix,coReqAdjMatrix,takeableUnits,desiredUnits,data):

  #trial and error must do here
  
  depSort = dependencyLengthGeneration(preReqAdjMatrix,coReqAdjMatrix,takeableUnits,desiredUnits)

  sesSort = sessionSort(depSort,data)

  return sesSort

def dependencyLengthGeneration(preReqAdjMatrix,coReqAdjMatrix,takeableUnits,desiredUnits):
  depDict = {}
  #print("Takeable Units is: ",takeableUnits)
  for unit in preReqAdjMatrix:
    if "#" not in unit[0] and "!" not in unit[0] and unit[0] != "" :
      if unit[0] in takeableUnits:
        if unit[0] in desiredUnits:
          higher = unitDependencyLength(preReqAdjMatrix,unit[0])
          temp = unitDependencyLength(coReqAdjMatrix,unit[0])
          if temp > higher:
            higher = temp
          depDict[unit[0]] = higher
  
  depDict = sorted(depDict.items(), key=lambda x:x[1], reverse=True)
  depDict = dict(depDict)
  #print(depDict)
  return depDict
 
def unitDependencyLength(adjMatrix, unit):
  highest = 0
  temp = 0
  unitRow = []
  for matrixRow in adjMatrix:
    if unit in matrixRow[0]:
      unitRow = matrixRow
      break
  
  for index,column in enumerate(unitRow):
    if column.isnumeric(): #if the column is an edge column and not a unit name
      if column != "0": #if the column contains an edge
        newUnit = adjMatrix[index][0] #should make the new unit row the appropriate row
        #print(newUnitRow)
        if "#" in unitRow[0] or "!" in unitRow[0]: # if unitcode is an OR node or a Credit Point node do not add 1 to the length as these are fake/dummy units
          return unitDependencyLength(adjMatrix,newUnit)
        temp = 1 + unitDependencyLength(adjMatrix,newUnit) #assign a variable to the edges dependency length
        if temp>highest: #if this units dep len is higher than the current highest
          highest = temp #make unit dep len the highest
  #for each units edge (any edge that leaves the unit)
  #check the dependency length of that unit and if it is higher than the current highest dependency length
  return highest