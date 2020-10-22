from common import *
from config import config
import io
import os
import numpy
from config import load_mCollect_config
def main():
  print("hello")

  dfs = open_excel_file(config.DOCUMENT_TYPE_WORKBOOK)
  docCodes = get_sheet(dfs, config.SHEET_DOCLIST)
  docCodes = docCodes.astype(str)
  #print(docCodes)


  dfs = open_excel_file(config.TRADE_TYPE_WORKBOOK)
  tradeTypeCodes = get_sheet(dfs, config.SHEET_TRADETYPE_LIST)
  tradeTypeCodes = tradeTypeCodes.astype(str)
  #print(tradeTypeCodes)

  INDEX_DOC_NAME = 1
  INDEX_APPL_TYPE_1 = 2
  INDEX_APPL_TYPE_2 = 3
  INDEX_MANDATORY_FLAG = 4
  COL_INDEX=1

  INDEX_TRADE_TYPE = 1
  INDEX_TRADE_CAT = 2
  INDEX_TRADE_NEW_FEE = 7
  INDEX_TRADE_RENEW_FEE = 9
  INDEX_TRADE_UOM = 8
  COL_INDEX=1

    

  #find the code in json and make objects
  tradeType_final=[]
  docCodes_new=[]
  docCodes_renew=[]
  i=1
  j=1
  tradeType_eating = "EATING"
  tradeType_medical=  "MEDICAL"
  tradeType_Veterinary = "VETERINARY"
  tradeType_dangerous = "DANGEROUS"
  tradeType_general = "GENERAL"
  tradeType_private = "PRIVATE"
  tradeType_category = "";

  for j in range(1,len(tradeTypeCodes)) :
    print(tradeTypeCodes.iloc[j, INDEX_TRADE_CAT])
    
    #if tradeTypeCodes.iloc[j, INDEX_TRADE_CAT] in tradeType_eating:
     # tradeType_category = tradeType_eating;

  print(tradeType_category)


  for i in range(1,len(docCodes)) :
      if docCodes.iloc[i, INDEX_APPL_TYPE_1] == "NEW" :
          docCodes_new.append(docCodes.iloc[i, INDEX_DOC_NAME])
      if docCodes.iloc[i, INDEX_APPL_TYPE_2] == "RENEWAL" :
          docCodes_renew.append(docCodes.iloc[i, INDEX_DOC_NAME])
  print(docCodes_new)
  print(docCodes_renew)




























if __name__ == "__main__":
  main()
