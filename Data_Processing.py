import pandas as pd

def dataRead(unitRequirements, unitSessions):
    rawRequirementData = pd.read_csv(unitRequirements)
    RequirementData = rawRequirementData.drop(columns=['Title', 'Version Number', 'Type', 'Status', 'Academic Org', 'Owning Faculty'])

    rawSessionData = pd.read_csv(unitSessions)
    SessionData = rawSessionData.drop(columns=['Title', 'Version Number', 'Status', 'Owning Faculty', 'Academic Org', 'Display Name', 'Attendance Mode', 'Quota Number', 'Location'])
    
    # Getting rid of garbage requirement types
    RequirementData = RequirementData[~RequirementData['Type.1'].isin(["NCCW (pre-2020 units)", "Info"])] #remove this because I might need the session time for some of the units
    RequirementData = RequirementData.sort_values('Academic Item')
    
    SessionData = SessionData[SessionData['Teaching Period'].isin(["Session 1", "Session 2"])]
    SessionData = SessionData.sort_values('Academic Item')

    # Merging the requirement and session data
    merged_data = pd.merge(RequirementData, SessionData, on="Academic Item", how="left")
    merged_data['Session 1'] = merged_data['Teaching Period'] == 'Session 1'
    merged_data['Session 2'] = merged_data['Teaching Period'] == 'Session 2'
    merged_data.drop(columns=['Teaching Period'], inplace=True)
    
    merged_data.drop_duplicates(inplace=True)
       
    
    grouped = merged_data.groupby(['Academic Item', 'Type.1', 'Description'])
    
    def merge_rows(group):

        merged_row = group.iloc[0]

        merged_row['Session 1'] = group['Session 1'].max()
        merged_row['Session 2'] = group['Session 2'].max()
        

        Corequisites = []
        Prerequisites = []

        for index, row in group.iterrows():
            if row['Type.1'] == 'Co-requisite':
                Corequisites.append(row['Description'])
            elif row['Type.1'] == 'Pre-requisite':
                Prerequisites.append(row['Description'])
                
        merged_row['Co-requisite'] = ', '.join(Corequisites)
        merged_row['Pre-requisite'] = ', '.join(Prerequisites)
            
        return merged_row

    merged_data = grouped.apply(merge_rows).reset_index(drop=True)
    
    merged_data.drop(columns=['Type.1','Description'], inplace=True)
    
    merged_data = merged_data.sort_values('Academic Item')
    
    
    temp = None
    for index, row in merged_data.iterrows():
        if temp is None:
            pass
        elif temp['Academic Item'] == row['Academic Item']:
            if row['Pre-requisite'] == "":
                merged_data.at[index,'Pre-requisite'] = temp['Pre-requisite']
                merged_data.drop(index, inplace=True)
            if row['Co-requisite'] == "":
                #print(row['Co-requisite']," Co ",temp['Co-requisite'], " Req")
                merged_data.at[index,'Co-requisite'] = temp['Co-requisite']
                merged_data.drop(index-1, inplace=True)
        temp = row

    for index,row in merged_data.iterrows():
        if row['Session 1'] == False and row['Session 2'] == False:
            #print("here")
            merged_data.drop(index,inplace=True)    
    
     
    
    return merged_data

unitRequirements_file = 'unitRequirements.csv'
unitSessions_file = 'unitSessionOfferings.csv'
result = dataRead(unitRequirements_file, unitSessions_file)
#for index, row in result.iterrows():

#    if row['Pre-requisite'] != "" and row['Co-requisite'] != "":
#        print(row['Pre-requisite'], " Hello ",row['Co-requisite'])
#print(result)
#result.to_csv("matrix.csv")