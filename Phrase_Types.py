import re
from POS_Tagging import sample, requirement_word_tag

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
  "sample 14":"30cp at 1000 level including COMP1000 ",
}

# Define requirement types and the corresponding patterns
phraseTags = {
    "Fake_Credit_Point": r"creditPoints\s+lbracket\s+(unitCode|pre2020)*",
    "Boolean": r"(\(*unitCode|pre2020)(\s+(bool|and|or)\s+(unitCode|pre2020))*",
    "Credit_Point": r"creditPoints\s+(unitYear\s+level(\s+(bool|inequal))*|)",
    #"Composite": r"creditPoints\s+(\(*unitCode|pre2020)(\s+(bool|and|or)\s+(unitCode|pre2020))*", #if boolean and credit point is present within a thingy
    #"Other": r"", #should return other for admission etc.
}

#(\(*unitCode|pre2020)(\s+(bool|and|or)\s+(unitCode|pre2020))*)


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



for sampleName ,sampleRequirement in sample.items():
    requirement_word_tag(sampleRequirement)
    words = requirement_word_tag(sampleRequirement)
    print(requirement_tag(words))
