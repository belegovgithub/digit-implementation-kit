import requests
import csv
from common import *
from config import config ,load_employee_creation_config
from common import superuser_login
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
    others_object = {
        "id": str(uuid.uuid4()),
        "boundaryNum": 1,
        "name": "Others",
        "localname": "Others",
        "longitude": None,
        "latitude": None,
        "label": "Zone",
        "code": "ZONE_OTHERS",
        "children": [
        {
            "id": str(uuid.uuid4()),
            "boundaryNum": 1,
            "name": "Others",
            "localname": "Others",
            "longitude": None,
            "latitude": None,
            "label": "Ward",
            "code": "WARD_OTHERS",
            "children": [
            {
                "id": str(uuid.uuid4()),
                "boundaryNum": 1,
                "name": "Others",
                "localname": "Others",
                "longitude": None,
                "latitude": None,
                "label": "Locality",
                "code": "LOCAL_OTHERS",
                "area": "Others",
                "children": []
            }
            ]
        }
        ]
    }
    with io.open(config.TENANT_JSON, encoding="utf-8") as f:
        cb_module_data = json.load(f)
        for found_index, module in enumerate(cb_module_data["tenants"]):
            if module["city"]["ulbGrade"]=="ST":
                continue
            
            tenant_id=module["code"]
            cityname = tenant_id.lower()[3:]
            boundary_path = config.MDMS_LOCATION /  cityname / "egov-location"
            print(cityname)
            
            if os.path.isfile(boundary_path / "boundary-data.json"):
                with open(boundary_path / "boundary-data.json") as f:
                    existing_boundary_data = json.load(f)
            found = False
            for tenantboundary in existing_boundary_data["TenantBoundary"]:
                if tenantboundary["hierarchyType"]["code"] == "REVENUE":
                    tenant_boundary = tenantboundary["boundary"]["children"]
                    for found_index, data in enumerate(tenant_boundary):
                        if data["code"] == "ZONE_OTHERS":
                            found = True
                            break
                break
            with open(boundary_path / "boundary-data.json", mode="w", encoding="utf-8") as f:
                if found:
                    print("Tenant - " + cityname + " already exists, overwriting")
                    #assert tenant_boundary[found_index] == tenant_id, "Updating for correct tenant id"
                    tenant_boundary[found_index] = others_object
                else:
                    print("Tenant - " + cityname + " doesn't exists, adding details")
                    tenant_boundary.append(others_object)
                json.dump(existing_boundary_data, f, indent=2,  ensure_ascii=False)
                process_boundary_localization_English(tenant_id,cityname)
                process_boundary_localization_hindi(tenant_id,cityname)
                #print("Boundary localization pushed.")
def process_boundary_localization_English(tenant_id,cityname):
    load_revenue_boundary_config()    
    locale_module = "rainmaker-" + tenant_id
    locale_data = []       
    locale_data.append({
                    "code": "PB_"+ cityname.upper() + "_REVENUE_" + "ZONE_OTHERS",
                    "message": "Others",
                    "module": locale_module,
                    "locale": "en_IN"
                })       
    locale_data.append({
                    "code": "PB_"+ cityname.upper() + "_REVENUE_" + "WARD_OTHERS",
                    "message": "Others",
                    "module": locale_module,
                    "locale": "en_IN"
                })        
    locale_data.append({
                    "code": "PB_"+ cityname.upper() + "_REVENUE_" + "LOCAL_OTHERS",
                    "message": "Others",
                    "module": locale_module,
                    "locale": "en_IN"
                })
    
    data = {
        "RequestInfo": {
            "authToken": "{{access_token}}"
        },
        "tenantId": tenant_id,
        "messages": locale_data
    }
    auth_token = superuser_login()["access_token"]
    localize_response = upsert_localization(auth_token, data)    
    #print(localize_response)

def process_boundary_localization_hindi(tenant_id,cityname):
    load_revenue_boundary_config()    
    locale_module = "rainmaker-" + tenant_id
    locale_data = []       
    locale_data.append({
                    "code": "PB_"+ cityname.upper() + "_REVENUE_" + "ZONE_OTHERS",
                    "message": "अन्य",
                    "module": locale_module,
                    "locale": "hi_IN"
                })       
    locale_data.append({
                    "code": "PB_"+ cityname.upper() + "_REVENUE_" + "WARD_OTHERS",
                    "message": "अन्य",
                    "module": locale_module,
                    "locale": "hi_IN"
                })        
    locale_data.append({
                    "code": "PB_"+ cityname.upper() + "_REVENUE_" + "LOCAL_OTHERS",
                    "message": "अन्य",
                    "module": locale_module,
                    "locale": "hi_IN"
                })
    data = {
        "RequestInfo": {
            "authToken": "{{access_token}}"
        },
        "tenantId": tenant_id,
        "messages": locale_data
    }
    auth_token = superuser_login()["access_token"]
    localize_response = upsert_localization(auth_token, data)
    #print(localize_response)

if __name__ == "__main__":
    main()
