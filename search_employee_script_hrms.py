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
import math 

def main():
    Flag =False
    tenantMapping={}
    post_data_resp_list=[]
    auth_token = superuser_login()["access_token"]
    print(config.TENANT_JSON,"config.TENANT_JSON")
    with io.open(config.TENANT_JSON, encoding="utf-8") as f:
        cb_module_data = json.load(f)
        for found_index, module in enumerate(cb_module_data["tenants"]):
            if module["city"]["ulbGrade"]=="ST":
                continue
            
            tenant_id=module["code"]
            cityname=module["name"]
            params = {"tenantId": tenant_id}
            jsonObj ={
                "RequestInfo": {
                    "apiId": "Rainmaker",
                    "ver": ".01",
                    "action": "",
                    "did": "1",
                    "key": "",
                    "msgId": "20170310130900|en_IN",
                    "requesterId": "",
                    "authToken": auth_token
                }
            }
            headers = {'Content-Type': 'application/json'}
            response_data = requests.post(config.HOST+"/egov-hrms/employees/_search", headers=headers, params=params, json=jsonObj)
            if response_data.status_code  == 200 : 
                employees =response_data.json()["Employees"]
                for employee in employees : 
                    if employee["user"] is None : 
                        continue
                    jsonObj ={}
                    jsonObj["city"]=cityname
                    
                    user =employee["user"]
                    jsonObj["userName"]=user["userName"]
                    jsonObj["name"]=user["name"]
                    jsonObj["mobileNumber"]=user["mobileNumber"]
                    
                    roles =user["roles"]
                    for role_index, role in enumerate(roles):
                        #print(role["name"])

                        jsonObj["Role"+str(role_index+1)]=role["name"]
                    post_data_resp_list.append(jsonObj)

            

        with io.open(os.path.join("D:\CB\Verified-CB-Data-20201230T133509Z-001\Verified-CB-Data","users.json"), mode="w", encoding="utf-8") as f:
            json.dump(post_data_resp_list, f, indent=2,  ensure_ascii=False, cls=DateTimeEncoder)
 

if __name__ == "__main__":
    main()
