from common import *
from config import config
import io
import os 
import sys
import pandas as pd
def main():
    Flag =False
    docDict = loadDocDict()
    tenantMapping={}
    with io.open(config.TENANT_JSON, encoding="utf-8") as f:
        cb_module_data = json.load(f)
    for found_index, module in enumerate(cb_module_data["tenants"]):
        tenantMapping[module["description"].lower()]=module["code"]
    print(tenantMapping)
    #for root, dirs, files in os.walk(r"D:\CBData\Verified CB Data\CC", topdown=True):
    for root, dirs, files in os.walk(r"D:\Temp\SC", topdown=True):
        for name in dirs:
            #print (os.path.join(root, name))
            subfolder = os.path.join(root, name)
            ws_doc_file =os.path.join(root, name,"Document Master for Water connection.xlsx")
            if os.path.exists(ws_doc_file) :
                city = subfolder.replace(r"D:\Temp\SC\CB ","" ).strip().lower()
                if city not in tenantMapping:
                    print("Not In city",city)
                    continue
                config.CITY_NAME = city
                config.TENANT_ID = tenantMapping[city]
                callWS_Doc(ws_doc_file, docDict)
                Flag=False
        if Flag : 
            break


def callWS_Doc(ws_doc_file, docDict):
    docCode_data = [{
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
                        "code": "SELF_DECLERATION",
                        "documentType": "SELF_DECLERATION",
                        "active": True,
                        "required": True,
                        "hasDropdown": True,
                        "dropdownData": [
                            {
                            "code": "SELF_DECLERATION",
                            "active": True
                            }
                        ],
                        "description": "SELF_DECLERATION_DESCRIPTION"
                        }]
    dfs = open_excel_file(ws_doc_file)
    docNames = get_sheet(dfs, "Document Details")
    docNames = docNames.astype(str)
    row = docNames.iloc[0]
    docCodes = []
    for i in range(4,6):
        if not pd.isna(row[i]) or row[i].strip() != 'nan':
            docCodes.append(docDict[row[i]])
    json.dump(docCodes, sys.stdout, indent=2)
    return
    for i in range(len(docCodes)):
        docCode_data.append({
                            "code": docCodes[i],
                            "documentType": docCodes[i],
                            "active": True,
                            "required": True,
                            "hasDropdown": True,
                            "dropdownData": [
                                {
                                "code": docCodes[i],
                                "active": True
                                }
                            ],
                            "description": docCodes[i] + "_DESCRIPTION"
                            })
    final_data = {
        "tenantId": config.TENANT_ID,
        "moduleName": "ws-services-masters",
        "Documents": [
            docCode_data
        ]
    }

    json.dump(final_data, sys.stdout, indent=2)
    cityname = config.TENANT_ID.lower()[3:]
    ws_path = config.MDMS_LOCATION / cityname / "ws"
    os.makedirs(ws_path, exist_ok=True)       

    with open(os.path.join(ws_path , "DocumentType.json"), "w") as f:
        json.dump(final_data, f, indent=2)

    
    
def loadDocDict():
  docDict = {
    "Proof Of Identity":"OWNER.IDENTITYPROOF",
    "Proof Of Address":"OWNER.ADDRESSPROOF",
    "Property Tax Receipt":"PROPERTY_TAX_RECIEPT",
    "Self Decleration":"SELF_DECLERATION"
  }   
  return docDict 

if __name__ == "__main__":
    main()
