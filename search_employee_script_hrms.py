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
    print(config.TENANT_JSON,"config.TENANT_JSON")
    with io.open(config.TENANT_JSON, encoding="utf-8") as f:
        cb_module_data = json.load(f)
    for found_index, module in enumerate(cb_module_data["tenants"]):
        tenantMapping[module["description"].lower()]=module["code"]
    print(tenantMapping)
    for tenant_id in tenantMapping :
        auth_token = superuser_login()["access_token"]
        response_data = requests.post(config.HOST + "/egov-hrms/employees/_search?tenantId=" + tenant_id, json={
            "RequestInfo": {
                "authToken": auth_token
            }
        })
        post_data_resp_list.append(response_data)
        print(post_data_resp_list)
        #print(json.dump(response_data, indent=2))
        CITY_NAME=tenant_id.replace("pb.","").strip().upper()
        with io.open(os.path.join(r"D:\Temp","user.csv") , mode="a+", newline="") as f:
            write = csv.writer(f) 
            #print("User LIst ",userList)
            write.writerow([CITY_NAME]) 
            #write.writerows(userList) 

if __name__ == "__main__":
    main()
