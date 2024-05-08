from POS_Tagging import sample, custom_tags, requirement_word_tag

from Phrase_Types import phraseTags, requirement_tag

sample = "(COMP1000 and COMP1050) or (MECH1000 or MECH1050)"

wordTags = requirement_word_tag()

lbracketIndex = 0
rbracketIndex = 0
    
    
    
for index,word in enumerate(wordTags):
    if word[1] == "lbracket":
        lbracketIndex = index
    if word[1] == "rbracket":
        rbracketIndex = index
        newWords = wordTags[lbracketIndex+1:rbracketIndex] #adjust the word list to be after the section of brackets ends
        #print("newWords = ",newWords)
        newTags = requirement_tag(newWords) 
        #print("newTags = ",newTags)
        #weight = findWeight(wordTags,weight)
        #figure out how to find the weight before I run this code

        adjMatrix = addRequirementEdges(adjMatrix,unit,newWords,newTags,data,weight)