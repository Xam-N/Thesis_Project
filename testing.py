from POS_Tagging import sample, custom_tags, requirement_word_tag
from Phrase_Types import phraseTags, requirement_tag

#fix this
test = "10cp from (MATH132-MATH136 or DMTH137 or MATH1007-MATH1025 or (STAT150 or STAT1250) or (STAT170 or STAT1170) or (STAT171 or STAT1371) or (STAT175 or STAT1175))"

def findWeight(wordTags,weight): #finds the number of and thingys to determine the weight each edge of a nested requirement should be added with)
  
  andCounter = 0.0
  
  lBracketCounter = 0
  
  for word in wordTags:
     
    if word[0] ==  "(":
      lBracketCounter = lBracketCounter + 1

    if word[0] == ")":
      lBracketCounter = lBracketCounter - 1
      
    if word[0] == "and" and lBracketCounter == 0: #if an and is present increment the AND counter to reflect as such
      andCounter += 1 
  
  print("The given word list is: ",wordTags)
  print("The weight before is: ",weight)
  
  weight = weight / (andCounter+1) #1 and has 2 nodes of weight 0.5 therefore divide weight by andCounter + 1
  
  print("The weight after is: ",weight)
  print("The weight of the new edge should be: ",weight," andCounter is : ",andCounter)
  return weight



testing = requirement_word_tag(test)
type = requirement_tag(testing)
print(type)
print(findWeight(testing,0.5))