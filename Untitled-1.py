for word,wordTag in wordTags.items(): # loop through each requirements words
      if wordTag == 'creditPoints':
        weight = 10/(int(re.findall(r'\d+',word)[0])) # 10/number of credit points required
      if wordTag == 'unitYear': 
        unitYear = (re.findall(r'\d',word))[0]
      if wordTag == 'inequal':
        above = True
      if wordTag == 'subjectArea':
        unitSubject = word
    for index,row in data.iterrows():
      my_regex = re.escape(unitYear) + r"[0-9]{3}"
      print("My Regex: ",my_regex)
      print(row['Academic Item'])
      
      if re.findall(my_regex,row['Academic Item']) != None:
        print("This matched")
        print(re.findall(my_regex,row['Academic Item']))
        if Pre == False:
          weight = weight * -1
        addEdge(adjMatrix,unit, row['Academic Item'],weight)