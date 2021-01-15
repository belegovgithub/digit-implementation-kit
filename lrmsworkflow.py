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
RETAIN_SAME_SLAB=[ ] 
dateStr=datetime.now().strftime("%d%m%Y%H%M%S")
ROLE_MAPPING ={"pb.agra":"DEO_AGRA","pb.mathura":"DEO_AGRA","pb.allahabad":"DEO_ALLAHABAD","pb.faizabad":"DEO_ALLAHABAD","pb.varanasi":"DEO_ALLAHABAD","pb.almora":"DEO_BAREILLY","pb.bareilly":"DEO_BAREILLY","pb.nainital":"DEO_BAREILLY","pb.ranikhet":"DEO_BAREILLY","pb.shahjahanpur":"DEO_BAREILLY","pb.danapur":"DEO_DANAPUR","pb.ramgarh":"DEO_DANAPUR","pb.jabalpur":"DEO_JABALPUR","pb.pachmarhi":"DEO_JABALPUR","pb.fatehgarh":"DEO_LUCKNOW","pb.kanpur":"DEO_LUCKNOW","pb.lucknow":"DEO_LUCKNOW","pb.chakrata":"DEO_MEERUT","pb.clementtown":"DEO_MEERUT","pb.dehradun":"DEO_MEERUT","pb.landour":"DEO_MEERUT","pb.lansdowne":"DEO_MEERUT","pb.meerut":"DEO_MEERUT","pb.roorkee":"DEO_MEERUT","pb.mhow":"DEO_MHOW","pb.shillong":"DEO_GUWAHATI","pb.barrackpore":"DEO_KOLKATA","pb.jalapahar":"DEO_SILIGURI","pb.lebong":"DEO_SILIGURI","pb.badamibagh":"DEO_KASHMIR","pb.ahmedabad":"DEO_AHMEDABAD","pb.belgaum":"DEO_BANGALORE","pb.babina":"DEO_BHOPAL","pb.jhansi":"DEO_BHOPAL","pb.morar":"DEO_BHOPAL","pb.saugor":"DEO_BHOPAL","pb.stm":"DEO_CHENNAI","pb.wellington":"DEO_CHENNAI","pb.cannanore":"DEO_COCHIN","pb.ajmer":"DEO_JODHPUR","pb.nasirabad":"DEO_JODHPUR","pb.deolali":"DEO_MUMBAI","pb.kamptee":"DEO_MUMBAI","pb.ahmednagar":"DEO_PUNE","pb.aurangabad":"DEO_PUNE","pb.dehuroad":"DEO_PUNE","pb.kirkee":"DEO_PUNE","pb.pune":"DEO_PUNE","pb.secunderabad":"DEO_SECUNDERABAD","pb.ambala":"DEO_AMBALA","pb.dagshai":"DEO_AMBALA","pb.jutogh":"DEO_AMBALA","pb.kasauli":"DEO_AMBALA","pb.subathu":"DEO_AMBALA","pb.delhi":"DEO_DELHI","pb.amritsar":"DEO_JALANDHAR","pb.ferozepur":"DEO_JALANDHAR","pb.jalandhar":"DEO_JALANDHAR","pb.jammu":"DEO_JAMMU","pb.bakloh":"DEO_PATHANKOT","pb.dalhousie":"DEO_PATHANKOT","pb.khasyol":"DEO_PATHANKOT","pb.testing":"DEO_TESTING"}

def updateFile (authToken,fileName,tenantId) :
    fin = open("LAMS_NewLR_DEO_V3.json", "rt")
    fout = open(os.path.join("lrms-deo","LAMS_NewLR_DEO_V3_"+tenantId.split(".")[1]+".json"), "wt")
    #for each line in the input file
    for line in fin:
        #read replace the string and write to output file
        fout.write(line.replace("LR_APPROVER_DEO", ROLE_MAPPING[tenantId]))
    #close input and output files
    fin.close()
    fout.close()

class DateTimeEncoder(JSONEncoder):
        #Override the default method
        def default(self, obj):
            if isinstance(obj, (date, datetime)):
                return int((obj - epoch).total_seconds() * 1000.0)
def createWorkflow_ceo(authToken,fileName,tenantId):
    with io.open(fileName, encoding="utf-8") as file : 
        workflow = json.load(file)
        workflow['tenantId']=tenantId
        #print("Workflow",workflow)
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
        #print(json.dumps(jsonObj, indent=2))
        post_data_list.append(jsonObj)
        url = urljoin(config.HOST, '/egov-workflow-v2/egov-wf/businessservice/_create')
        params = {"tenantId": config.TENANT_ID}
        data = requests.post(url, params=params, json=jsonObj)
        if(data.status_code == 200):
            print("Workflow created for ",tenantId ," successfully")
        else : 
            print("Error in workflow creation for ",tenantId )
        post_data_resp_list.append(data.json()) 
def createWorkflow(authToken,fileName,tenantId):
    with io.open(os.path.join("lrms-deo","LAMS_NewLR_DEO_V3_"+tenantId.split(".")[1]+".json"), encoding="utf-8") as file : 
        workflow = json.load(file)
        workflow['tenantId']=tenantId
        #print("Workflow",workflow)
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
        #print(json.dumps(jsonObj, indent=2))
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
    auth_token = superuser_login()["access_token"] 
 

    with io.open(config.TENANT_JSON, encoding="utf-8") as f:
        cb_module_data = json.load(f)
        #print(cb_module_data  )
    for found_index, module in enumerate(cb_module_data["tenants"]):
        if module["city"]["ulbGrade"]!="ST":
            print(module["code"]) 
            if True : 
                tenantId =module['code']
                if tenantId in RETAIN_SAME_SLAB : 
                    continue
                flowA="LAMS_NewLR_CEO_V3.json"
                flowB="LAMS_NewLR_DEO_V3.json"
                



                resp =search_Workflow(auth_token,tenantId,"LAMS_NewLR_DEO_V3")
                #print(resp) 

                if(len(resp['BusinessServices'])==0) :
                    print("+++++++++++++++++++++++++++++++++++++++++++")
                    print("+++++++++++++++++++++++++++++++++++++++++++")
                    print("+++++++++++++++++++++++++++++++++++++++++++")
                    print("+++++++++++++++++++++++++++++++++++++++++++")
                    print("+++++++++++++++++++++++++++++++++++++++++++")
                    print("tenantid ",tenantId)
                    try : 
                        updateFile(auth_token,flowB,tenantId)
                        createWorkflow_ceo(auth_token, flowA,tenantId)
                        createWorkflow(auth_token, flowB,tenantId)

                    except Exception as e : 
                        print("error ",e)
                 
                    
                    
    
    with io.open(os.path.join(config.LOG_PATH,"lrms-workflow-request_"+str(dateStr)+".json"), mode="w", encoding="utf-8") as f:
        json.dump(post_data_list, f, indent=2,  ensure_ascii=False, cls=DateTimeEncoder)
    with io.open(os.path.join(config.LOG_PATH,"lrms-workflow-response_"+str(dateStr)+".json"), mode="w", encoding="utf-8") as f:
        json.dump(post_data_resp_list, f, indent=2,  ensure_ascii=False, cls=DateTimeEncoder)
    print("OUTPUT FOLDER PATH ",config.LOG_PATH)
            


if __name__ == "__main__":
    main()
