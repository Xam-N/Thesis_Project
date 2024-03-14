import pandas as pd
#unitRequirements.csv
#unitSessionOfferings.csv
def dataRead(unitRequirements, unitSessions):
  rawRequirementData = pd.read_csv(unitRequirements)
  #print(rawRequirementData.columns)
  RequirementData = rawRequirementData.drop(columns=['Title','Version Number','Type','Status','Academic Org', 'Owning Faculty'])
  #print(rawRequirementData.columns)
  rawSessionData = pd.read_csv(unitSessions)
  #print(rawSessionData.columns)
  SessionData = rawSessionData.drop(columns=['Title','Version Number','Status','Owning Faculty','Academic Org','Display Name', 'Attendance Mode', 'Quota Number', 'Location'])
  #rawRequirementData = rawRequirementData.drop(rawRequirementData['Type.1'] == 'NCCW (pre-2020 units)')
  RequirementData = RequirementData.drop(RequirementData[RequirementData['Type.1'] == "NCCW (pre-2020 units)"].index)
  RequirementData = RequirementData.drop(RequirementData[RequirementData['Type.1'] == "Info"].index)
  RequirementData = RequirementData.sort_values('Academic Item')
  SessionData = SessionData.drop(SessionData[(SessionData['Teaching Period'] != "Session 1") & (SessionData['Teaching Period'] != "Session 2")].index)
  SessionData = SessionData.sort_values('Academic Item')
  for session in SessionData:
    
  
  
  
  
  for unit in RequirementData:
    for session in SessionData:
      if unit['Academic Item'] == session['Academic Item']:
        if session['Teaching Period'] == 'Session 1':
          unit['Session 1'] == True
          SessionData.drop(session)
        if session['Teaching Period'] == 'Session 2':
          unit['Session 2'] == True
      
  
  #print(RequirementData)
  #print(SessionData)
  return RequirementData
  #Test = pd.merge(RequirementData, SessionData, on="Academic Item", how="right")
  #Test["Session 1"] = " "
  #Test["Session 2"] = " "
  #print(Test) 

  """
  for index, row in Test.iterrows():
    if(row['Teaching Period'] == "Session 1"):
      row['Session 1'] = True
      row['Session 2'] = False
    if(row['Teaching Period'] == "Session 2"):
      row['Session 2'] = True
      row['Session 1'] = False
  """


  #print(rawSessionData.columns)
  #print(rawRequirementData)
  #print(rawSessionData)
  #nd SessionData[SessionData['Teaching Period'] != "Session 2"]