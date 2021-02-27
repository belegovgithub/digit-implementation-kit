import requests
import csv
from common import *
from config import config ,load_employee_creation_config
from common import superuser_login
from config import config
import io
import os
import numpy
import pandas as pd
import openpyxl
from datetime import datetime, timedelta
from math import isnan

# import shutil
# import xlrd
# import requests
# import xlwt
# from xlwt import Workbook
#import xlsxwriter

def main():
    Flag =False
    tenantMapping={}
    post_data_resp_list=[]

    with io.open(config.TENANT_JSON, encoding="utf-8") as f:
        cb_module_data = json.load(f)
        for found_index, module in enumerate(cb_module_data["tenants"]):
            if module["city"]["ulbGrade"]=="ST":
                continue
            data = []
            
            tenant_id=module["code"]
            cityname = tenant_id.lower()[3:]
            #cityname = "ahmednagar"
            boundary_path = os.path.join(config.MDMS_LOCATION ,  cityname , "egov-location")
            template_file = os.path.join(config.LOG_PATH ,  "Locality.xlsx" )
            print(cityname)
            
            if os.path.isfile(os.path.join(boundary_path , "boundary-data.json")):
                with open(os.path.join(boundary_path , "boundary-data.json")) as f:
                    existing_boundary_data = json.load(f)
            found = False
            for tenantboundary in existing_boundary_data["TenantBoundary"]:                
                for tenant_boundary in tenantboundary["boundary"]["children"]:
                    for t1 in tenant_boundary["children"]:
                        for t2 in t1["children"]:
                            data.append([t2["name"],t2["code"]])
                            #print(json.dumps(t1, indent = 2))
            df = pd.DataFrame(data,columns=['Locality Name','Code'])
            # df.to_excel(template_file,sheet_name=cityname,index=False)
            workbook1 = openpyxl.load_workbook(template_file)
            writer = pd.ExcelWriter(template_file, engine='openpyxl')   
            writer.book = workbook1        
            df.to_excel(writer,sheet_name=cityname,index=False,engine='openpyxl') 
            writer.save()
            writer.close()
            # os.makedirs(template_path, exist_ok=True)  
            # df.to_excel(os.path.join(template_path,'Template for Existing Property Detail.xlsx'),index=False)
            # #Open existing excel file
            # templateFile = os.path.join(template_path,'Template for Existing Property Detail.xlsx')
            # workbook1 = openpyxl.load_workbook(r'D:\eGov\Data\WS\Template\Template for Existing Property Detail.xlsx')         
            # writer = pd.ExcelWriter(templateFile, engine='openpyxl')   
            # writer.book = workbook1          
            # #Add dataframe to excel file 
            # df.to_excel(writer,sheet_name="Master_Locality/Mohalla",index=False,engine='openpyxl')                
            # writer.save()
            # writer.close()
            #return
            # shutil.copy(r'D:\eGov\Data\WS\Template\Template for Existing Property Detail.xlsx',os.path.join(template_path,'Template for Existing Property Detail.xlsx'))
            # filePath =os.path.join(template_path,'Template for Existing Property Detail.xlsx')
            # workbook = xlsxwriter.Workbook(filePath)
            # worksheet = workbook.add_worksheet()

            # worksheet.write(0, 0, 1234)     # Writes an int
            # worksheet.write(1, 0, 1234.56)  # Writes a float
            # worksheet.write(2, 0, 'Hello')  # Writes a string
            # worksheet.write(3, 0, None)     # Writes None
            # worksheet.write(4, 0, True)     # Writes a bool

            # workbook.close()

            # wb=openpyxl.load_workbook(os.path.join(template_path,'Template for Existing Property Detail.xlsx'), keep_vba = True)
            # source=wb.get_sheet_by_name('Locality')
            # # load demo.xlsx 
            # # get Sheet
            # # copy sheet
            # target=wb.copy_worksheet(source)
            # # save workbook
            # wb.save(os.path.join(template_path,'Template for Existing Property Detail.xlsx'))
        print("Done")    


if __name__ == "__main__":
    main()
