import math
import time
from math import isnan
import io
import os
import numpy
import xlrd as xlrd
import xlwt
from common import superuser_login, open_excel_file, get_sheet, fix_value
from config import config, load_config
import requests
import json
import pandas as pd
#from numpyencoder import NumpyEncoder
#from tlPreprocessor import create_trade_n_accessory_data

def main():
    tenants = [
        "pb.amritsar"
    ]

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
        "No of Beds - Number":"NoBed",
        "Star":"Star",
        "no. of workers":"NoWorker"
    }


    #config.CITY_NAME = tenant.replace(" ", "").replace("pb.", "")
    load_config()

    tenant_id = config.TENANT_ID

    auth_token = superuser_login()["access_token"]

    slabs = requests.post(config.HOST + "/tl-calculator/billingslab/_search?tenantId=" + tenant_id, json={
        "RequestInfo": {
            "authToken": auth_token
        }
    })

    existing_slab_data = {get_slab_id(slab): slab for slab in slabs.json()["billingSlab"]}

    #print(json.dumps(existing_slab_data, indent=2))
    #source_file = config.BASE_PPATH / "source" / "{}.xlsx".format(tenant_id)
    # create_trade_n_accessory_data(tenant_id, source_file, destination_path=config.BASE_PPATH / "source",
    #                             template_file_path="source/template.xlsx")

    #dfs = open_excel_file(config.BASE_PPATH / "source" / "{}.processed.xls".format(tenant_id))
    dfs = open_excel_file(config.TRADE_RATE_WORKBOOK)
    tradeRates = get_sheet(dfs, config.SHEET_TRADERATE)
    # tradeRates = tradeRates.astype(str)
    # tradeRates = tradeRates.infer_objects() 
    # tradeRates = tradeRates.replace(numpy.nan, '', regex=True)
    # tradeRates = tradeRates.fillna('')
    # tradeRates = tradeRates.replace('nan','')
    #category = fix_value(data.iloc[INDEX_TENANT_ULB_NAME][INDEX_CATEGORY])

    # data.fillna(value=0)
    columns = ["tenantid", "id", "licensetype", "structuretype", "tradetype", "accessorycategory", "type", "uom",
            "fromuom", "touom", "rate", "createdtime", "createdby", "lastmodifiedtime", "lastmodifiedby"]
    fields = {field: index for index, field in enumerate([])}
    count=0
    new_slabs = {}
    update_slabs = {}
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
                    slab_data.append(get_slab_object(row,tradeType,"FLAT",None,0,0,rate,applicationFee,"NEW"))
                    slab_data.append(get_slab_object(row,tradeType,"FLAT",None,0,0,rate,applicationFee,"RENEWAL"))
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
                        slab_data.append(get_slab_object(row,tradeType,"FLAT",uom,fromUom,toUom,rate,applicationFee,"NEW"))
                        slab_data.append(get_slab_object(row,tradeType,"FLAT",uom,fromUom,toUom,rate,applicationFee,"RENEWAL"))
            elif row[INDEX_RATE_TYPE] == "Unit by Range":
                uom = uomDict[row[INDEX_UOM]]
                for j in range(0,5):
                    rateIndex = "Rate" +  str(j + 1) 
                    rate = row[rateIndex]
                    if not pd.isna(rate):
                        fromIndex = "RangeFrom" +  str(j + 1)    
                        toIndex = "RangeTo" +  str(j + 1)          
                        fromUom = int(row[fromIndex])
                        toUom = int(row[toIndex])
                        checkforValidData(tradeType,rate,applicationFee,uom,fromUom,toUom) 
                        slab_data.append(get_slab_object(row,tradeType,"RATE",uom,fromUom,toUom,rate,applicationFee,"NEW"))
                        slab_data.append(get_slab_object(row,tradeType,"RATE",uom,fromUom,toUom,rate,applicationFee,"RENEWAL"))
                
    #print(json.dumps(slab_data, indent=2, default=np_encoder))
            

    new_slabs_data = []
    update_slabs_data = []

    for slab_id, row_data in new_slabs.items():
        new_slabs_data.append(get_slab_object(row_data))

    for slab_id, row_data in update_slabs.items():
        update_slabs_data.append(get_slab_object(row_data))

    #print(new_slabs_data, json.dumps(update_slabs_data, indent=2))

    if slab_data:
        print("Post call")
        res = requests.post(config.HOST + "/tl-calculator/billingslab/_create?tenantId={}".format(tenant_id), json={
            "RequestInfo": {
                "authToken": auth_token
            },
            "billingSlab": slab_data
        })

        print(json.dumps(res.json(), indent=2, default=np_encoder))

    if update_slabs_data:
        print("Updating changed billing slabs")
        print(json.dumps(update_slabs_data, indent=2))
        res = requests.post(config.HOST + "/tl-calculator/billingslab/_update?tenantId={}".format(tenant_id), json={
            "RequestInfo": {
                "authToken": auth_token
            },
            "billingSlab": update_slabs_data
        })

        print(json.dumps(res.json(), indent=2, default=np_encoder))


def remove_nan(data, default=None):
    if type(data) in (float, int) and math.isnan(data):
        return default

    if type(data) is str:
        data = data.strip()

    return data


def get_slab_object(row_data,tradeType,type1,uom,fromUom,toUom,rate,applicationFee,newOrRenewal):
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
    fields = ["licenseType", "structureType", "tradeType", "accessoryCategory", "type", "uom", "fromUom", "toUom"]
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