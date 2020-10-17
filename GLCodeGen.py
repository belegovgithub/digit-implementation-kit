from common import *
from config import config
import io
import os
import numpy
from config import load_mCollect_config
def main():
    load_mCollect_config()
    print("BUSINESS_SERVICE_JSON",config.BUSINESS_SERVICE_JSON)
    #load json data from MDMS
    with io.open(config.BUSINESS_SERVICE_JSON, encoding="utf-8") as f:
        businessservice_data = json.load(f)
    #print("tenant data",businessservice_data)
    found = False
    businessService = {}
    #make array of key value pair
    for found_index, service in enumerate(businessservice_data["BusinessService"]):
        businessService[service["businessService"].lower()]=service["code"]

    #print(businessService)
    dfs = open_excel_file(config.MCOLLECT_WORKBOOK)
    glcodes = get_sheet(dfs, config.SHEET_MCOLLECT)
    #print(glcodes)
    glcodes = glcodes.astype(str)
    #create a new column in dataframe
    glcodes['businessService'] = glcodes.apply(get_businessService, axis=1)
    #print(glcodes['businessService'])
    #print(glcodes.columns)
    offset = 1

    INDEX_TENANT_ULB_NAME = 0
    INDEX_GLCODE = 1
    INDEX_CB_CODE = 2
    INDEX_DEPT_CODE = 3 
    INDEX_FUND = 4
   
    INDEX_GLCODE = 4
    INDEX_CB_CODE = 5
    INDEX_DEPT_CODE = 6
    INDEX_FUND = 7
    #find the code in json and make objects
    glcodes_data=[]
    for i in range(len(glcodes)) : 
        #print(glcodes.iloc[i, 4], glcodes.loc[i, "businessService"]) 
        if glcodes.loc[i, "businessService"] in businessService : 
            glcodes_data.append({"code": businessService[glcodes.loc[i, "businessService"]],
                                                    "glcode": glcodes.iloc[i,INDEX_GLCODE].strip(),
                                                    "dept": glcodes.iloc[i, INDEX_DEPT_CODE].strip(),
                                                    "fund": glcodes.iloc[i , INDEX_FUND].strip()})


    # for found_index, row in enumerate(glcodes):
    #     print(row)
    #     if  row['businessService'] in businessService  :
    #         glcodes_data = glcodes.apply(lambda row: {"code": row[INDEX_GLCODE].strip(),
    #                                             "glcode": row[INDEX_GLCODE].strip(),
    #                                             "dept": row[INDEX_DEPT_CODE].strip(),
    #                                             "fund": row[INDEX_FUND].strip()}
    #                                 , axis=1)
    print(glcodes_data)
    final_data = {
        "tenantId": config.TENANT_ID,
        "moduleName": "BillingService",
        "GLCode": [
            glcodes_data
        ]
    }
     
    import sys

    json.dump(final_data, sys.stdout, indent=2)

    if config.ASSUME_YES:
        response = os.getenv("ASSUME_YES", None) or input("\nDo you want to append the data in repo (y/[n])? ")
    else:
        response = "y"

    if response.lower() == "y":
        mCollect_path = config.MDMS_LOCATION / config.CITY_NAME.lower() / "mCollect"
        os.makedirs(mCollect_path, exist_ok=True)       

        with open(os.path.join(mCollect_path , "GLCode.json"), "w") as f:
            json.dump(final_data, f, indent=2)

def get_businessService(row):
    return str(row[config.COLUMN_SERVICE_CAT]).lower() + "." + str(row[config.COLUMN_SERVICE_SUBCAT]).lower()

if __name__ == "__main__":
    main()