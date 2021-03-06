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

def updateWorkflowSLA(authToken,fileName,tenantId, existingData,fileN):
    print("File Name ",fileName)
    with io.open(fileName, encoding="utf-8") as file : 
        workflow = json.load(file)
        workflow['tenantId']=tenantId 

        ######### modification #########

        with io.open(os.path.join(config.LOG_PATH,"workflow-"+str(tenantId.split(".")[1])+fileN+".json" ), mode="w", encoding="utf-8") as f:
            json.dump(existingData, f, indent=2,  ensure_ascii=False, cls=DateTimeEncoder)
        existingData['businessServiceSla']=workflow['businessServiceSla']

        for index, state in enumerate(existingData["states"]) :
            for masterState in workflow["states"] :
                if masterState["applicationStatus"]==state["applicationStatus"] :
                    state["sla"]=masterState["sla"]
        with io.open(os.path.join(config.LOG_PATH,"workflow-"+str(tenantId.split(".")[1])+fileN+"_m.json"), mode="w", encoding="utf-8") as f:
            json.dump(existingData, f, indent=2,  ensure_ascii=False, cls=DateTimeEncoder)
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
        "BusinessServices": [existingData]}
        url = urljoin(config.HOST, '/egov-workflow-v2/egov-wf/businessservice/_update')
        params = {"tenantId":tenantId}
        data = requests.post(url, params=params, json=jsonObj)
        with io.open(os.path.join(config.LOG_PATH,"workflow-"+str(tenantId.split(".")[1])+fileN+"_m_res.json"), mode="w", encoding="utf-8") as f:
            json.dump(existingData, f, indent=2,  ensure_ascii=False, cls=DateTimeEncoder)
        if(data.status_code == 200):
           print("Workflow updated for ",tenantId ," successfully")
        else : 
            print("Error in workflow creation for ",tenantId)


def updateWorkflow(authToken,fileName,tenantId, existingData,fileN,obsolateStates):
    print("File Name ",fileName)
 
    obsolateAction=[]
    with io.open(fileName, encoding="utf-8") as file : 
        workflow = json.load(file)
        workflow['tenantId']=tenantId 

        ######### modification #########
        print(os.path.join(config.LOG_PATH,"workflow-"+str(tenantId.split(".")[1])+fileN+".json" ))
        with io.open(os.path.join(config.LOG_PATH,"workflow-"+str(tenantId.split(".")[1])+fileN+"_before.json" ), mode="w", encoding="utf-8") as f:
            json.dump(existingData, f, indent=2,  ensure_ascii=False, cls=DateTimeEncoder)
        with io.open(os.path.join(config.LOG_PATH,"workflow-"+str(tenantId.split(".")[1])+fileN+"_master.json" ), mode="w", encoding="utf-8") as f:
            json.dump(workflow, f, indent=2,  ensure_ascii=False, cls=DateTimeEncoder)
        existingData['businessServiceSla']=workflow['businessServiceSla']

        dictForMasterState =dict()
        for state in workflow["states"] :
            dictForMasterState[state["applicationStatus"]] =state 


        dictForExistingState =dict()
        dictForUUIDStates =dict()
        for state in existingData["states"] :
            if state["applicationStatus"] not in dictForMasterState :
                obsolateStates.append( state["uuid"] )   
            else : 
                dictForExistingState[state["applicationStatus"]] =state 
                dictForUUIDStates[state["uuid"]]=state["applicationStatus"]

        
        for masterState in workflow["states"]:
            flagForPrint=False
            if masterState["applicationStatus"] not in dictForExistingState : 
                if "actions" in masterState and  masterState["actions"] is not None : 
                    for masterAction in masterState["actions"] :
                        if masterAction["nextState"] in dictForExistingState :
                            print(dictForExistingState[masterAction["nextState"]])
                            masterAction["nextState"] =dictForExistingState[masterAction["nextState"]]["uuid"]

                existingData["states"].append(masterState) 
            else : 
                state =dictForExistingState[masterState["applicationStatus"]]
                if masterState["applicationStatus"] =="INITIATED" :
                    flagForPrint=True
                state["sla"] =masterState["sla"]
                if "actions" not in state or state["actions"] is None : 
                    state["actions"]=[]
                if "actions" not in masterState or masterState["actions"] is None : 
                    masterState["actions"]=[]
                masterActionList =[]
                for mAction in masterState["actions"] :
                    masterActionList.append(mAction["action"])
                    isActionFound =False
                    if flagForPrint : 
                        print(mAction)
                    for action in state["actions"] :
                        
                        if mAction["action"] ==action["action"]:
                            if flagForPrint :
                                print ("M ",action)
                            isActionFound =True
                            action["roles"]=mAction["roles"]
                            if action["nextState"] not in dictForUUIDStates or dictForUUIDStates[action["nextState"]] !=mAction["nextState"]:
                                action["nextState"]=mAction["nextState"]

                    if not isActionFound : 
                        if mAction["nextState"] in dictForExistingState : 
                            mAction["nextState"] =dictForExistingState[mAction["nextState"]]["uuid"]
                        state["actions"].append(mAction)
                    for action in state["actions"] :
                        if action not in masterActionList and "uuid" in action and action['uuid'] is not None: 
                            print(action)
                            obsolateAction.append(action["uuid"])


                    
             
        print("States which should be deleted manually ",obsolateStates)
        print("Actions which should be deleted manually ",obsolateAction)
        with io.open(os.path.join(config.LOG_PATH,"workflow-"+str(tenantId.split(".")[1])+fileN+"_modified.json"), mode="w", encoding="utf-8") as f:
            json.dump(existingData, f, indent=2,  ensure_ascii=False, cls=DateTimeEncoder)
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
        "BusinessServices": [existingData]}
        url = urljoin(config.HOST, '/egov-workflow-v2/egov-wf/businessservice/_update')
        params = {"tenantId":tenantId}
        data = requests.post(url, params=params, json=jsonObj)
        with io.open(os.path.join(config.LOG_PATH,"workflow-"+str(tenantId.split(".")[1])+fileN+"_m_res.json"), mode="w", encoding="utf-8") as f:
            json.dump(existingData, f, indent=2,  ensure_ascii=False, cls=DateTimeEncoder)
        if(data.status_code == 200):
           print("Workflow updated for ",tenantId ," successfully")
        else : 
            print("Error in workflow creation for ",tenantId)


 
         
         
def main():
    # load default config
    obsolateStates=[]
    print("TENANT_JSON", config.CITY_MODULES_JSON)
    auth_token =superuser_login()["access_token"] 
    config.LOG_PATH=r"D:\workflow"
    with io.open(config.CITY_MODULES_JSON, encoding="utf-8") as f:
        cb_module_data = json.load(f)
    businessService ={"WS" : ["NewWS1" ] , "SW" :["NewSW1" ] }
 
    for found_index, module in enumerate(cb_module_data["citymodule"]):
        if module["module"] in businessService:
            for index, teant in enumerate(module['tenants']) :
                tenantId =teant['code']
                
                for bs in businessService[module["module"]] : 
                    resp =search_Workflow(auth_token,tenantId,bs)

                    if(len(resp['BusinessServices'])== 0) :
                        createWorkflow(auth_token, os.path.join("ws_workflow",bs +str(".json")),tenantId)
                    else : 
                        updateWorkflowSLA(auth_token, os.path.join("ws_workflow",bs +str(".json")),tenantId,resp["BusinessServices"][0],bs  )
                        #updateWorkflow(auth_token, os.path.join("ws_workflow",bs +str(".json")),tenantId,resp["BusinessServices"][0],bs,obsolateStates  )
                propRes =search_Workflow(auth_token,tenantId,"PT.CREATEWITHWNS")
                if(len(propRes['BusinessServices'])== 0) :
                    createWorkflow(auth_token, os.path.join("ws_workflow","createwithWS" +str(".json")),tenantId)

                
                        
                        
    
    with io.open(os.path.join(config.LOG_PATH,"workflow-request_"+str(dateStr)+".json"), mode="w", encoding="utf-8") as f:
        json.dump(post_data_list, f, indent=2,  ensure_ascii=False, cls=DateTimeEncoder)
    with io.open(os.path.join(config.LOG_PATH,"workflow-response_"+str(dateStr)+".json"), mode="w", encoding="utf-8") as f:
        json.dump(post_data_resp_list, f, indent=2,  ensure_ascii=False, cls=DateTimeEncoder)
    print("OUTPUT FOLDER PATH ",config.LOG_PATH)
            
    print("States which should be deleted manually ",obsolateStates)

if __name__ == "__main__":
    main()
