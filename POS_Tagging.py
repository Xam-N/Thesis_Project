import re

sample = {
  "sample 1": "COMP3100 - something else ",
  "sample 2": "COMP1000 - ENGG1000 ",
  "sample 3":"COMP3100 and COMP1000",
  "sample 4":"COMP3100 or COMP1000 ",
  "sample 5":"20cp from 3000 level units ",
  "sample 6":"30cp at 1000 level or above ",
  "sample 7": "(COMP3100 or COMP3000) and (ENGG3000 or ENGG3050)",
  "sample 8": "(COMP3100 or COMP3000) and (20cp from 3000 level units)",
  "sample 9": "COMP3100 or COMP310",
  "sample 10": "DUPL1000 or DUPL1000"
}



custom_tags = {
  "unitCode": r"[A-Z]{4}[0-9]{4}",
  "dash": r"-",
  "unitYear": r"[0-9]{4}",  # Changed the pattern to match any 4-digit number
  "level": r"level",      # Changed the pattern to match any 4-digit number
  "bool": r"or|and|include|,",
  "inequal": r"above",
  "creditPoints": r"[0-9]{2}[0-9]*cp",
  "unitField": r" [a-zA-Z]{4} ",
  "lbracket": r"\(",
  "rbracket": r"\)",
  "pre2020": r"[A-Z]{4}[0-9]{3}"
}

#returns a tagged requirement given
def requirement_word_tag(data):
  words = re.findall(r'\(|\)|\w+', data)
  #print(words)
  word_types = {}
  for index,word in enumerate(words):
      matched = None
      for type_label, pattern in custom_tags.items():
          if re.match(pattern, word):
            #print("Pattern is : ",pattern)
            #print("Word is : ",word)
            matched = type_label
            #print("Matched = ",matched)
            break
      #print(type(word))
      word = str(index) + "#" + word
      word_types[word] = matched
      #print("Word Types[word] is now : ",word_types[word])
  #print(word_types)
  return word_types

#for sampleName ,sampleRequirement in sample.items():
  #requirement_word_tag(sampleRequirement)
  #print(requirement_word_tag(sampleRequirement))