from common import *
from config import config
import io
import os 
import sys
import pandas as pd

def getTemplate() :
    docList =[
    {
      "code": "OWNER.IDENTITYPROOF",
      "documentType": "OWNER",
      "required": True,
      "active": True,
      "hasDropdown": True,
      "dropdownData": [
        {
          "code": "OWNER.IDENTITYPROOF.AADHAAR",
          "active": True
        },
        {
          "code": "OWNER.IDENTITYPROOF.VOTERID",
          "active": True
        },
        {
          "code": "OWNER.IDENTITYPROOF.DRIVING",
          "active": True
        },
        {
          "code": "OWNER.IDENTITYPROOF.PAN",
          "active": True
        },
        {
          "code": "OWNER.IDENTITYPROOF.PASSPORT",
          "active": True
        }
      ],
      "description": "OWNER.ADDRESSPROOF.IDENTITYPROOF_DESCRIPTION"
    },
    {
      "code": "OWNER.ADDRESSPROOF",
      "documentType": "OWNER",
      "required": True,
      "active": True,
      "hasDropdown": True,
      "dropdownData": [
        {
          "code": "OWNER.ADDRESSPROOF.ELECTRICITYBILL",
          "active": True
        },
        {
          "code": "OWNER.ADDRESSPROOF.DL",
          "active": True
        },
        {
          "code": "OWNER.ADDRESSPROOF.VOTERID",
          "active": True
        },
        {
          "code": "OWNER.ADDRESSPROOF.AADHAAR",
          "active": True
        },
        {
          "code": "OWNER.ADDRESSPROOF.PAN",
          "active": True
        },
        {
          "code": "OWNER.ADDRESSPROOF.PASSPORT",
          "active": True
        }
      ],
      "description": "OWNER.ADDRESSPROOF.ADDRESSPROOF_DESCRIPTION"
    },
    {
      "code": "PROPERTY_TAX_RECIEPT",
      "documentType": "PROPERTY_TAX_RECIEPT",
      "active": True,
      "required": True,
      "hasDropdown": True,
      "dropdownData": [
        {
          "code": "PROPERTY_TAX_RECIEPT",
          "active": True
        }
      ],
      "description": "PROPERTY_TAX_RECIEPT_DESCRIPTION"
    },
    {
      "code": "SELFDECLERATION",
      "documentType": "SELFDECLERATION",
      "active": True,
      "required": True,
      "hasDropdown": True,
      "dropdownData": [
        {
          "code": "SELFDECLERATION",
          "active": True
        }
      ],
      "description": "SELFDECLERATION_DESCRIPTION"
    } 
    
  ]
    return docList


def getValue(df, row,colName,defValue="") :
    if not pd.isna(row[df.columns.get_loc(colName)] ) : 
        return str(row[df.columns.get_loc(colName)]).strip() 
    else : 
        return defValue if defValue is not None else row[df.columns.get_loc(colName)] 
def main():
    tenantMapping={}
    cbDocData ={}
    localizationData =[]
    with io.open(config.TENANT_JSON, encoding="utf-8") as f:
        cb_module_data = json.load(f)
    for found_index, module in enumerate(cb_module_data["tenants"]):
        tenantMapping[module["description"].lower()]=module["code"]
        cbDocData[module["description"].lower()]=getTemplate()
    
    dfs = open_excel_file('D:\HRMS_Data\DocsMapping&Clarifications_1.xlsx')
    df = get_sheet(dfs, "Sheet2")
    for ind in df.index: 
        row =df.iloc[ind]
        cbName = getValue(df,row,"CB" ,None ).lower()
        if cbName not in cbDocData : 
            print("CB description not found ",cbName)
            continue
        cbDocs =cbDocData[cbName]
        
        docCategory = getValue(df,row,"Doc Category" ,None ) 
        docDesc = getValue(df,row,"Doc Description " ,"" ) 
        mandatoryFld = getValue(df,row,"M_OR_N" ,True ) 
        dropDownCode = getValue(df,row,"DOC_MAPPING" ,None ) 
        dropDownText = getValue(df,row,"Additional Docs" ,"" ) 
        docList  = list(filter(lambda doc: doc["code"]==docCategory, cbDocs))
        if docCategory is None or dropDownCode is None : 
            print("Code is none for cb ",cbName)
        if len(docList) == 0 : 
            ele ={
                    "code": docCategory,
                    "documentType": docCategory,
                    "active":True,
                    "required": False,
                    "hasDropdown": True,
                    "dropdownData": [
                        {
                        "code": dropDownCode,
                        "active": True
                        }
                    ],
                    "description": str(docCategory) + "_DESCRIPTION"
                } 
            cbDocs.append(ele)
        else :
            ele ={
                        "code": dropDownCode,
                        "active": True
                  }
            docList[0]["dropdownData"].append(ele)
        if len(list(filter(lambda doc: doc["code"]==docCategory, localizationData))) ==0 : 
            localData ={
                "locale": "en_IN",
                "code": docCategory,
                "message": docDesc,
                "module": "rainmaker-ws"
            }
            localizationData.append(localData)
            localData ={
                "locale": "en_IN",
                "code": docCategory+"_DESCRIPTION",
                "message": docDesc,
                "module": "rainmaker-ws"
            }
            localizationData.append(localData)
        if len(list(filter(lambda doc: doc["code"]==dropDownCode, localizationData))) ==0 : 
            localData ={
                "locale": "en_IN",
                "code": dropDownCode,
                "message": dropDownText,
                "module": "rainmaker-ws"
            }
            localizationData.append(localData)

         
        

    print(json.dumps(cbDocData))
    with io.open(os.path.join(r"D:\HRMS_Data","localization.json"), mode="w", encoding="utf-8") as f:
        json.dump(localizationData, f, indent=2,  ensure_ascii=False, cls=DateTimeEncoder)   
    with io.open(os.path.join(r"D:\HRMS_Data","cbData.json"), mode="w", encoding="utf-8") as f:
        json.dump(cbDocData, f, indent=2,  ensure_ascii=False, cls=DateTimeEncoder)       
    for ele in cbDocData : 
        docList=cbDocData[ele]
        templateToPush ={
            "tenantId": tenantMapping[ele],
            "moduleName": "ws-services-masters",
            "Documents": docList
        }
        modifyTemplateToPush ={
            "tenantId": tenantMapping[ele],
            "moduleName": "ws-services-masters",
            "ModifyConnectionDocuments": docList
        }
        mCollect_path = config.MDMS_LOCATION / ele / "ws-services-masters"
        os.makedirs(mCollect_path, exist_ok=True)    
        with io.open(os.path.join(mCollect_path,"Documents.json"), mode="w", encoding="utf-8") as f:
            json.dump(templateToPush, f, indent=2,  ensure_ascii=False, cls=DateTimeEncoder)   
        with io.open(os.path.join(mCollect_path,"ModifyConnectionDocuments.json"), mode="w", encoding="utf-8") as f:
            json.dump(modifyTemplateToPush, f, indent=2,  ensure_ascii=False, cls=DateTimeEncoder)   
       
    
        




  

if __name__ == "__main__":
    main()
