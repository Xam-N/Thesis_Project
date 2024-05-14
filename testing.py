from POS_Tagging import sample, custom_tags, requirement_word_tag
from Phrase_Types import phraseTags, requirement_tag
import re
import numpy as np
import pandas as pd

def parse_statement(adjMatrixParse,unit,statement): 
    lbracketIndex = -1
    for index,word in enumerate(statement):
        if word[1] == "lbracket" or word[1] == "rbracket":
            if len(statement[lbracketIndex+1:index]) != 0:
                #print("These words used to call function, : ",statement[lbracketIndex+1:index])
                #print(findWeight(statement,lbracketIndex+1,index))
                wordTags = statement[lbracketIndex+1:index]
                #weight = findWeight(statement,lbracketIndex+1,index)
                #requirementTag = requirement_tag(wordTags)
                #maybe somehow check if I should be added an or edge or not????
                #maybe check fi unit is a fake credity point, i might need to change this somehow if that is the case
                #adjMatrixParse = addRequirementEdges(adjMatrixParse,unit,wordTags,requirementTag,weight)
                print("here")
                #print(adjMatrix)
            lbracketIndex = index
    if lbracketIndex == -1:
      weight = 1
      requirementTag = requirement_tag(statement)
      #adjMatrixParse = addRequirementEdges(adjMatrixParse,unit,statement,requirementTag,weight) 
            
    return adjMatrixParse

def leftAndSearch(wordTags,startIndex):
    tempDict = {}
    height = 0
    andCounter = 0 
    skip = False
    skipQuantity = 0
    if startIndex == 0:
        return tempDict
    for uselessIndex,word in enumerate(reversed(wordTags[:startIndex-1])):
        print(word)
        if skip == True: 
            if word[1] == "rbracket":
                skipQuantity = skipQuantity + 1
                continue
            if word[1] == "lbracket" and skipQuantity == 0:
                skip = False
                continue
            if word[1] == "lbracket" and skipQuantity != 0:
                skipQuantity = skipQuantity - 1
                continue
            continue
        if word[1] == "bool":
            if word[0] == "and":
                andCounter = andCounter + 1
        if word[1] == "rbracket":
            skip = True
        if word[1] == "lbracket":
            tempDict[height] = andCounter
            height = height + 1
            andCounter = 0
    if andCounter != 0:
        tempDict[height] = andCounter
    return tempDict

def rightAndSearch(wordTags,stopIndex):
    tempDict = {}
    height = 0
    andCounter = 0 
    skip = False
    skipQuantity = 0
    for index,word in enumerate(wordTags[stopIndex+1:]):
        if skip == True: 
            if word[1] == "lbracket":
                skipQuantity = skipQuantity + 1
                continue
            if word[1] == "rbracket" and skipQuantity == 0:
                skip = False
                continue
            if word[1] == "rbracket" and skipQuantity != 0:
                skipQuantity = skipQuantity - 1
                continue
            continue
        if word[1] == "bool":
            if word[0] == "and":
                andCounter = andCounter + 1
        if word[1] == "lbracket":
            skip = True
        if word[1] == "rbracket":
            tempDict[height] = andCounter
            height = height + 1
            andCounter = 0
    if andCounter != 0:
        tempDict[height] = andCounter
        
    return tempDict        

statement = "MECH3005 and(MECH3003 or MECH303)"
statement2 = "(MECH3003 or MECH303) and MECH3005"
tags = requirement_word_tag(statement)
tags2 = requirement_word_tag(statement2)
#parse_statement([],"COMP2000",tags)
print(tags2[:])
print(leftAndSearch(tags2,5))
print(rightAndSearch(tags2,6))

