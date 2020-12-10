from common import *
from config import config
import io
import os
import numpy
from config import load_mCollect_config
import pandas as pd

def getTradeCategory(keyword,subType):
  #print("keyword--",keyword,int(float(subType)))
  global letter
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

  dfs = open_excel_file(config.TRADE_DOC_TYPE_WORKBOOK)
  docCodes = get_sheet(dfs, config.SHEET_TRADEDOC)
  docCodes = docCodes.astype(str)
  #print(len(docCodes. columns))
  #print(docCodes.columns)
  #print(docCodes.iloc[0, 1])

  dfs = open_excel_file(config.TRADE_RATE_WORKBOOK)
  tradeTypeCodes = get_sheet(dfs, config.SHEET_TRADERATE)
  tradeTypeCodes = tradeTypeCodes.astype(str)
  #print(tradeTypeCodes)
  #print(tradeTypeCodes.iloc[0, 1])

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
 
  
  tradeType_uom = ""
  tradeType_trade = []
  #print(getTradeCategory(tradeTypeCodes.iloc[2, 1]))
  docDict = loadDocDict()
  print(docDict)

  uomDict = {
    "Flat/Fixed":None,
    "Area- per -Sq Ft":"SqFt",
    "Motor Power - HP":"MoHP",
    "No of Beds - Number":"NoBed",
    "Star":"Star",
    "no. of workers":"NoWorker",
    "No. of category":"NoCategory"
  }

  for j in range(0,len(tradeTypeCodes)) :
    if tradeTypeCodes.iloc[j, INDEX_TRADE_APPLICABLE] == "Applicable":
      #print(tradeTypeCodes.iloc[j, 2], docCodes.iloc[j,2])
      tradeType_category = getTradeCategory(tradeTypeCodes.iloc[j, 1],tradeTypeCodes.iloc[j, 2])
      tradeType_uom = uomDict[tradeTypeCodes.iloc[j,5]]
      #print(tradeType_category)
      if tradeTypeCodes.iloc[j, 2] == docCodes.iloc[j,2]:
        k=0
        docCodes_new=[]
        docCodes_renew=[]
        for k in range(4,len(docCodes.columns)):
          #print(str(docCodes.iloc[j, k]).strip())
        #for k in range(4,9):
          #if not pd.isna(docCodes.iloc[j, k]):
          if str(docCodes.iloc[j, k]).strip() != 'nan':
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
  #print(final_data)

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
  

def loadDocDict():
  docDict = {
    "Applicant Photo":"OWNERPHOTO",
    "Occupancy Related Doc":"OWNERSHIPPROOF",
    "Proof Of Identity":"OWNERIDPROOF",
    "Proof Of Address":"ADDPROOF",
    "Self Decleration":"SELFDECLERATION",
    "Medical Certificate":"MEDCERT",
    "Medical Fitness Certificate":"MEDCERT",    
    "Medical Fitness":"MEDCERT",    
    "NOC from fire Department":"FIRENOC",
    "Food Safety Certificate":"FOODCERT",
    "Duly filled application form":"APPLETTER",
    "Tax Receipt" : "TAXRECEIPT",
    "Fire NOC" : "FIRENOC",
    "NOC  Neighbour1" : "NBNOC1",
    "NOC  Neighbour2" : "NBNOC2",
    "CMO Registration Certificate": "CMOREGCERT",
    "Drug License Certificate": "DRUGLICCERT",
    "Building Photograph": "BULDPHOTO",
    "Certification and NOC from related Authorities":"CERTNOCAUTH",
    "Registration of Jal Nigam Department (State Govt.)":"REG_JALNIGAM",
    "Licence from Excise Department of State Govt.":"LIC_EXCISE",
    "Licence from Excise Department":"LIC_EXCISE",
    "Registration from Food & Supplies Department of State Govt.": "FOODCERT",
    "Licence from Medical Department (i.e. CMO)  of State Govt.":"CMOREGCERT",
    "Registration of DIOS/BSA/Education Department of State Govt.":"REG_EDUCATION",
    "Licence from Entertainment Tax Department of State Govt.":"LIC_ENTERTAINMENT_TAX",
    "Licence from Petroleum Department":"LIC_PETROL",
    "Allotment Letter of Competent Authority":"APPOINT_LETTER",#localization executed
    "Food Safety Certificate and Tab Vaccination Certificate":"FOOD_TAB_CERT",
    "NOC from Owner for Rented Private Buildings":"NOC_OWNER",
    "NOC from Cantt. Board":"NOC_CANTT",
    "Liquore Licence from State":"LIC_LIQUOR",
    "Photo Copy Of Old Licence/Reciept No.":"PHOTO_OLD_LIC",
    "NOC From The House Owner/Lessee Of The Holding":"NOC_OWNER",
    "NOC of the HOR if Applicant is not HOR": "NOC_HOR",
    "Food License Issued by FSSAI":"FOOD_FSSAI",
    "Valid License Issued by Concerned Authority":"LIC_AUTH",
    "Property Tax Bill":"PROPERTY_TAX",
    "Bar/Liquor Licence":"LIC_LIQUOR",
    "Licence Halls":"LIC_HALLS",
    "Labour Licence" : "LIC_LABOUR",
    "Pollution Control Board" : "POLLUTION_BOARD_NOC",
    "Animal Husbandary Deptt" : "LIC_ANIMAL_HUSBANDARY",
    "Health Deptt" : "REG_HEALTH",
    "Disaster Management Deptt":"DISASTER_MGMT_NOC",
    "Supply Deptt":"SUPPLY_DEPT_NOC",
    "Agri Deptt" : "LIC_AGRI_DEPT",
    "RBI Authorization" : "RBI_CERT",
    "Transport Deptt" : "TRANSPORT_DEPT_NOC",
    "Labor Department certificate" : "LABOUR_DEPT_NOC",
    "Education Deptt" : "REG_EDU_DEPT",
    "Local authority permission from Local Police/S.D.O/D.M":"LOCAL_CERT",
    "FSSAI Certificate Of State Govt":"FOOD_FSSAI",
    "Copy Of GST / State Govt Registration/Certificate":"GST_REGT_CERT"


  }
  return docDict

if __name__ == "__main__":
  main()
