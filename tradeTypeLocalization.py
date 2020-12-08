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
    letter = tradeType_category+"_"+"EATING"+"_"+"A"+subTypeVal
  elif keyword.find("Medical") != -1:
    letter = tradeType_category+"_"+ "MEDICAL"+"_"+"B"+subTypeVal
  elif keyword.find("Veterinary") != -1:
	  letter =tradeType_category+"_"+"VETERINARY"+"_"+"C"+subTypeVal
  elif keyword.find("Flammables") != -1:
	  letter =tradeType_category+"_"+"DANGEROUS"+"_"+"D"+subTypeVal
  elif keyword.find("Medium") != -1:
	  letter =tradeType_category+"_"+"MEDIUM"+"_"+"F"+subTypeVal
  elif keyword.find("Offices ") != -1:
	  letter =tradeType_category+"_"+"OTHERS"+"_"+"E"+subTypeVal
    
  return letter

def main():
  

  dfs = open_excel_file("C:/Users/Administrator/Downloads/Trade License Rate Template.xlsx")
  docCodes = get_sheet(dfs, "TradeRates")
  docCodes = docCodes.astype(str)
  #print(docCodes)
  locale_data = []


  for j in range(0,len(docCodes)) :
    tradeType_category = getTradeCategory(docCodes.iloc[j, 1],docCodes.iloc[j, 2])
    tradeType_message = docCodes.iloc[j, 4] 
    #print(tradeType_message)
    locale_module = "rainmaker-tl"
    locale_data.append({
                        "code": "TRADELICENSE_TRADETYPE_"+ tradeType_category,
                        "message": tradeType_message,
                        "module": locale_module,
                        "locale": "hi_IN"
                    })

  
  data = {
        "RequestInfo": {
            "authToken": "{{access_token}}"
        },
        "tenantId": config.TENANT,
        "messages": locale_data
    }
  print(json.dumps(data, indent=2))
  auth_token = superuser_login()["access_token"]
  localize_response = upsert_localization(auth_token, data)






if __name__ == "__main__":
  main()