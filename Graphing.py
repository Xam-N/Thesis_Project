def GraphRequirement(requirements):
    for requirement in requirements:
        if(requirement is boolean): 
            # boolean
            # 'unit' + 'bool' + 'unit'
        elif(requirement is credit_point):
            # credit point
            # xxcp from 'level' units
            # xxcp from 'inequality' 'level'
            # xxcp from 'subject' at 'level'
            # xxcp from 'unit range'
        elif(requirement is composite):
            # composite
            # combination of other phrase types
        elif(requirement is other):
            # other
            # special admission required etc.
            # ignore everything that reaches here
        