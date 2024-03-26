import pandas as pd

def dataRead(unitRequirements, unitSessions):
    rawRequirementData = pd.read_csv(unitRequirements)
    RequirementData = rawRequirementData.drop(columns=['Title', 'Version Number', 'Type', 'Status', 'Academic Org', 'Owning Faculty'])

    rawSessionData = pd.read_csv(unitSessions)
    SessionData = rawSessionData.drop(columns=['Title', 'Version Number', 'Status', 'Owning Faculty', 'Academic Org', 'Display Name', 'Attendance Mode', 'Quota Number', 'Location'])
    
    # Getting rid of garbage requirement types
    RequirementData = RequirementData[~RequirementData['Type.1'].isin(["NCCW (pre-2020 units)", "Info"])]
    RequirementData = RequirementData.sort_values('Academic Item')
    
    SessionData = SessionData[SessionData['Teaching Period'].isin(["Session 1", "Session 2"])]
    SessionData = SessionData.sort_values('Academic Item')

    # Merging the requirement and session data
    merged_data = pd.merge(RequirementData, SessionData, on="Academic Item", how="left")
    merged_data['Session 1'] = merged_data['Teaching Period'] == 'Session 1'
    merged_data['Session 2'] = merged_data['Teaching Period'] == 'Session 2'
    merged_data.drop(columns=['Teaching Period'], inplace=True)

    return merged_data

# Example usage:
unitRequirements_file = 'unitRequirements.csv'
unitSessions_file = 'unitSessionOfferings.csv'
result = dataRead(unitRequirements_file, unitSessions_file)
print(result)