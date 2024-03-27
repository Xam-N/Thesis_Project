import re
from POS_Tagging import sample, requirement_word_tag

# Define requirement types and the corresponding patterns
phraseTags = {
    "Boolean": r"unitCode(\s+(bool|and|or)\s+unitCode)*",
    "Credit_Point": r"creditPoints\s+unitYear\s+level(\s+(bool|inequal))*",
    "Composite": r"(unitCode(\s+(bool|and|or)\s+unitCode)*)+(creditPoints\s+unitYear\s+level(\s+(bool|inequal))+)",
    #"Other": r"",
}

#returns the label of the requirement
def requirement_tag(description):
    label = ""
    requirement = requirement_word_tag(description)
    temp = ""
    for word_tag in requirement.values():
        if word_tag is not None:
            temp += word_tag + " "
    for phrase_name, phrase_type in phraseTags.items():
        if re.match(phrase_type, temp):
            label += phrase_name
    return label

for examples in sample.values():
  print(requirement_tag(examples))
