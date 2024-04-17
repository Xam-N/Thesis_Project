from Data_Processing import *
from POS_Tagging import *
from Phrase_Types import *
from Graphing import *

def runner():
  unitRequirements_file = 'unitRequirements.csv'
  unitSessions_file = 'unitSessionOfferings.csv'
  data = dataRead(unitRequirements_file, unitSessions_file)
  #desired = ["ABST2020","ABST2035","ENGG1000","ENGG1050","ENGG2000","ENGG3000","COMP1000","ENGG2050","MATH1015","MATH1007","MATH1007","MATH1000","MATH1010"]
  #desired = ["ABST2020","ABST2035","ENGG1000","ENGG1050"]
  softwareEng = ["COMP1000","COMP1010","COMP1050","COMP1300","COMP1350","MATH1007","COMP2000","COMP2010","COMP2050","COMP2100","COMP2250","MATH2907","COMP3000","COMP3010","COMP3100","COMP3310","COMP4000","COMP4050","COMP4060","COMP4092","COMP4093"]
  matrix = createMatrix(data,softwareEng)
  #print(matrix)
  df = pd.DataFrame(matrix)
  df.to_csv("matrix.csv")
  #np.savetxt("matrix.csv", matrix, delimiter=",")


runner()