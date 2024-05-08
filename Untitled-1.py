    for index, row in merged_data.iterrows():
        if "COMP1000" in row['Academic Item'] or "ENGG1000" in row['Academic Item']:
            print(row['Academic Item'])
            print(row['Type.1'])
            print(row['Description'])
            print(row['Session 1'])
            print(row['Session 2'])