from Data_Processing import *
from POS_Tagging import *
from Phrase_Types import *
from Graphing import *

def runner():
  unitRequirements_file = 'unitRequirements.csv'
  unitSessions_file = 'unitSessionOfferings.csv'
  data = dataRead(unitRequirements_file, unitSessions_file)
  matrix = createMatrix(data)
  print("Hello" +matrix)


print(runner())