from Data_Processing import *
from POS_Tagging import *
from Phrase_Types import *
from Graphing import *
from Bin_Packing import *

def runner():
  unitRequirements_file = 'unitRequirements.csv'
  unitSessions_file = 'unitSessionOfferings.csv'
  data = dataRead(unitRequirements_file, unitSessions_file)

  civilEng = ["LAWS1000","PHIL1037","STAT1170","MHIS1001","ENGG1000","ENGG1050","ENGG2000","ENGG2050","ENGG3000","ENGG3050","ENGG4001","CIVL1001","MATH1010","MATH1020","COMP1000","PHYS1510","CIVL2101","CIVL2201","CIVL2205","CIVL2301","MATH2055","MECH2002","CIVL3101","CIVL3201","CIVL3301","CIVL3305","CIVL3401","CIVL4090","CIVL4091","CIVL4201","CIVL4301","CIVL4401"]
  elecEng = ["LAWS1000","PHIL1037","STAT1170","MHIS1001","ENGG1000","ENGG1050","ENGG2000","ENGG2050","ENGG3000","ENGG3050","ENGG4001","MATH1010","MATH1020","COMP1000","PHYS1510","PHYS1520","MATH2055","ELEC2005","ELEC2040","ELEC2042","ELEC2070","ELCT3005","ELCT3006","ELEC3024","ELEC3042","ELEC3076","TELE3350","ELCT4001","ELCT4004","ELEC4250","ELEC4092","ELEC4093"]
  mechanicalEng = ["LAWS1000","PHIL1037","STAT1170","MHIS1002","ENGG1000","ENGG1050","ENGG2000","ENGG2050","ENGG3000","ENGG3050","ENGG4001","MATH1010","MATH1020","COMP1000","MECH1001","PHYS1510","MATH2055","MECH2001","MECH2002","MECH2003","MECH2004","MECH2005","MECH3001","MECH3002","MECH3003","MECH3004","MECH3005","MECH4001","MECH4002","MECH4092","MECH4093","MECH4005"]
  mechatronicEng = ["LAWS1000","PHIL1037","STAT1170","MHIS1001","ENGG1000","ENGG1050","ENGG2000","ENGG2050","ENGG3000","ENGG3050","ENGG4001","MATH1010","MATH1020","COMP1000","MECH1001","PHYS1510","PHYS1520","ELEC2070","ELEC2005","ELEC2040","MATH2055","MECH2003","MTRN2060","ELEC3024","ELEC3042","MTRN3026","MTRN3060","MTRN4062","MTRN4066","MTRN4068","MTRN4092","MTRN4093"]
  softwareEng = ["LAWS1000","PHIL1037","STAT1170","MHIS1002","ENGG1000","ENGG1050","ENGG2000","ENGG2050","ENGG3000","ENGG3050","ENGG4001","COMP1000","COMP1010","COMP1050","COMP1300","COMP1350","MATH1007","COMP2000","COMP2010","COMP2050","COMP2100","COMP2250","MATH2907","COMP3000","COMP3010","COMP3100","COMP3310","COMP4000","COMP4050","COMP4060","COMP4092","COMP4093"]
                                      
  
  testingResult = ""
  testingResult = f"{testingResult}\n Civil Engineering \n{tester(civilEng,data)}\n"
  testingResult = f"{testingResult}\n Electrical Engineering \n{tester(elecEng,data)}"
  testingResult = f"{testingResult}\n Mechanical Engineering \n{tester(mechanicalEng,data)}"
  testingResult = f"{testingResult}\n Mechatronic Engineering \n{tester(mechatronicEng,data)}"
  testingResult = f"{testingResult}\n Software Engineering \n{tester(softwareEng,data)}"
  print("length_is:",len(mechanicalEng))
  return testingResult

def tester(testingString,data):
  preReqMatrix = createPreReqMatrix(data,testingString)
  coReqMatrix = createCoReqMatrix(data,testingString)
  df = pd.DataFrame(preReqMatrix)
  df.to_csv("preReqMatrix.csv")
  dt = pd.DataFrame(coReqMatrix)
  dt.to_csv("coReqMatrix.csv") 
  testResults = f"{binPacking(preReqMatrix,coReqMatrix,data,testingString)}\n"
  return testResults

print(runner())