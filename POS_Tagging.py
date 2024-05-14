import re

sample = {
  "sample 1": "COMP3100 - something else ",
  "sample 2": "COMP1000 - ENGG1000 ",
  "sample 3":"COMP3100 and COMP1000",
  "sample 4":"COMP3100 or COMP1000 ",
  "sample 5":"20cp from 3000 level units and ENGG1000 or ENGG1050",
  "sample 6":"30cp at 1000 level or above ",
  "sample 7": "(COMP3100 or COMP3000) and (ENGG3000 or ENGG3050)",
  "sample 8": "(COMP3100 or COMP3000) and (20cp from 3000 level units)",
  "sample 9": "COMP3100 or COMP310",
  "sample 10": "DUPL1000 or DUPL1000",
  "sample 11": "COMP3100",
  "sample 12": "10cp from (MATH132-MATH136 or DMTH137 or MATH1007-MATH1025 or (STAT150 or STAT1250) or (STAT170 or STAT1170) or (STAT171 or STAT1371) or (STAT175 or STAT1175))",
  "sample 13": "HSC Mathematics Advanced Band 4 and above or Extension 1 Band E2 and above or Extension 2 Band E2 and above ",
  "sample 14":"30cp at 1000 level including COMP1000 "
}


custom_tags = {
  "unitCode": r"[A-Z]{4}[0-9]{4}",
  "dash": r"-",
  "unitYear": r"[0-9]{4}",  # Changed the pattern to match any 4-digit number
  "level": r"level",      # Changed the pattern to match any 4-digit number
  "bool": r"or|and|include|,including",
  "inequal": r"above",
  "creditPoints": r"[0-9]{2}[0-9]*cp",
  "unitField": r" [a-zA-Z]{4} ",
  "lbracket": r"\(",
  "rbracket": r"\)",  
  #"pre2020": r"[A-Z]{4}[0-9]{3}",
}


#maybe if an OR is found, check to see if the next word in ABOVE, if so remove the OR

#returns a tagged requirement given
def requirement_word_tag(data): #when given a string, works perfectly
  words = re.findall(r'\(|\)|\w+', data)
  word_types = []
  for index,word in enumerate(words):
      matched = None
      for type_label, pattern in custom_tags.items():
        if(word) == "or":
          if len(words) > index+1:
            if words[index+1] == "above":
              break 
        if re.match(pattern, word):
          matched = type_label
          break
      if matched != None:
        word_types.append([word,matched])
  return word_types


for sampleName ,sampleRequirement in sample.items():
  hey = requirement_word_tag(sampleRequirement)
  print(requirement_word_tag(sampleRequirement))