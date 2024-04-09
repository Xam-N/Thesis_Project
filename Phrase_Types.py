import re
from POS_Tagging import sample, requirement_word_tag

# Define requirement types and the corresponding patterns
phraseTags = {
    "Boolean": r"(\(*unitCode|pre2020)(\s+(bool|and|or)\s+(unitCode|pre2020))*",
    "Credit_Point": r"creditPoints\s+unitYear\s+level(\s+(bool|inequal))*",
    "Composite": r"(Boolean|Credit_Point) (bool Boolean|Credit_Point)+",
    #"Other": r"", #should return other for admission etc.
}

#returns the label of the requirement
def requirement_tag(descriptionTags: str): # input should be string
    label = ""
    #print(temp) 
    lbracketIndex = 0
    rbracketIndex = 0
    while 'lbracket' in descriptionTags[rbracketIndex:]:
        lbracketIndex = descriptionTags.index('lbracket')
        #print(temp[lbracketIndex+1])
        rbracketIndex = descriptionTags.index('rbracket')
        #print(temp[rbracketIndex])
        new = descriptionTags[lbracketIndex+9:rbracketIndex-1]
        #print(new)
        #print("I am here : ",requirement_tag(new))
        print("Before ", descriptionTags)
        descriptionTags = descriptionTags.replace((descriptionTags[lbracketIndex:rbracketIndex+8]),requirement_tag(new))
        #descriptionTags[lbracketIndex:rbracketIndex] = requirement_tag(new)
        print("After ",     descriptionTags)
        #descriptionTags = descriptionTags[:lbracketIndex]+[requirement_tag(new)]+descriptionTags[rbracketIndex+1:]
        #label += requirement_tag(new)
    for phrase_name, phrase_type in phraseTags.items():
        if re.match(phrase_type, descriptionTags):
            label += phrase_name                
    #print("The requirement Label for: ",descriptionTags,"is: ",label)
    return label

for examples in sample.values():
    requirementTags = requirement_word_tag(examples)
    descriptionTags = ""
    for word_tag in requirementTags.values():
       if word_tag is not None:
           descriptionTags += word_tag + " "
    requirement_tag(descriptionTags)
    print(requirement_tag(descriptionTags))
