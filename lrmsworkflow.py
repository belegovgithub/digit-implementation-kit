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
RETAIN_SAME_SLAB=["pb.agra","pb.delhi","pb.pune","pb.testing","pb.secunderabad","pb.lucknow"]
LOG_PATH=r"D:\CB\Verified-CB-Data"
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
    print("TENANT_JSON", config.TENANT_JSON)
    auth_token = "ef9d6e42-526c-4c29-8e70-6d27a9694aef"#superuser_login()["access_token"] 
 

    with io.open(config.TENANT_JSON, encoding="utf-8") as f:
        cb_module_data = json.load(f)
        print(cb_module_data  )
    for found_index, module in enumerate(cb_module_data["tenants"]):
        if module["city"]["ulbGrade"]!="ST":
            print(module["code"]) 
            if True : 
                tenantId =module['code']
                if tenantId in RETAIN_SAME_SLAB : 
                    continue
                flowA="LAMS_NewLR_CEO_V3.json"
                flowB="LAMS_NewLR_DEO_V3.json"
                
                resp =search_Workflow(auth_token,tenantId,"LAMS_NewLR_CEO_V3")
                print(resp) 
                if(len(resp['BusinessServices'])==0) :
                    print("+++++++++++++++++++++++++++++++++++++++++++")
                    print("+++++++++++++++++++++++++++++++++++++++++++")
                    print("+++++++++++++++++++++++++++++++++++++++++++")
                    print("+++++++++++++++++++++++++++++++++++++++++++")
                    print("+++++++++++++++++++++++++++++++++++++++++++")
                    print("tenantid ",tenantId)
                    createWorkflow(auth_token, flowA,tenantId)
                    createWorkflow(auth_token, flowB,tenantId)
                    
    dateStr=datetime.now().strftime("%d%m%Y%H%M%S")
    with io.open(os.path.join(LOG_PATH,"lrms-workflow-request_"+str(dateStr)+".json"), mode="w", encoding="utf-8") as f:
        json.dump(post_data_list, f, indent=2,  ensure_ascii=False, cls=DateTimeEncoder)
    with io.open(os.path.join(LOG_PATH,"lrms-workflow-response_"+str(dateStr)+".json"), mode="w", encoding="utf-8") as f:
        json.dump(post_data_resp_list, f, indent=2,  ensure_ascii=False, cls=DateTimeEncoder)
    print("OUTPUT FOLDER PATH ",LOG_PATH)
            


if __name__ == "__main__":
    main()
