import math
import time
from math import isnan
import io
import os
import numpy
import xlrd as xlrd
import xlwt
from common import *
#from common import superuser_login, open_excel_file, get_sheet, fix_value,search_Workflow,search_tl_billing_slab
from config import config, load_config
import requests
import json
import pandas as pd
#from numpyencoder import NumpyEncoder
#from tlPreprocessor import create_trade_n_accessory_data
post_data_resp_list=[]
post_data_list=[]
class DateTimeEncoder(JSONEncoder):
        #Override the default method
        def default(self, obj):
            if isinstance(obj, (date, datetime)):
                return int((obj - epoch).total_seconds() * 1000.0)
def createWorkflow(authToken,fileName,tenantId):
    with io.open(fileName, encoding="utf-8") as file : 
        workflow = json.load(file)
        workflow['tenantId']=tenantId
        print("Workflow",workflow)
        jsonObj ={
        "RequestInfo": {
            "apiId": "Rainmaker",
            "action": "",
            "did": 1,
            "key": "",
            "msgId": "20170310130900|en_IN",
            "requesterId": "",
            "ts": 1513579888683,
            "ver": ".01",
            "authToken": authToken 
             
        },
        "BusinessServices": [ workflow]}
        post_data_list.append(jsonObj)
        url = urljoin(config.HOST, '/egov-workflow-v2/egov-wf/businessservice/_create')
        params = {"tenantId": config.TENANT_ID}
        data = requests.post(url, params=params, json=jsonObj)
        if(data.status_code == 200):
            print("Workflow created for ",tenantId ," successfully")
        else : 
            print("Error in workflow creation for ",tenantId )
        post_data_resp_list.append(data.json()) 
def main():
    # load default config
    print("TENANT_JSON", config.CITY_MODULES_JSON)
    auth_token =superuser_login()["access_token"] 

    with io.open(config.CITY_MODULES_JSON, encoding="utf-8") as f:
        cb_module_data = json.load(f)
    for found_index, module in enumerate(cb_module_data["citymodule"]):
        if module["module"]=="TL":
            #print("index ",found_index,"  tenant ",module['tenants'])
            for index, teant in enumerate(module['tenants']) :
                tenantId =teant['code']
                
                resp =search_Workflow(auth_token,tenantId,"NewTL")
                if(len(resp['BusinessServices'])==0) :
                    print("+++++++++++++++++++++++++++++++++++++++++++")
                    print("+++++++++++++++++++++++++++++++++++++++++++")
                    print("+++++++++++++++++++++++++++++++++++++++++++")
                    print("+++++++++++++++++++++++++++++++++++++++++++")
                    print("+++++++++++++++++++++++++++++++++++++++++++")
                    print("tenantid ",tenantId)
                    
                    billingSlabResp = search_tl_billing_slab(auth_token,tenantId)
                    if(len(billingSlabResp['billingSlab'])> 0) :
                        print("Check which flow to execute ",billingSlabResp['billingSlab'][0])
                        appFee = int(billingSlabResp['billingSlab'][0]["applicationFee"]) 
                        newTLFlow ="TLWF_Without_AppFee_NewTL.json"
                        renewalTLFlow ="TLWF_Without_AppFee_Renewal.json"
                        if appFee > 0 : 
                            print("Workflow with app fee ")
                            newTLFlow ="TLWF_With_AppFee_NewTL.json"
                            renewalTLFlow ="TLWF_With_AppFee_Renewal.json"

                        else : 
                            print("workflow without app fee")
                        
                        createWorkflow(auth_token, newTLFlow,tenantId)
                        createWorkflow(auth_token, renewalTLFlow,tenantId)

   
                        #break
    dateStr=datetime.now().strftime("%d%m%Y%H%M%S")
    with io.open(os.path.join(config.LOG_PATH,"workflow-request_"+str(dateStr)+".json"), mode="w", encoding="utf-8") as f:
        json.dump(post_data_list, f, indent=2,  ensure_ascii=False, cls=DateTimeEncoder)
    with io.open(os.path.join(config.LOG_PATH,"workflow-response_"+str(dateStr)+".json"), mode="w", encoding="utf-8") as f:
        json.dump(post_data_resp_list, f, indent=2,  ensure_ascii=False, cls=DateTimeEncoder)
    print("OUTPUT FOLDER PATH ",config.LOG_PATH)
            


if __name__ == "__main__":
    main()
