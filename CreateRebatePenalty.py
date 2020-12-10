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
 
def main():
    # load default config
    print("TENANT_JSON", config.CITY_MODULES_JSON)
    #auth_token = superuser_login()["access_token"] 
 
    with io.open("Rebate.json", encoding="utf-8") as file : 
        rebateData = json.load(file)
    with io.open("Penalty.json", encoding="utf-8") as file : 
        penaltyData = json.load(file)
        

    with io.open(config.CITY_MODULES_JSON, encoding="utf-8") as f:
        cb_module_data = json.load(f)
        print(cb_module_data["citymodule"] )
    for found_index, module in enumerate(cb_module_data["citymodule"]):
        if module["module"]=="TL":
            #print("index ",found_index,"  tenant ",module['tenants'])
            for index, teant in enumerate(module['tenants']) :
                tenantId =teant['code']
                print(tenantId,tenantId.split("."))
                path = os.path.join( config.MDMS_LOCATION, tenantId.split(".")[1],"TradeLicense")
                if os.path.exists(os.path.join( path,"Rebate.json")) : 
                    continue 
                
                if not os.path.exists(path) : 
                    os.makedirs(path)
                
                penaltyData["tenantId"]=tenantId
                rebateData["tenantId"]=tenantId
                with io.open(os.path.join(path,"Rebate.json"), mode="w", encoding="utf-8") as f:
                    json.dump(rebateData, f, indent=2,  ensure_ascii=False, cls=DateTimeEncoder)
                with io.open(os.path.join(path,"Penalty.json"), mode="w", encoding="utf-8") as f:
                    json.dump(penaltyData, f, indent=2,  ensure_ascii=False, cls=DateTimeEncoder)
                #break
                
    
            


if __name__ == "__main__":
    main()
