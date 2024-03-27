from Data_Processing import dataRead
from POS_Tagging import sample, custom_tags, requirement_word_tag
from Phrase_Types import phraseTags, requirement_tag
from Graphing import createMatrix

def main():
  unitRequirements_file = 'unitRequirements.csv'
  unitSessions_file = 'unitSessionOfferings.csv'
  data = dataRead(unitRequirements_file, unitSessions_file)
  createMatrix(data)
  
  