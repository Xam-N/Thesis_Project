import re

custom_tags = {
  "unitCode": r"[A-Z]{4}[0-9]{4}",
  "dash": r"-",
  "unitYear": r"[0-9]000",
  "level": r"level",
  "bool": r"or|and|include|,",
  "inequal": r"above",

}

sample = "COMP3100 - something else"
sample2 = "COMP1000 - ENGG1000"
sample3 = "3000 level and above"

def tagDescription(data):
  words = data.split()
  word_types = {}
  for word in words:
      matched = None
      for type_label, pattern in custom_tags.items():
          if re.match(pattern, word):
              matched = type_label
              break
      word_types[word] = matched

  for word, custom_type in word_types.items():
    print(f"{word}: {custom_type}")
  
  return word_types
    
tagDescription(sample)
tagDescription(sample2)
tagDescription(sample3)