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
dateStr=datetime.now().strftime("%d%m%Y%H%M%S")
class DateTimeEncoder(JSONEncoder):
        #Override the default method
        def default(self, obj):
            if isinstance(obj, (date, datetime)):
                return int((obj - epoch).total_seconds() * 1000.0)
def createWorkflow(authToken,fileName,tenantId):
    with io.open(fileName, encoding="utf-8") as file : 
        workflow = json.load(file)
        workflow['tenantId']=tenantId 
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
    config.LOG_PATH=r"D:\workflow"
    with io.open(config.CITY_MODULES_JSON, encoding="utf-8") as f:
        cb_module_data = json.load(f)
    businessService ={"WS" : ["NewWS1","ModifyWSConnection"] , "SW" :["NewSW1","ModifySWConnection"] }
 
    for found_index, module in enumerate(cb_module_data["citymodule"]):
        if module["module"] in businessService:
            for index, teant in enumerate(module['tenants']) :
                tenantId =teant['code']
                
                for bs in businessService[module["module"]] : 
                    resp =search_Workflow(auth_token,tenantId,bs)

                    if(len(resp['BusinessServices'])== 0) :
                        createWorkflow(auth_token, os.path.join("ws_workflow",bs +str(".json")),tenantId)
                propRes =search_Workflow(auth_token,tenantId,"PT.CREATEWITHWNS")
                if(len(propRes['BusinessServices'])== 0) :
                    createWorkflow(auth_token, os.path.join("ws_workflow","createwithWS" +str(".json")),tenantId)

                
                        
                        
    
    with io.open(os.path.join(config.LOG_PATH,"workflow-request_"+str(dateStr)+".json"), mode="w", encoding="utf-8") as f:
        json.dump(post_data_list, f, indent=2,  ensure_ascii=False, cls=DateTimeEncoder)
    with io.open(os.path.join(config.LOG_PATH,"workflow-response_"+str(dateStr)+".json"), mode="w", encoding="utf-8") as f:
        json.dump(post_data_resp_list, f, indent=2,  ensure_ascii=False, cls=DateTimeEncoder)
    print("OUTPUT FOLDER PATH ",config.LOG_PATH)
            


if __name__ == "__main__":
    main()
