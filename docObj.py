from common import *
from config import config
import io
import os
import numpy
from config import load_mCollect_config
def main():
    print("BUSINESS_SERVICE_JSON",config.DOCUMENT_TYPE_MASTER_JSON)
    print("hello")
    with io.open(config.DOCUMENT_TYPE_MASTER_JSON, encoding="utf-8") as f:
        documentType_data = json.load(f)
    #print("tenant data",documentType_data)
    found = False
    docType = []
    #make array of key value pair
    for found_index, service in enumerate(documentType_data["DocumentType"]):
        docType.append(service["code"])
    #print(docType)
    dfs = open_excel_file(config.DOCUMENT_TYPE_WORKBOOK)
    docCodes = get_sheet(dfs, config.SHEET_DOCLIST)
    docCodes = docCodes.astype(str)
    #print(glcodes)

    INDEX_DOC_NAME = 1
    INDEX_APPL_TYPE_1 = 2
    INDEX_APPL_TYPE_2 = 3
    INDEX_MANDATORY_FLAG = 4
    COL_INDEX=1

    ulbName = fix_value(docCodes.iloc[INDEX_DOC_NAME][COL_INDEX])
    #print(ulbName)

    #find the code in json and make objects
    docCodes_data=[]
    i=1
    for i in range(1,len(docCodes)) :
      if docCodes.iloc[i, INDEX_DOC_NAME] in docType :
           docCodes_data.append({"documentType": docCodes.iloc[i, INDEX_DOC_NAME],
                              "applicationType": [docCodes.iloc[i,INDEX_APPL_TYPE_1] , docCodes.iloc[i,INDEX_APPL_TYPE_2]],
                               "required": docCodes.iloc[i, INDEX_MANDATORY_FLAG]})
    

    print(docCodes_data)
    final_data = {
        "tenantId": config.TENANT_ID,
        "moduleName": "TradeLicense",
        "documentObj": [
          {
            "allowedDocs":[
                docCodes_data
            ],
             "tradeType": "TRADE"
          }
            
        ]
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

        with open(os.path.join(mCollect_path , "documentObj.json"), "w") as f:
            json.dump(final_data, f, indent=2)



if __name__ == "__main__":
    main()