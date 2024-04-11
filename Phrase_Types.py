import re
from POS_Tagging import sample, requirement_word_tag

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
  "sample 10": "DUPL1000 or DUPL1000",
  "sample 11": "COMP3100"
}

# Define requirement types and the corresponding patterns
phraseTags = {
    "Boolean": r"(\(*unitCode|pre2020)(\s+(bool|and|or)\s+(unitCode|pre2020))*",
    "Credit_Point": r"creditPoints\s+unitYear\s+level(\s+(bool|inequal))*",
    "Composite": r"((Boolean bool Credit_Point)|(Credit_Point bool Boolean))+", #if boolean and credit point is present within a thingy
    #"Other": r"", #should return other for admission etc.
}


def requirement_tag(descriptionTags):#returns the label of the requirement as long as no brackets involved
    wordTags = ""
    for wordList in descriptionTags:
        if wordList[1] is not None:
            wordTags = wordTags + wordList[1] + " "
    label = ""
    for phrase_name, phrase_type in phraseTags.items():
        if re.match(phrase_type, wordTags):
            label = label + phrase_name              
    print("The requirement Label for: ",wordTags,"is: ",label)
    if label == "":
        label = "Other"
    return label



 
#for sampleName ,sampleRequirement in sample.items():
  
  #requirement_word_tag(sampleRequirement)
#  words = requirement_word_tag(sampleRequirement)
#  print(requirement_tag(words))
