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
from math import isnan

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
            auth_token = superuser_login()["access_token"]

            slabs = requests.post(config.HOST + "/tl-calculator/billingslab/_search?tenantId=" + tenant_id, json={
                "RequestInfo": {
                    "authToken": auth_token
                }
            })
            existing_slab_data = {get_slab_id(slab): slab for slab in slabs.json()["billingSlab"]}
            print(cityname.upper())
            #print(json.dumps(existing_slab_data, indent=2))
            
            slab_data_dict = {get_slab_id(slab): slab for slab in existing_slab_data}
            for item in slab_data_dict.keys() : 
                if item in existing_slab_data.keys() :                     
                    oldData =existing_slab_data[item]

 
def get_slab_id(slab):
    fields = ["applicationType", "structureType", "tradeType", "accessoryCategory", "type", "uom", "fromUom", "toUom"]
    data = []

    for field in fields:
        
        value = slab[field]
        if type(value) is not str and value is not None and isnan(value):
            value = None
        if value == "N.A.":
            value = None
        elif value == "NULL":
            value = None
        elif value == "Infinite":
            value = "Infinity"

        if type(value) is float:
            value = int(value)
        
        data.append(str(value or "-"))
    return "|".join(data)

if __name__ == "__main__":
    main()
