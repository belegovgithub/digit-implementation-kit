import json
import io
import os
from pathlib import Path
from config import config
from common import *


dfs = open_excel_file(config.TRADE_TYPE_WORKBOOK)
tradeTypeCodes = get_sheet(dfs, config.SHEET_TRADETYPE_LIST)
tradeTypeCodes = tradeTypeCodes.astype(str)

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
bank_data = []
tradeType_final=[]
docCodes_new=[]
docCodes_renew=[]
i=1
j=1
 
  
tradeType_uom = ""
tradeType_trade = []
uom = ""

  
for j in range(1,len(tradeTypeCodes)) :
    if tradeTypeCodes.iloc[j, INDEX_TRADE_NEW_FEE] is not None:
      tradeType_category = "TRADE"
    if config.TRADETYPE_EATING in tradeTypeCodes.iloc[j, INDEX_TRADE_CAT].upper():
      tradeType_category = tradeType_category+"."+config.TRADETYPE_EATING
    elif config.TRADETYPE_MEDICAL in tradeTypeCodes.iloc[j, INDEX_TRADE_CAT].upper():
      tradeType_category = tradeType_category+"."+config.TRADETYPE_MEDICAL 
    elif config.TRADETYPE_VETERINARY in tradeTypeCodes.iloc[j, INDEX_TRADE_CAT].upper():
      tradeType_category = tradeType_category+"."+config.TRADETYPE_VETERINARY
    elif config.TRADETYPE_DANGEROUS in tradeTypeCodes.iloc[j, INDEX_TRADE_CAT].upper():
      tradeType_category = tradeType_category+"."+config.TRADETYPE_DANGEROUS
    elif config.TRADETYPE_GENERAL in tradeTypeCodes.iloc[j, INDEX_TRADE_CAT].upper():
      tradeType_category = tradeType_category+"."+config.TRADETYPE_GENERAL 
    elif config.TRADETYPE_PRIVATE in tradeTypeCodes.iloc[j, INDEX_TRADE_CAT].upper():
      tradeType_category = tradeType_category+"."+config.TRADETYPE_PRIVATE
    tradeType_category = tradeType_category+"."+tradeTypeCodes.iloc[j, INDEX_TRADE_TYPE]
    if tradeTypeCodes.iloc[j, INDEX_TRADE_UOM] == "FIXED":
      tradeType_uom = "FLAT"
      uom = 'null'
    else :
      tradeType_uom = "RATE"
      if 

    
      docCodes_new=[]
      docCodes_renew=[]
    tradeType_trade.append({ "tenantId": "pb.delhi",
                             "licenseType": "PERMANENT",
                             "structureType": "IMMOVABLE.PUCCA",
                             "tradeType": tradeType_category,
                             "accessoryCategory": null,
                              "type": tradeType_uom,
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
                            "validityPeriod": "null",
                            "verificationDocument": []
                            })
  
  
print(tradeType_trade)

    data = {
        "RequestInfo": {
            "authToken": "{{access_token}}"
        },        
        "banks": bank_data
    }
    print(data)