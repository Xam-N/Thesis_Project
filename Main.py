from Data_Processing import *
from POS_Tagging import *
from Phrase_Types import *
from Graphing import *
from Bin_Packing import *

def runner():
  unitRequirements_file = 'unitRequirements.csv'
  unitSessions_file = 'unitSessionOfferings.csv'
  data = dataRead(unitRequirements_file, unitSessions_file)

  civilEng = ["ENGG1000","ENGG1050","ENGG2000","ENGG2050","ENGG3000","ENGG3050","ENGG4001","CIVL1001","MATH1010","MATH1020","COMP1000","PHYS1510","CIVL2101","CIVL2201","CIVL2205","CIVL2301","MATH2055","MECH2002","CIVL3101","CIVL3201","CIVL3301","CIVL3305","CIVL3401","CIVL4090","CIVL4091","CIVL4201","CIVL4301","CIVL4401"]
  elecEng = ["ENGG1000","ENGG1050","ENGG2000","ENGG2050","ENGG3000","ENGG3050","ENGG4001","MATH1010","MATH1020","COMP1000","PHYS1510","PHYS1520","MATH2055","ELEC2005","ELEC2040","ELEC2042","ELEC2070","ELCT3005","ELCT3006","ELEC3024","ELEC3042","ELEC3076","TELE3350","ELCT4001","ELCT4004","ELEC4250","ELEC4092","ELEC4093"]
  mechanicalEng = ["ENGG1000","ENGG1050","ENGG2000","ENGG2050","ENGG3000","ENGG3050","ENGG4001","MATH1010","MATH1020","COMP1000","MECH1001","PHYS1510","MATH2055","MECH2001","MECH2002","MECH2003","MECH2004","MECH2005","MECH3001","MECH3002","MECH3003","MECH3004","MECH3005","MECH4001","MECH4002","MECH4092","MECH4093","MECH4005"]
  mechatronicEng = ["ENGG1000","ENGG1050","ENGG2000","ENGG2050","ENGG3000","ENGG3050","ENGG4001","MATH1010","MATH1020","COMP1000","MECH1001","PHYS1510","PHYS1520","ELEC2070","ELEC2005","ELEC2040","MATH2055","MECH2003","MTRN2060","ELEC3024","ELEC3042","MTRN3026","MTRN3060","MTRN4062","MTRN4066","MTRN4068","MTRN4092","MTRN4093"]
  softwareEng = ["ENGG1000","ENGG1050","ENGG2000","ENGG2050","ENGG3000","ENGG3050","ENGG4001","COMP1000","COMP1010","COMP1050","COMP1300","COMP1350","MATH1007","COMP2000","COMP2010","COMP2050","COMP2100","COMP2250","MATH2907","COMP3000","COMP3010","COMP3100","COMP3310","COMP4000","COMP4050","COMP4060","COMP4092","COMP4093"]
  economics = ["ECON1020","ECON1021","STAT1250","ECON2003","ECON2004","ECON2032","ECON2041","ECON3000","ECON2015","ECON3081","ECON2035","ECON2044","ECON2050","ECON3018","ECON3034","ECON3036","ECON3056","ECON3059","ECON3060","ECON1031","BUSA1000","ACST1001","ACCG1000","COMP1000"]
  medScienceAnatomyMajor = ["ANAT1001","BIOL1110","BIOL1210","BIOL1620","CHEM1001","STAT1170","BIOL3661","HLTH2000", "PHYS1210","ANAT2003","BIOL2220","MEDI2100","MEDI2300","BIOL3210","MEDI3100","MEDI3300","MATH2010","MATH2020","MATH2110","MATH1010","MATH1020","MATH3900","MATH3902","MATH3905"]
  medScienceGenomicsMajor = ["ANAT1001","BIOL1110","BIOL1210","BIOL1620","CHEM1001","STAT1170","BIOL3661","HLTH2000","FOSE1025","BIOL2110","BMOL2401","BMOL2201","MEDI2201","BIOL3120","MEDI3200","BMOL3402","PSYU1101","PSYU1102","PSYU2236","PSYU2247","PSYU2234","PSYU3338","PSYU3352","PSYU3333"]
  medScienceInfectiousDiseaseMajor = ["ANAT1001","BIOL1110","BIOL1210","BIOL1620","CHEM1001","STAT1170","BIOL3661","HLTH2000","BIOL1310","BIOL2110","BIOL2410","HLTH2301","BMOL2401","BIOL3130","BMOL3401","HLTH3302","PSYU1101","PSYU1102","PSYU2236","PSYU2247","PSYU2234","PSYU3338","PSYU3352","PSYU3333"]
  medScienceMedicinalChemistryMajor = ["ANAT1001","BIOL1110","BIOL1210","BIOL1620","CHEM1001","STAT1170","BIOL3661","HLTH2000","CHEM1002","BMOL2201","CHEM2201","CHEM2601","MEDI2004","CHEM3202","CHEM3601","CHEM3801","PSYU1101","PSYU1102","PSYU2236","PSYU2247","PSYU2234","PSYU3338","PSYU3352","PSYU3333"]
  medScienceNeuroscienceMajor = ["ANAT1001","BIOL1110","BIOL1210","BIOL1620","CHEM1001","STAT1170","BIOL3661","HLTH2000","COGS1000","MEDI3301","ANAT2004","BIOL2230","MEDI2300","MEDI2301","PSYU3344","MEDI3300","PSYU1101","PSYU1102","PSYU2236","PSYU2247","PSYU2234","PSYU3338","PSYU3344","PSYU3333"]
  primaryEducationGeography = ["ARTS1000","PHIL1037","ARTS3500","ARTS3005","MMCC1012","SOCI1030","MMCC1020","MMCC1030","EDUC1070","SPED1020","EDUC2580","EDUC2610","EDUC2620","EDUC3620","EDUC3730","EDUC3830","GEOP1010","ENVS1017","GEOP2010","GEOP2050","GEOP2060","GEOP3000","GEOP3020","GEOP3090"]
  artsEnglishMajor = ["MMCC1050","MMCC1110","MMCC2011","MMCC2110","MMCC3011","MMCC3020","MMCC3110","MMCC2061","ENGL1001","ENGL1002","ENGL2010","ENGL2020","ENGL2030","ENGL3010","ENGL3020","ENGL3031","ARTS1000","PHIL1037","ARTS3500","AHIS3005","PHIL1031","PHIL1032","PHIL2010","PHIL2026"]
  chiropracticScience = ["ANAT1001","ANAT1002","BIOL1210","CHEM1001","CHIR1101","CHIR1102","PHYS1210","PSYU1101","ANAT2003","ANAT2004","ANTH2002","BIOL2220","BIOL2230","BMOL2201","CHIR2103","CHIR2104","HLTH2110","HLTH2301","CHIR3105","CHIR3610","HLTH3140","HLTH3302","HLTH3303","CHIR3106"]
  cyberSecurity = ["COMP1000","COMP1010","COMP1300","COMP1350","MATH1007","STAT1170","COMP2100","COMP2110","COMP2200","COMP2250","COMP2300","COMP2310","COMP2320","PICT2001","COMP3300","COMP3850","COMP3320","ACCG3025","COMP3100","COMP3310"]
  informationTechnologyAI = ["COMP1000","COMP1300","COMP1350","COMP2250","COMP3850","COMP1010","COMP2200","COMP3410","COMP1150","COMP1750","COMP2110","COMP2750","MMCC2041","COMP3120","COMP3130","COMP3770","MATH1007","COMP2100","COMP2291","COMP2300","COMP3100","COMP3250","COMP3010","STAT1170"]
  sciencePhysicsMajor = ["FOSE3000","FOSE1005","FOSE1015","FOSE1025","STAT1170","PHYS3810","PHYS1010","PHYS1020","PHYS2010","PHYS2020","PHYS2030","PHYS3010","PHYS3140","PHYS3180"]
  scienceMathsMajor = ["FOSE3000","FOSE1005","FOSE1015","FOSE1025","STAT1170","MATH3599","MATH2010","MATH2020","MATH2110","MATH1010","MATH1015","MATH1020","MATH1025","MATH3900","MATH3902","MATH3905","CHEM1001","CHEM1002","CHEM2201","CHEM2401","CHEM2601","CHEM3202","CHEM3601","CHEM3801"]
  archaeology = ["AHIS1300","AHIS1301","AHIS1200","AHIS1250","AHIS2211","AHIS2250","AHIS2251","AHIS2301","AHIS2302","AHIS3001","AHIS3005","AHIS3241","AHIS3251","AHIS3302","AHIS3306","AHIS3000","AHIS1210","AHIS1250","AHIS3000","AHIS2210","AHIS2211","AHIS2225","AHIS3001","AHIS3201"]
  ancientHistory = ["AHIS1200","AHIS1210","AHIS1250","AHIS1300","AHIS2210","AHIS2130","AHIS2225","AHIS2250","AHIS2251","AHIS3001","AHIS3201","AHIS3202","AHIS3241","AHIS3251","AHIS3005","AHIS3000"]
  music = ["MMCC1012","MMCC1020","MMCC1030","MMCC1045","MMCC2000","MMCC2057","MMCC2090","MMCC2063","MMCC2020","MMCC2033","MMCC3130","MMCC3032","MMCC3000","MMCC3043","MMCC3060","MMCC3160","MHIS1001","MHIS1002","MHIS3000","MHIS2000","MHIS2001","MHIS2003","MHIS3022","MHIS3027"]
  securityStudies = ["PHIL1037","PICT1010","PICT1011","PICT1012","PICT1014","PICT2001","PICT2010","PICT2012","PICT2013","PICT2015","PICT3011","PICT3012","PICT3013","PICT3014","PICT3015","PICT3020"]
  socialScience = ["SSCI1000","SOCI1000","POIR1010","SOCI2030","POIR2070","GEOP2050","SOCI2040","SSCI2010","SSCI2020","SSCI3010","POIR3060","ANTH3023","GEOP3070","ABST3040","SSCI3090"]
  fake = ["COMP4092","COMP4093"]
  
  testingResult = ""
  testingResult = f"{testingResult}n Civil Engineering \n{tester(civilEng,data)}\n"
  #testingResult = f"{testingResult}\n Electrical Engineering \n{tester(elecEng,data)}"
  #testingResult = f"{testingResult}\n Mechanical Engineering \n{tester(mechanicalEng,data)}"
  #testingResult = f"{testingResult}\n Mechatronic Engineering \n{tester(mechatronicEng,data)}"
  #testingResult = f"{testingResult}\n Software Engineering \n{tester(softwareEng,data)}"
  #testingResult = f"{testingResult}\n Economics \n{tester(economics,data)}"
  #testingResult = f"{testingResult}\n Medical Science, Anatomy \n{tester(medScienceAnatomyMajor,data)}"
  #testingResult = f"{testingResult}\n Medical Science, Genomics \n{tester(medScienceGenomicsMajor,data)}"
  #testingResult = f"{testingResult}\n Medical Science, Infectious Diseases \n{tester(medScienceInfectiousDiseaseMajor,data)}"
  #testingResult = f"{testingResult}\n Medical Science, Chemistry \n{tester(medScienceMedicinalChemistryMajor,data)}\n"
  #testingResult = f"{testingResult}\n Medical Science, Neuroscience \n{tester(medScienceNeuroscienceMajor,data)}"
  #testingResult = f"{testingResult}\n Primary Education \n{tester(primaryEducationGeography,data)}"
  #testingResult = f"{testingResult}\n Arts, English \n{tester(artsEnglishMajor,data)}"
  #testingResult = f"{testingResult}\n Chiropractic \n{tester(chiropracticScience,data)}"
  #testingResult = f"{testingResult}\n Cybersecurity \n{tester(cyberSecurity,data)}"
  #testingResult = f"{testingResult}\n Information Technology AI \n{tester(informationTechnologyAI,data)}"
  #testingResult = f"{testingResult}\n Science, Physics \n{tester(sciencePhysicsMajor,data)}"
  #testingResult = f"{testingResult}\n Science, Maths \n{tester(scienceMathsMajor,data)}"
  #testingResult = f"{testingResult}\n Archaeology \n{tester(archaeology,data)}"
  #testingResult = f"{testingResult}\n Ancient History \n{tester(ancientHistory,data)}"
  #testingResult = f"{testingResult}\n Music \n{tester(music,data)}"
  #testingResult = f"{testingResult}\n Security \n{tester(securityStudies,data)}"
  #testingResult = f"{testingResult}\n Social Science \n{tester(socialScience,data)}"
  #testingResult = f"{testingResult}\n Fake \n{tester(fake,data)}"
  #print("length_is:",len(mechanicalEng))
  return testingResult

def tester(testingString,data):
  preReqMatrix = createPreReqMatrix(data,testingString)
  coReqMatrix = createCoReqMatrix(data,testingString)
  #print("Here : ",unitDependencyLength(preReqMatrix, "ENGG2000"))
  #print("Here : ",unitDependencyLength(preReqMatrix, "PHIL1037"))
  #return 
  df = pd.DataFrame(preReqMatrix)
  df.to_csv("preReqMatrix.csv")
  dt = pd.DataFrame(coReqMatrix)
  dt.to_csv("coReqMatrix.csv") 
  
  
  
  testResults = f"{binPacking(preReqMatrix,coReqMatrix,data,testingString)}\n"
  return testResults

temp = runner()
print(runner())
f = open("results.txt", "a")
f.write(runner())
f.close()