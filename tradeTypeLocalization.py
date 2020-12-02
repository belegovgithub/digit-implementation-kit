from common import *
from config import config
import io
import os
import numpy
from processing.generate_localization_data import process_CB_localization

def getTradeCategory(keyword,subType):
  #print("keyword--",keyword,int(float(subType)))
  global letter;
  subTypeVal = str(int(float(subType)))
  tradeType_category = "TRADE"
  if keyword.find("Eating") != -1:
    letter = tradeType_category+"."+"EATING"+"."+"A"+subTypeVal
  elif keyword.find("Medical") != -1:
    letter = tradeType_category+"."+ "MEDICAL"+"."+"B"+subTypeVal
  elif keyword.find("Veterinary") != -1:
	  letter =tradeType_category+"."+"VETERINARY"+"."+"C"+subTypeVal
  elif keyword.find("Flammables") != -1:
	  letter =tradeType_category+"."+"DANGEROUS"+"."+"D"+subTypeVal
  elif keyword.find("Medium") != -1:
	  letter =tradeType_category+"."+"MEDIUM"+"."+"F"+subTypeVal
  elif keyword.find("Offices ") != -1:
	  letter =tradeType_category+"."+"OTHERS"+"."+"E"+subTypeVal
    
  return letter

def main():
  print("hello")

  dfs = open_excel_file("/content/drive/MyDrive/Workspace/Trade Type Localization/TL Localization updated.xlsx")
  docCodes = get_sheet(dfs, "Sheet1")
  docCodes = docCodes.astype(str)
  print(docCodes)
  locale_data = []


  for j in range(0,len(docCodes)) :
    tradeType_category = getTradeCategory(docCodes.iloc[j, 1],docCodes.iloc[j, 2])
    tradeType_message = docCodes.iloc[j, 3] 
    locale_module = "rainmaker-tl"
    locale_data.append({
                        "code": "TRADELICENSE_TRADETYPE_"+ tradeType_category,
                        "message": tradeType_message,
                        "module": locale_module,
                        "locale": "en_IN"
                    })

  
  print(locale_data)








if __name__ == "__main__":
  main()