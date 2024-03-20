sentence_types = {
    "Boolean": r"unitCode+ [and|or|, unitCode]*",
    "Credit_Point": r"[0-9]*+cp"
    "Credit_Point": r"[0-9]+cp +(from +[A-Z]+[A-Z]+|at +[0-9]+ level or above|from +[A-Z]+ units at +[0-9]+ level or above|-)",
    "Composite": r"(Credit_Point +BOOL +Boolean|Boolean +BOOL +Other|Credit_Point +BOOL +Other|Boolean +BOOL +Credit_Point +BOOL +Other)",
    "Other": r"Admission to MRes|Admission to a special program|Admission requires permission of course director|Admission to Wuyagiba Study Hub Program 1"
}



def phraseIdentifying(requirement):
    
    
    
    
    if(requirement): 
        # boolean
        # 'unit' + 'bool' + 'unit'
    elif():
        # credit point
        # xxcp from 'level' units
        # xxcp from 'inequality' 'level'
        # xxcp from 'subject' at 'level'
        # xxcp from 'unit range'
    elif():
        # composite
        # combination of other phrase types
    elif():
        # other
        # special admission required etc.
        # ignore everything that reaches here
    