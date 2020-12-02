from common import *
from config import config
import io
import os
import numpy
from config import load_mCollect_config

def getTradeCategory(keyword):
  print("Hello from a function")
  global letter;
  tradeType_category = "TRADE"
  if keyword.find("Eating") != -1:
    letter = tradeType_category+"."+"EATING"
  elif keyword.find("Medical") != -1:
    letter = tradeType_category+"."+ "MEDICAL"
  elif keyword.find("Veterinary") != -1:
	  letter =tradeType_category+"."+"VETERINARY"
  elif keyword.find("Flammables") != -1:
	  letter =tradeType_category+"."+"DANGEROUS"
  elif keyword.find("Medium") != -1:
	  letter =tradeType_category+"."+"MEDIUM"
  elif keyword.find("Offices ") != -1:
	  letter =tradeType_category+"."+"OTHERS"
    
  return letter


def main():
  print("hello")

  dfs = open_excel_file(config.TRADE_DOC_TYPE_WORKBOOK)
  docCodes = get_sheet(dfs, config.SHEET_TRADEDOC)
  docCodes = docCodes.astype(str)
  #print(docCodes)
  #print(docCodes.columns)
  #print(docCodes.iloc[2, 1])

  dfs = open_excel_file(config.TRADE_TYPE_NEW_WORKBOOK)
  tradeTypeCodes = get_sheet(dfs, config.SHEET_TRADERATE)
  tradeTypeCodes = tradeTypeCodes.astype(str)
  #print(tradeTypeCodes)
  print(tradeTypeCodes.iloc[2, 4])

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

  for j in range(1,len(tradeTypeCodes)) :
    if tradeTypeCodes.iloc[j, INDEX_TRADE_APPLICABLE] == "Applicable":
      print(getTradeCategory(tradeTypeCodes.iloc[2, 1]))











if __name__ == "__main__":
  main()
