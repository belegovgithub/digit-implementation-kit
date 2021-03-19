import math
import time
from math import isnan
import io
import os
import numpy
import xlrd as xlrd
import xlwt
from common import superuser_login, open_excel_file, get_sheet, fix_value,DateTimeEncoder
from config import config, load_config
import requests
import json
import pandas as pd
from datetime import datetime, timedelta
#from numpyencoder import NumpyEncoder
#from tlPreprocessor import create_trade_n_accessory_data
import numpy as np
import copy 

"""
Check TL Billing slabs , 
If billing slab values are not properly defined or overlapped exist between billing slab then it will save such billing slab in file 
"""    
def bilingWithIssues():
    dateStr=datetime.now().strftime("%d%m%Y%H%M%S")
    auth_token = superuser_login()["access_token"]
    print(auth_token)
    print("Slab will be copied using available TL module", config.CITY_MODULES_JSON)
    with io.open(config.CITY_MODULES_JSON, encoding="utf-8") as f:
        cb_module_data = json.load(f) 
    issueWithBilling ={}

    for found_index, module in enumerate(cb_module_data["citymodule"]):

        if module["module"]=="TL":
            for index, teant in enumerate(module['tenants']) :
                new_slabs_data = []
                update_slabs_data = []
                old_slab=[]
                tenantId =teant['code']
                cityname=tenantId.split(".")[1]
                print("====================",tenantId,"=====================")
                respOfBilling = requests.post(config.HOST + "/tl-calculator/billingslab/_search?tenantId=" + tenantId, json={
                    "RequestInfo": {
                        "authToken": auth_token
                    }
                })
                srcbillingSlabs=respOfBilling.json()["billingSlab"]
                #srcbillingSlabs = list(filter(lambda x: (x["applicationType"] == "NEW"), srcbillingSlabs))    
                existing_slab_data =dictSlabObject(srcbillingSlabs)
                #print(os.path.join(config.LOG_PATH,cityname+str(dateStr)+"_mappingOfExistingSlab.json"))
                with io.open(os.path.join(config.LOG_PATH,cityname+str(dateStr)+"_mappingOfExistingSlab.json"), mode="w", encoding="utf-8") as f:
                    json.dump(existing_slab_data, f, indent=2,  ensure_ascii=False, cls=DateTimeEncoder)    
                for key in existing_slab_data : 
                    billingSlabs = existing_slab_data[key]
                    uom =None 
                    uomEnd =None 
                    isError =False
                    for slab in billingSlabs : 
                        if uom is None : 
                            uom =slab["uom"]
                        elif uom != slab["uom"] :
                            print("Billing Slab is having issue")
                            isError=True
                            print(tenantId +"|"+key)
                            print("Error not same")
                        if uom is not None :                            
                            fromUom = slab["fromUom"]
                            toUom = slab["toUom"]
                            #print(fromUom,toUom, uomEnd)
                            #print(type(fromUom),type(toUom), type(uomEnd))
                            if fromUom >= toUom :
                                isError=True
                                print("FROM IS BIGGER THAN TO RANGE")
                                print((tenantId +"|"+key))
                            if uomEnd is None : 
                                uomEnd = toUom          
                            elif uomEnd !=fromUom :
                                print("RANGE OVERLAPPED ", (tenantId +"|"+key))
                                isError=True
                            uomEnd = toUom
                    if isError : 
                        if tenantId not in issueWithBilling : 
                            issueWithBilling[tenantId]={}
                        issueWithBilling[tenantId][key]=existing_slab_data[key]
        
    print("Billing With Issue : ",os.path.join(config.LOG_PATH, "BillingWithIssue.json"))
    with io.open(os.path.join(config.LOG_PATH, "BillingWithIssue.json"), mode="w", encoding="utf-8") as f:
        json.dump(issueWithBilling, f, indent=2,  ensure_ascii=False, cls=DateTimeEncoder)   



"""
Approach : 

1. Read billing slab from db
2. Create dict object for unique billing id and corresponding object array : NEW|TRADE.OTHERS.E52 :[Sorted Array based on fromUOm]
3. Parse excel and create the billing slab
4. Convert excel based billing slab to same dict array as of step 2. 
5. Now start iterating the new billing slab 
    5.1 If old and new billing slab object count is same then simply update the full object 
    5.2 if old_dict_key_array is less than new_dict_key_array then also copy ( update old and copy new )
    5.3 if old_key_array > new_dict_key_array then raise it as issue
6. Based on updated objects call update function

"""


def main():
    UPDATE_EVEN_SAME_DATA =True
    dateStr=''#datetime.now().strftime("%d%m%Y%H%M%S")
    INDEX_CATEGORY = 1
    INDEX_SLNO = 2
    INDEX_SUB_CATEGORY = 3
    INDEX_TRADE_APPLICABLE = 4
    INDEX_UOM = 5
    INDEX_RATE_TYPE = 6
    INDEX_RANGE1_FROM = 7
    INDEX_RANGE1_TO = 8
    INDEX_RANGE1_RATE = 9
    INDEX_RANGE2_FROM = 10
    INDEX_RANGE2_TO = 11
    INDEX_RANGE2_RATE = 12
    INDEX_RANGE3_FROM = 13
    INDEX_RANGE3_TO = 14
    INDEX_RANGE3_RATE = 15
    INDEX_RANGE4_FROM = 16
    INDEX_RANGE4_TO = 17
    INDEX_RANGE4_RATE = 18
    INDEX_RANGE5_FROM = 19
    INDEX_RANGE5_TO = 20
    INDEX_RANGE5_TO = 21
    INDEX_APPLICATION_FEE = 22

    CategoryDict = {
        "Eating Establishments": "EATING",
        "Veterinary Trades & trades dealing with animal products": "VETERINARY",
        "Medical Establishments": "MEDICAL",
        "Flammables": "DANGEROUS",
        "Small Scale Industries/Small & Medium factories": "MEDIUM",
        "Other Establishment/Offices (Non eating/non medical)": "OTHERS"        
    }
    uomDict = {
        "Flat/Fixed":None,
        "Area- per -Sq Ft":"SqFt",
        "Motor Power - HP":"MoHP",
        "No of Beds - Number":"Bed",
        "Star":"Star",
        "no. of workers":"Worker",
        "No. of category":"Category"
    }


    #config.CITY_NAME = tenant.replace(" ", "").replace("pb.", "")
    load_config()

    tenant_id = config.TENANT_ID

    auth_token = superuser_login()["access_token"]
    print(auth_token)
     


    slabs = requests.post(config.HOST + "/tl-calculator/billingslab/_search?tenantId=" + tenant_id, json={
        "RequestInfo": {
            "authToken": auth_token
        }
    })
    #print(json.dumps(slabs.json()["billingSlab"], indent=2))
    with io.open(os.path.join(config.LOG_PATH,config.CITY_NAME+str(datetime.now().strftime("%d%m%Y%H%M%S"))+"_billingslab_search_resp.json"), mode="w", encoding="utf-8") as f:
        json.dump(slabs.json()["billingSlab"], f, indent=2,  ensure_ascii=False, cls=DateTimeEncoder)
    result = slabs.json()["billingSlab"]

    
    #result = list(filter(lambda x: (x["applicationType"] == "NEW"), slabs.json()["billingSlab"]))    
    existing_slab_data =dictSlabObject(result)
    with io.open(os.path.join(config.LOG_PATH,config.CITY_NAME+str(dateStr)+"_mappingOfExistingSlab.json"), mode="w", encoding="utf-8") as f:
        json.dump(existing_slab_data, f, indent=2,  ensure_ascii=False, cls=DateTimeEncoder)    
    
     
    dfs = open_excel_file(config.TRADE_RATE_WORKBOOK)
    tradeRates = get_sheet(dfs, config.SHEET_TRADERATE)
     

    # data.fillna(value=0)
    columns = ["tenantid", "id", "licensetype", "structuretype", "tradetype", "accessorycategory", "type", "uom",
            "fromuom", "touom", "rate", "createdtime", "createdby", "lastmodifiedtime", "lastmodifiedby"]
    fields = {field: index for index, field in enumerate([])}
    count=0
    slabs_processed = set()
    slab_data = []
    for i in range(len(tradeRates)) :
        if tradeRates.iloc[i, INDEX_TRADE_APPLICABLE] == "Applicable":
            row = tradeRates.iloc[i]
            tradeType = getTradeCategory(row[INDEX_CATEGORY], row[INDEX_SLNO])
            #print(pd.isna(row[INDEX_RATE_TYPE] ))
            applicationFee = row[INDEX_APPLICATION_FEE]            
            if pd.isna(row[INDEX_RATE_TYPE] ):
                for j in range(0,5): 
                    rateIndex = "Rate" +  str(j + 1) 
                    rate = str(row[rateIndex])
                    fromIndex = "RangeFrom" + str(j + 1)     
                    toIndex = "RangeTo" + str(j + 1)                                  
                    fromUom = row[fromIndex]
                    toUom = row[toIndex]   
                    checkforValidData(tradeType,rate,applicationFee)                     
                    slab_data.append(constructSlabObject(row,tradeType,"FLAT",None,0,0,rate,applicationFee,"NEW"))
                    slab_data.append(constructSlabObject(row,tradeType,"FLAT",None,0,0,rate,applicationFee,"RENEWAL"))
                    break
            elif row[INDEX_RATE_TYPE] == "Flat by Range":
                uom = uomDict[row[INDEX_UOM]]
                for j in range(0,5): 
                    rateIndex = "Rate" +  str(j + 1) 
                    rate = row[rateIndex]
                    if not pd.isna(rate):                         
                        fromIndex = "RangeFrom" + str(j + 1)   
                        toIndex = "RangeTo" +  str(j + 1)                                     
                        fromUom = row[fromIndex]
                        toUom = row[toIndex]   
                        checkforValidData(tradeType,rate,applicationFee,uom,fromUom,toUom)                              
                        slab_data.append(constructSlabObject(row,tradeType,"FLAT",uom,fromUom,toUom,rate,applicationFee,"NEW"))
                        slab_data.append(constructSlabObject(row,tradeType,"FLAT",uom,fromUom,toUom,rate,applicationFee,"RENEWAL"))
            elif row[INDEX_RATE_TYPE] == "Unit by Range":
                uom = uomDict[row[INDEX_UOM]]
                for j in range(0,5):
                    rateIndex = "Rate" +  str(j + 1) 
                    rate = row[rateIndex]
                    if not pd.isna(rate):
                        fromIndex = "RangeFrom" +  str(j + 1)    
                        toIndex = "RangeTo" +  str(j + 1)          
                        fromUom = (row[fromIndex])
                        toUom = (row[toIndex])
                        checkforValidData(tradeType,rate,applicationFee,uom,fromUom,toUom) 
                        slab_data.append(constructSlabObject(row,tradeType,"RATE",uom,fromUom,toUom,rate,applicationFee,"NEW"))
                        slab_data.append(constructSlabObject(row,tradeType,"RATE",uom,fromUom,toUom,rate,applicationFee,"RENEWAL"))
                
    with io.open(os.path.join(config.LOG_PATH,config.CITY_NAME+str(dateStr)+"_excelSlabData.json"), mode="w", encoding="utf-8") as f:
        json.dump(slab_data, f, indent=2,  ensure_ascii=False, cls=DateTimeEncoder)
    newSlabs =dictSlabObject(slab_data)
    with io.open(os.path.join(config.LOG_PATH,config.CITY_NAME+str(dateStr)+"_mappingOfNewSlab.json"), mode="w", encoding="utf-8") as f:
        json.dump(newSlabs, f, indent=2,  ensure_ascii=False, cls=DateTimeEncoder)    
            
 
    new_slabs_data=[]
    keysHavingIssue =[]  
    update_slabs_data_old=[]
    update_slabs_data=[]
    for key in newSlabs : 
        # if key !='NEW|TRADE.EATING.A1' :
        #     continue
        if key in existing_slab_data :
            if len(existing_slab_data[key]) != len(newSlabs[key]) : 
                if len(existing_slab_data[key]) <= len(newSlabs[key]) : 
                    update_slabs_data_old.extend(existing_slab_data[key])
                    updatedData , newData = syncBillingSlab(existing_slab_data,newSlabs,key, False)
                    update_slabs_data.extend(updatedData)
                    new_slabs_data.extend( newData)
                else : 
                    print("ISSUE ", key  , " ",len(existing_slab_data[key]),"--",len(newSlabs[key]))
                    keysHavingIssue.append(key)
            else : 
                update_slabs_data_old.extend(copy.deepcopy(existing_slab_data[key]))
                updatedData , newData = syncBillingSlab(existing_slab_data,newSlabs,key, False)
                update_slabs_data.extend(updatedData)
                new_slabs_data.extend( newData)
        else : 
            new_slabs_data.extend( newSlabs[key])
    print(keysHavingIssue)
   
    with io.open(os.path.join(config.LOG_PATH,config.CITY_NAME+str(dateStr)+"old.json"), mode="w", encoding="utf-8") as f:
        json.dump(update_slabs_data_old, f, indent=2,  ensure_ascii=False, cls=DateTimeEncoder)    
    with io.open(os.path.join(config.LOG_PATH,config.CITY_NAME+str(dateStr)+"updated.json"), mode="w", encoding="utf-8") as f:
        json.dump(update_slabs_data, f, indent=2,  ensure_ascii=False, cls=DateTimeEncoder)     
    with io.open(os.path.join(config.LOG_PATH,config.CITY_NAME+str(dateStr)+"new.json"), mode="w", encoding="utf-8") as f:
        json.dump(new_slabs_data, f, indent=2,  ensure_ascii=False, cls=DateTimeEncoder ) 
 
     
     
    if len(new_slabs_data)>0:
        print("Post call")
        res = requests.post(config.HOST + "/tl-calculator/billingslab/_create?tenantId={}".format(tenant_id), json={
            "RequestInfo": {
                "authToken": auth_token
            },
            "billingSlab": new_slabs_data
        })
        with io.open(os.path.join(config.LOG_PATH,config.CITY_NAME+str(dateStr)+"_billingslab_new_res.json"), mode="w", encoding="utf-8") as f:
            json.dump(res.json(), f, indent=2,  ensure_ascii=False, cls=DateTimeEncoder)


 
    if len(update_slabs_data)>0:
        print("Updating changed billing slabs")
        res = requests.post(config.HOST + "/tl-calculator/billingslab/_update?tenantId={}".format(tenant_id), json={
            "RequestInfo": {
                "authToken": auth_token
            },
            "billingSlab": update_slabs_data
        })
        with io.open(os.path.join(config.LOG_PATH,config.CITY_NAME+str(dateStr)+"_billingslab_update_res.json"), mode="w", encoding="utf-8") as f:
            json.dump(res.json(), f, indent=2,  ensure_ascii=False, cls=DateTimeEncoder)
 
"""
Sync billing slab update old object with new values and if old slab not exist then copy it in different array
"""
def syncBillingSlab(existing_slab_data, newSlabs,key,pushEvenSameData =True) :
    #print(key, len(existing_slab_data[key]), len(newSlabs[key]))
    keyset =["type","uom","fromUom","toUom","rate","applicationFee"]
    updatedCopy=[]
    newData =[]
    for index in range(0, len(existing_slab_data[key])) :
        old =existing_slab_data[key][index]
        new =newSlabs[key][index]
        isSame =True
        for attrKey in keyset : 
            oldAttr = old[attrKey]
            newAttr = new[attrKey]
            if (type(old[attrKey]) is float  or (type(old[attrKey]) is int )) :
                oldAttr = float(old[attrKey])
                newAttr = float(new[attrKey])
            if old[attrKey]!=new[attrKey] :
                isSame =False
        if pushEvenSameData : 
            isSame =False
        if not isSame :
            for attrKey in keyset : 
                if (type(old[attrKey]) is float  or (type(old[attrKey]) is int )) :
                    old[attrKey] =float(new[attrKey] )
                else : 
                    old[attrKey] = new[attrKey] 
            updatedCopy.append(old)
        else : 
            print("Retain same",key)
    for index in range(len(existing_slab_data[key]), len(newSlabs[key])) : 
        newData.append(newSlabs[key][index])
    return updatedCopy ,newData    


def remove_nan(data, default=None):
    if type(data) in (float, int) and math.isnan(data):
        return default

    if type(data) is str:
        data = data.strip()

    return data

 
def dictSlabObject(slabObj) :
    mapObj ={}
    for ele in slabObj : 
        keyOfSlab =get_slab_id(ele) 
        if keyOfSlab not in mapObj : 
            mapObj[keyOfSlab]=[]
        mapObj[keyOfSlab].append(ele)
    for key in mapObj : 
        mapObj[key].sort(reverse=False, key=lambda e: (e['fromUom'],e['toUom'])) 
    return mapObj



def constructSlabObject(row_data,tradeType,type1,uom,fromUom,toUom,rate,applicationFee,newOrRenewal):
    data = {
        "tenantId": config.TENANT_ID,
        "licenseType": "PERMANENT",
        "structureType": "IMMOVABLE.PUCCA",
        "tradeType": remove_nan(tradeType),
        "accessoryCategory": None,
        "type": remove_nan(type1),
        "uom": remove_nan(uom),
        "fromUom": int(remove_nan(fromUom)),
        "toUom": int(remove_nan(toUom)),
        "rate": float(remove_nan(rate, default=0.0)),
        "applicationType": newOrRenewal,
        "applicationFee": float(remove_nan(applicationFee, default=0.0))
    }
    
    if "id" in row_data and type(row_data['id']) is str and len(row_data["id"]) > 6:
        data["id"] = row_data["id"]

    return data
    
 


def get_slab_id(slab):
    fields = ["applicationType",  "tradeType"]
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

def checkforValidData(tradeType,rate,applicationFee,uom=None,fromUom=0,toUom=0): 
    if(pd.isna(rate)):
        raise SystemExit("rate is not entered for trade type ",  str(tradeType))
    if(pd.isna(applicationFee)):
        raise SystemExit("Application Fee is not entered ",  str(tradeType))
    if(pd.isna(fromUom)):
        raise SystemExit("fromUom is not entered ",  str(tradeType))
    if(pd.isna(toUom)):
        raise SystemExit("toUom is not entered ",  str(tradeType))

def getTradeCategory(keyword,subType):
  #print("keyword--",keyword,int(float(subType)))
  global letter
  subType = str(int(subType))
  keyword = str(keyword)
  tradeType_category = "TRADE"
  if keyword.find("Eating") != -1:
    letter = tradeType_category+"."+"EATING"+"."+"A"+subType
  elif keyword.find("Medical") != -1:
    letter = tradeType_category+"."+ "MEDICAL"+"."+"B"+subType
  elif keyword.find("Veterinary") != -1:
    letter =tradeType_category+"."+"VETERINARY"+"."+"C"+subType
  elif keyword.find("Flammables") != -1:
    letter =tradeType_category+"."+"DANGEROUS"+"."+"D"+subType
  elif keyword.find("Medium") != -1:
    letter =tradeType_category+"."+"MEDIUM"+"."+"F"+subType
  elif keyword.find("Offices ") != -1:
    letter =tradeType_category+"."+"OTHERS"+"."+"E"+subType
  #print(letter)
  return letter

def np_encoder(object):
    if isinstance(object, numpy.generic):
        return numpy.asscalar(object)



if __name__ == "__main__":
    main()
    #bilingWithIssues()