from Data_Processing import *
from POS_Tagging import *
from Phrase_Types import *
from Graphing import *

def runner():
  unitRequirements_file = 'unitRequirements.csv'
  unitSessions_file = 'unitSessionOfferings.csv'
  data = dataRead(unitRequirements_file, unitSessions_file)
  #desired = ["ENGG1000","ENGG1050","ENGG2000"]
  #desired = ["ENGG1000","ENGG1050","ENGG2000","ENGG3000","COMP1000","ENGG2050","MATH1015","MATH1007","MATH1007","MATH1000","MATH1010"]
  matrix = createMatrix(data)
  #print(matrix)
  df = pd.DataFrame(matrix)
  df.to_csv("matrix.csv")
  #np.savetxt("matrix.csv", matrix, delimiter=",")


runner()