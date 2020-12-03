from common import *
from config import config
import io
import os
import numpy
from config import load_mCollect_config

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

  dfs = open_excel_file(config.TRADE_DOC_TYPE_WORKBOOK)
  docCodes = get_sheet(dfs, config.SHEET_TRADEDOC)
  docCodes = docCodes.astype(str)
  #print(len(docCodes. columns))
  #print(docCodes.columns)
  print(docCodes.iloc[0, 1])

  dfs = open_excel_file(config.TRADE_RATE_WORKBOOK)
  tradeTypeCodes = get_sheet(dfs, config.SHEET_TRADERATE)
  tradeTypeCodes = tradeTypeCodes.astype(str)
  #print(tradeTypeCodes)
  print(tradeTypeCodes.iloc[0, 1])

  INDEX_DOC_NAME = 1
  INDEX_APPL_TYPE_1 = 2
  INDEX_APPL_TYPE_2 = 3
  INDEX_MANDATORY_FLAG = 4
  COL_INDEX=1

  INDEX_TRADE_TYPE = 1
  INDEX_TRADE_CAT = 2
  INDEX_TRADE_NEW_FEE = 6
  INDEX_TRADE_RENEW_FEE = 8
  INDEX_TRADE_UOM = 7
  COL_INDEX=1

  INDEX_TRADE_APPLICABLE = 4
    

  #find the code in json and make objects
  tradeType_final=[]
  docCodes_new=[]
  docCodes_renew=[]
  i=2
  j=1
 
  
  tradeType_uom = "";
  tradeType_trade = [];
  #print(getTradeCategory(tradeTypeCodes.iloc[2, 1]))
  docDict = {
    "Applicant Photo":"OWNERPHOTO",
    "Occupancy Related Doc":"OWNERSHIPPROOF",
    "Proof Of Identity":"OWNERIDPROOF",
    "Proof Of Address":"ADDPROOF",
    "Self Decleration":"SELFDECLERATION",
    "Medical Certificate":"MEDCERT",
    "NOC from fire Department":"FIRENOC",
    "Food Safety Certificate":"FOODCERT",
    "Duly filled application form":"APPLETTER",
    "Tax Receipt" : "TAXRECEIPT",
    "Fire NOC" : "FIRENOC"
  }

  uomDict = {
    "Flat/Fixed":None,
    "Area- per -Sq Ft":"SqFt",
    "Motor Power - HP":"MoHP",
    "No of Beds - Number":"NoBed",
    "Star":"Star"
  }

  for j in range(0,len(tradeTypeCodes)) :
    if tradeTypeCodes.iloc[j, INDEX_TRADE_APPLICABLE] == "Applicable":
      print(tradeTypeCodes.iloc[j, 2], docCodes.iloc[j,2])
      tradeType_category = getTradeCategory(tradeTypeCodes.iloc[j, 1],tradeTypeCodes.iloc[j, 2])
      tradeType_uom = uomDict[tradeTypeCodes.iloc[j,5]]
      #print(tradeType_category)
      if tradeTypeCodes.iloc[j, 2] == docCodes.iloc[j,2]:
        k=0;
        docCodes_new=[]
        docCodes_renew=[]
        for k in range(4,len(docCodes.columns)):
          if docCodes.iloc[j, k] != 'nan':
            docCodes_new.append(docDict[docCodes.iloc[j, k]])
            docCodes_renew.append(docDict[docCodes.iloc[j, k]])

        
      #print(docCodes_new);
      tradeType_trade.append({"code": tradeType_category,
                            "uom" : tradeType_uom,
                            "applicationDocument" :[
                              {
                              "applicationType": "NEW",
                               "documentList": docCodes_new
                              },
                              {
                              "applicationType": "RENEWAL",
                               "documentList": docCodes_renew
                              }
                            ],
                            "active": "true",
                            "type": "TL",
                            "validityPeriod": None,
                            "verificationDocument": []
                            })


  #print(tradeType_trade)
  final_data = {
        "tenantId": config.TENANT_ID,
        "moduleName": "TradeLicense",
        "TradeType":  tradeType_trade
      }
  print(final_data)

  import sys

  json.dump(final_data, sys.stdout, indent=2)

  if config.ASSUME_YES:
        response = os.getenv("ASSUME_YES", None) or input("\nDo you want to append the data in repo (y/[n])? ")
  else:
        response = "y"

  if response.lower() == "y":
        mCollect_path = config.MDMS_LOCATION / config.CITY_NAME.lower() / "TradeLicense"
        os.makedirs(mCollect_path, exist_ok=True)       

        with open(os.path.join(mCollect_path , "TradeType.json"), "w") as f:
            json.dump(final_data, f, indent=2)
  



if __name__ == "__main__":
  main()
