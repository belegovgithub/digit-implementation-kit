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
SRC_LINK="https://13.71.65.215.nip.io"
TGT_IP_LINK=""
SRC_TOKEN=""
TGT_TOKEN=""  #prod auth-token
RETAIN_SAME_SLAB=[]

class DateTimeEncoder(JSONEncoder):
        #Override the default method
        def default(self, obj):
            if isinstance(obj, (date, datetime)):
                return int((obj - epoch).total_seconds() * 1000.0)

def fetchBillingSlabs(tenantid,host,token) : 
    srcbillingSlabs =[]
    slabs = requests.post(host + "/tl-calculator/billingslab/_search?tenantId=" + tenantid, json={
                    "RequestInfo": {
                        "authToken": token
                    }})
    #print(slabs.status_code)
    if slabs.status_code == 200 :
        srcbillingSlabs=slabs.json()["billingSlab"]
    return srcbillingSlabs

def createBillingSlabs(tenantid,host,token,billingSlab):
    createData ={
            "RequestInfo": {
                "authToken": token
            },
            "billingSlab": billingSlab
    } 
    post_data_list.append(createData)
    res = requests.post(host + "/tl-calculator/billingslab/_create?tenantId={}".format(tenantid), json=createData )
    #print(json.dumps(res.json(),indent=2))
   
    if res.status_code ==200 or res.status_code ==201 :
        return res.json()
    else : 
        print("Error in pushing data for CB ",tenantid)

def updateBillingSlabs(tenantid,host,token,billingSlab):
    createData ={
            "RequestInfo": {
                "authToken": token
            },
            "billingSlab": billingSlab
    } 
    post_data_list.append(createData)
    res = requests.post(host + "/tl-calculator/billingslab/_update?tenantId={}".format(tenantid), json=createData )
    #print(json.dumps(res.json(),indent=2))
   
    if res.status_code ==200 or res.status_code ==201 :
        return res.json()
    else : 
        print("Error in pushing data for CB ",tenantid)

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
def main():
    dateStr=datetime.now().strftime("%d%m%Y%H%M%S")
    print("Slab will be copied using available TL module", config.CITY_MODULES_JSON)
    with io.open(config.CITY_MODULES_JSON, encoding="utf-8") as f:
        cb_module_data = json.load(f) 
    for found_index, module in enumerate(cb_module_data["citymodule"]):

        if module["module"]=="TL":
            for index, teant in enumerate(module['tenants']) :
                new_slabs_data = []
                update_slabs_data = []
                old_slab=[]
                tenantId =teant['code']
                cityname=tenantId.split(".")[1]
                if tenantId in RETAIN_SAME_SLAB : 
                    continue
                print("====================",tenantId,"=====================")
                srcbillingSlabs =fetchBillingSlabs(tenantId,SRC_LINK,SRC_TOKEN)
                # with io.open(os.path.join(config.LOG_PATH,cityname+str(dateStr)+"_src_search.json"), mode="w", encoding="utf-8") as f:
                #     json.dump(srcbillingSlabs, f, indent=2,  ensure_ascii=False, cls=DateTimeEncoder)
                
                tgtExistingBillingSlabs =fetchBillingSlabs(tenantId,TGT_IP_LINK,TGT_TOKEN)
                # with io.open(os.path.join(config.LOG_PATH,cityname+str(dateStr)+"_tgt_search.json"), mode="w", encoding="utf-8") as f:
                #     json.dump(tgtExistingBillingSlabs, f, indent=2,  ensure_ascii=False, cls=DateTimeEncoder)
                src_slab_data_dict = {get_slab_id(slab): slab for slab in srcbillingSlabs}
                tgt_slab_data_dict = {get_slab_id(slab): slab for slab in tgtExistingBillingSlabs}
                if len(srcbillingSlabs) > 0  and len(tgtExistingBillingSlabs) > 0 :
                    for item in src_slab_data_dict.keys() : 
                        if item in tgt_slab_data_dict.keys() : 
                            oldData =tgt_slab_data_dict[item]
                            newData=src_slab_data_dict[item]
                            if oldData["rate"]!= newData["rate"] or oldData["applicationFee"]!=newData["applicationFee"] :
                                old_slab.append(tgt_slab_data_dict[item].copy())
                                oldData["rate"]=newData["rate"]
                                oldData["applicationFee"]=newData["applicationFee"]
                                update_slabs_data.append(oldData)
                        else : 
                            new_slabs_data.append(src_slab_data_dict[item])
                count =len(update_slabs_data)+len(new_slabs_data)  
                if count > 0 and len(srcbillingSlabs)  !=count:
                    print ("THIS CB IS HAVING ISSUE",tenantId)
                if len(new_slabs_data) > 0 :
                    with io.open(os.path.join(config.LOG_PATH,cityname+str(dateStr)+"_billingslab_create_req.json"), mode="w", encoding="utf-8") as f:
                        json.dump(new_slabs_data, f, indent=2,  ensure_ascii=False, cls=DateTimeEncoder)
                    resp = createBillingSlabs(tenantId,TGT_IP_LINK,TGT_TOKEN,new_slabs_data)
                    with io.open(os.path.join(config.LOG_PATH,cityname+str(dateStr)+"_billingslab_create_res.json"), mode="w", encoding="utf-8") as f:
                        json.dump(resp, f, indent=2,  ensure_ascii=False, cls=DateTimeEncoder)
                if len(update_slabs_data) > 0 : 
                    with io.open(os.path.join(config.LOG_PATH,cityname+str(dateStr)+"_billingslab_before_update.json"), mode="w", encoding="utf-8") as f:
                        json.dump(old_slab, f, indent=2,  ensure_ascii=False, cls=DateTimeEncoder)
                    with io.open(os.path.join(config.LOG_PATH,cityname+str(dateStr)+"_billingslab_after_update_req.json"), mode="w", encoding="utf-8") as f:
                        json.dump(update_slabs_data, f, indent=2,  ensure_ascii=False, cls=DateTimeEncoder)
                    resp = updateBillingSlabs(tenantId,TGT_IP_LINK,TGT_TOKEN,update_slabs_data)
                    with io.open(os.path.join(config.LOG_PATH,cityname+str(dateStr)+"_billingslab_after_update_res.json"), mode="w", encoding="utf-8") as f:
                        json.dump(update_slabs_data, f, indent=2,  ensure_ascii=False, cls=DateTimeEncoder)
 

 
                
if __name__ == "__main__":
    main()
