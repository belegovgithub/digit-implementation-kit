import math
import time
from math import isnan
import io
import os
import numpy
import xlrd as xlrd
import xlwt
from common import *
from config import config, load_config
import requests
import json
import pandas as pd

search_resp_list=[]
post_data_list=[]
post_data_resp_list=[]
AZURE_LINK="https://13.71.65.215.nip.io"
DEMO_CHAWANI_LINK="https://demo.echhawani.gov.in"
AZURE_TOKEN="ef9d6e42-526c-4c29-8e70-6d27a9694aef"
DEMO_CHAWANI_TOKEN=""
LOG_PATH=r"D:\CB\Verified-CB-Data"
RETAIN_SAME_SLAB=["pb.agra","pb.delhi","pb.pune","pb.testing","pb.secunderabad","pb.lucknow"]

class DateTimeEncoder(JSONEncoder):
        #Override the default method
        def default(self, obj):
            if isinstance(obj, (date, datetime)):
                return int((obj - epoch).total_seconds() * 1000.0)

def fetchBillingSlabs(tenantid,host,token) : 
    billingSlabs =[]
    slabs = requests.post(host + "/tl-calculator/billingslab/_search?tenantId=" + tenantid, json={
                    "RequestInfo": {
                        "authToken": token
                    }})
    #print(slabs.status_code)
    if slabs.status_code == 200 :
        billingSlabs=slabs.json()["billingSlab"]
    return billingSlabs

def createBillingSlabs(tenantid,host,token,billingSlab):
    createData ={
            "RequestInfo": {
                "authToken": token
            },
            "billingSlab": billingSlab
    } 
    post_data_list.append(createData)
    res = requests.post(host + "/tl-calculator/billingslab/_create?tenantId={}".format(tenantid), json=createData )
    print(res)
    if res.status_code ==200 or res.status_code ==201 :
        post_data_resp_list.append(res.json())
    else : 
        print("Error in pushing data for CB ",tenantid)

def main():
    print("Slab will be copied using available TL module", config.CITY_MODULES_JSON)
    with io.open(config.CITY_MODULES_JSON, encoding="utf-8") as f:
        cb_module_data = json.load(f) 
    for found_index, module in enumerate(cb_module_data["citymodule"]):
        if module["module"]=="TL":
            for index, teant in enumerate(module['tenants']) :
                tenantId =teant['code']
                if tenantId in RETAIN_SAME_SLAB : 
                    continue
                print("====================",tenantId,"=====================")
                billingSlabs =fetchBillingSlabs(tenantId,AZURE_LINK,AZURE_TOKEN)
                print(len(billingSlabs))
                if len(billingSlabs) > 0 :
                    search_resp_list.append(billingSlabs)
                    createBillingSlabs(tenantId,DEMO_CHAWANI_LINK,DEMO_CHAWANI_TOKEN,billingSlabs)
                
    dateStr=datetime.now().strftime("%d%m%Y%H%M%S")

    ## Copy the response to json file
    with io.open(os.path.join(LOG_PATH, "billingslab-search_res_"+str(dateStr)+".json"), mode="w", encoding="utf-8") as f:
        json.dump(search_resp_list, f, indent=2,  ensure_ascii=False, cls=DateTimeEncoder)
    
    with io.open(os.path.join(LOG_PATH, "billingslab-create_req_"+str(dateStr)+".json"), mode="w", encoding="utf-8") as f:
        json.dump(post_data_list, f, indent=2,  ensure_ascii=False, cls=DateTimeEncoder)
    
    with io.open(os.path.join(LOG_PATH, "billingslab-create_res_"+str(dateStr)+".json"), mode="w", encoding="utf-8") as f:
        json.dump(post_data_resp_list, f, indent=2,  ensure_ascii=False, cls=DateTimeEncoder)
                
if __name__ == "__main__":
    main()
