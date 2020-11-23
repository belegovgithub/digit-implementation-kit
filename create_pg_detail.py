import requests
import csv
from common import *
from config import config ,load_employee_creation_config
from common import superuser_login, get_employee_types, get_employee_status, add_role_to_user, get_employees_by_phone, \
    get_employees_by_id 
from config import config
import io
import os
import numpy
import pandas as pd
from datetime import datetime, timedelta


PG_HOST =r"http://localhost:8098/"
SUPERUSER_USER_INFO_OBJ ={}

def getValue(df, row,colName,defValue="") :
    if not pd.isna(row[df.columns.get_loc(colName)] ) : 
        return str(row[df.columns.get_loc(colName)]).strip() 
    else : 
        return defValue if defValue is not None else row[df.columns.get_loc(colName)] 

    
def getTime(df, row,colName,defValue=None) :
    try : 
        dObj = row[df.columns.get_loc(colName)]
        if not isinstance(dObj, datetime) and type(dObj) is str: 
            dateStr =row[df.columns.get_loc(colName)].strip() 
            if "/" in dateStr : 
                dObj=datetime.strptime(dateStr, '%d/%m/%Y') 
            elif "." in dateStr : 
                dObj=datetime.strptime(dateStr, '%d.%m.%Y') 
            else : 
                dObj=datetime.strptime(dateStr, '%d-%m-%Y') 
        milliseconds = int((dObj - datetime(1970, 1, 1)).total_seconds())*1000
        return milliseconds
    except Exception as ex:
        print("Error in time conversion ",row[df.columns.get_loc(colName)],ex)
    return None


def main():
    ## load default config
    load_employee_creation_config()
    city = config.CITY_NAME
    tenant_id = config.TENANT + "." + city.lower()
    post_data_list=[]
    post_data_resp_list=[]
    filePath = r"D:\paygov\Crendetials.xlsx"  #os.path.join(config.BOUNDARIES_FOLDER, config.HRMS_EXCEL_NAME)
    if not os.path.isfile(filePath) :
        raise Exception("File Not Found ",filePath)

    auth_token = superuser_login()["access_token"]
    DEPT_LIST =(mdms_call(auth_token, "common-masters", 'Department')["MdmsRes"]["common-masters"]["Department"])
    DESIG_LIST =(mdms_call(auth_token, "common-masters", 'Designation')["MdmsRes"]["common-masters"]["Designation"])

    print("auth token ", auth_token)
    start_row = 0
    dfs = open_excel_file(filePath)
    df = get_sheet(dfs, "Sheet1")
 
    requestObjList =[]
    responseObjList =[]
    for ind in df.index:
 
        row = df.iloc[ind] 
        
        headers = {'Content-Type': 'application/json'}
        details = []
        roles = []
        assignments=[]
        is_primary = True
        tenant = getValue(df,row,"TenantId" ,"" ) 
        merchantId = getValue(df,row,"MerchantID" ,"" ) 
        serviceId = getValue(df,row,"ServiceId" ,"" ) 
        secretKey = getValue(df,row,"SecretKey" ,"" ) 
        password = getValue(df,row,"Password" ,"" )  

        
        requestObj ={
                                 "RequestInfo": {
                                     "authToken": auth_token,
                                     "userInfo":SUPERUSER_USER_INFO_OBJ ## Need to enter superUser Detail 
                                 },
                                 "pgDetail": [
                                                {
                                                
                                                    "tenantId": tenant,
                                                    "merchantId": merchantId,
                                                    "merchantSecretKey": secretKey,
                                                    "merchantUserName": merchantId,
                                                    "merchantPassword": password,
                                                    "merchantServiceId": serviceId
                                                }
                                            ]
        }
        print("==================================================")
        print(requestObj)
        search_pg_detail_resp = requests.post(url=PG_HOST + 'pg-detail/_get', headers=headers,
                                      json=requestObj)
        print("Existing Detail ",search_pg_detail_resp,search_pg_detail_resp.json() )
        pgDetail = search_pg_detail_resp.json()["pgDetail"]
        if len(pgDetail)>0  : 
            print("PG Detail exist for tenant ",tenant)
        else : 
            requestObjList.append(requestObj)
            create_pg_detail_resp = requests.post(url=PG_HOST + 'pg-detail/_create', headers=headers,
                                      json=requestObj)
            if create_pg_detail_resp.status_code == 201 : 
                print("Gateway details saved successfully")
            print(create_pg_detail_resp.json())
            responseObjList.append(create_pg_detail_resp.json())
        

         
        print("\n\n")

    # Save the request /response of newly created user in same  folder for reference
    with io.open(os.path.join(config.BOUNDARIES_FOLDER,"pg-detail-request.json"), mode="w", encoding="utf-8") as f:
        json.dump(requestObjList, f, indent=2,  ensure_ascii=False, cls=DateTimeEncoder)
    with io.open(os.path.join(config.BOUNDARIES_FOLDER,"pg-detail-response.json"), mode="w", encoding="utf-8") as f:
        json.dump(responseObjList, f, indent=2,  ensure_ascii=False, cls=DateTimeEncoder)

if __name__ == "__main__":
    main()
