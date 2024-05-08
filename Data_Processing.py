import pandas as pd
import math

def dataRead(unitRequirements, unitSessions):
    rawRequirementData = pd.read_csv(unitRequirements)
    RequirementData = rawRequirementData.drop(columns=['Title', 'Version Number', 'Type', 'Status', 'Academic Org', 'Owning Faculty'])

    rawSessionData = pd.read_csv(unitSessions)
    SessionData = rawSessionData.drop(columns=['Title', 'Version Number', 'Status', 'Owning Faculty', 'Academic Org', 'Display Name', 'Attendance Mode', 'Quota Number', 'Location'])
    
    #remove this one for bin packing, need all of the units sessions not just the ones with pre and co-requisites
    RequirementData = RequirementData[~RequirementData['Type.1'].isin(["NCCW (pre-2020 units)"])]
    RequirementData = RequirementData[~RequirementData['Type.1'].isin(["Info"])]

    
    RequirementData = RequirementData.sort_values('Academic Item')
    
    SessionData = SessionData[SessionData['Teaching Period'].isin(["Session 1", "Session 2"])]
    SessionData = SessionData.sort_values('Academic Item')


    # Merging the requirement and session data
    #merged_data = pd.merge(RequirementData, SessionData, on="Academic Item", how="left")
    merged_data = pd.merge(SessionData, RequirementData, on="Academic Item", how="left")

    merged_data['Session 1'] = merged_data['Teaching Period'] == 'Session 1'
    merged_data['Session 2'] = merged_data['Teaching Period'] == 'Session 2'
    merged_data.drop(columns=['Teaching Period'], inplace=True)
    
    merged_data.drop_duplicates(inplace=True)
    
    merged_data.reset_index # reset the index so that I can reference in the future

    for index,row in merged_data.iterrows():

        if pd.isnull(row['Type.1']) == True:
            merged_data.loc[index,'Type.1'] = "Empty"
            merged_data.loc[index,'Description'] = "Empty"

        """_summary_

        Returns:
            _type_: _description_
        
    for index,row in merged_data.iterrows():
        if row['Academic Item'] == "ENGG1000":
            print(row)
            
    for index,row in merged_data.iterrows():
        if row['Academic Item'] == "ENGG1050":
            print(row)
    
        """
    grouped = merged_data.groupby(['Academic Item', 'Type.1', 'Description'])

            
    def merge_rows(group):

        merged_row = group.iloc[0]

        merged_row['Session 1'] = group['Session 1'].max()
        merged_row['Session 2'] = group['Session 2'].max()
                    
        Corequisites = []
        Prerequisites = []
        present = False
        
        for index, row in group.iterrows():
            
            if row['Type.1'] == 'Co-requisite':
                
                for item in Corequisites:
                    present = False
                    if row['Description'] == item:
                        present = True
                if present == False:
                    Corequisites.append(row['Description'])
            elif row['Type.1'] == 'Pre-requisite':        
                for item in Prerequisites:
                    present = False
                    if row['Description'] == item:
                        present = True
                if present == False:
                    Prerequisites.append(row['Description'])
                
                
        
            merged_row['Co-requisite'] = ', '.join(Corequisites)
            merged_row['Pre-requisite'] = ', '.join(Prerequisites)
            
        return merged_row




    merged_data = grouped.apply(merge_rows).reset_index(drop=True)
    
    #print(merged_data)

    
    merged_data = merged_data.sort_values('Academic Item')
    
    temp = None
    rows_to_drop = []  # Collect indices of rows to drop
    for index, row in enumerate(merged_data.itertuples()):
        #print(row)
        if temp is not None and temp._1 == row._1: #if temp has not been assigned yet and temp aca
            if row._2 == "Empty":
                rows_to_drop.append(index)
            if row._7 == "" or row._2 == "Empty":
                merged_data.at[index,'Pre-requisite'] = temp._7 # change

            if row._6 == "" or row._2 == "Empty":
                merged_data.at[index,'Co-requisite'] = temp._6 # change
                rows_to_drop.append(index - 1)
        temp = row


    
    
    #print(len(merged_data))
    #print(rows_to_drop)
    merged_data.drop(index=rows_to_drop, inplace=True)
    #print(len(merged_data))
    
    """
    for index, row in merged_data.iterrows():
        if "COMP1000" in row['Academic Item'] or "ENGG1000" in row['Academic Item']:
            print(row['Academic Item'])
            print(row['Type.1'])
            print(row['Description'])
            print(row['Session 1'])
            print(row['Session 2'])
    """
    rows_to_drop = []
    for index,row in merged_data.iterrows():
        if row['Session 1'] == False and row['Session 2'] == False:
            #print("here")
            rows_to_drop.append(index)
    
    merged_data.drop(index=rows_to_drop, inplace=True)
    
    merged_data.drop(columns=['Type.1','Description'], inplace=True) 
    
    merged_data = merged_data.sort_values('Academic Item')
    
    merged_data.reset_index
    
    return merged_data

unitRequirements_file = 'unitRequirements.csv'
unitSessions_file = 'unitSessionOfferings.csv'
result = dataRead(unitRequirements_file, unitSessions_file)
print(result)
#for index, row in result.iterrows():
#    if row['Pre-requisite'] == "" or row['Co-requisite'] == "":
#       print(row['Pre-requisite'], " Hello ",row['Co-requisite'])
#print(result)
result.to_csv("matrix.csv")