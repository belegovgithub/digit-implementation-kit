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
from openpyxl.worksheet.datavalidation import DataValidation
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

    templateFile = r"D:\eGov\Data\WS\Template\Template for Existing Property Detail.xlsx"
    df1 = pd.read_excel(templateFile, 'Property Ownership Details')
    df2 = pd.read_excel(templateFile, 'Master Data')
    df3 = pd.read_excel(templateFile, 'Master_UsageType')

    with io.open(config.TENANT_JSON, encoding="utf-8") as f:
        cb_module_data = json.load(f)
        for found_index, module in enumerate(cb_module_data["tenants"]):
            if module["city"]["ulbGrade"]=="ST":
                continue
            tenantMapping[module["code"].lower()]=module["code"].lower()[3:]

        for root, dirs, files in os.walk(r"D:\eGov\Data\WS\ABASPY\CC", topdown=True):
            for name in dirs:
                #print (os.path.join(root, name))
                subfolder = os.path.join(root, name)
                cbFile =os.path.join(root, name,"BEL_Template for Existing Property Detail.xlsx")
                if os.path.exists(cbFile) :  
                    city = "pb."+ subfolder.replace(r"D:\eGov\Data\WS\ABASPY\CC\CB ","" ).strip().lower()

                    if city not in tenantMapping:
                        print("Not In city",city)
                        continue
                    cityname = tenantMapping[city]
                    print(cityname)
                    template_path = os.path.join(r"D:/eGov/Data/WS/Template/CC/CB "+cityname) 
                    # template_file = os.path.join(config.LOG_PATH ,  "Locality.xlsx" )
                    dfLocality = getLocalityData(cityname)
                    # cbFile = os.path.join(r"D:\eGov\Data\WS\ABASPY\CC\CB Agra",'BEL_Template for Existing Property Detail_CBAgra.xlsx')
                    workbook1 = openpyxl.load_workbook(cbFile)   
                    writer = pd.ExcelWriter(cbFile, engine='openpyxl')   
                    writer.book = workbook1   
                    df1.to_excel(writer,sheet_name="Property Ownership Details",index=False) 
                    df2.to_excel(writer,sheet_name="Master Data",index=False) 
                    df3.to_excel(writer,sheet_name="Master_UsageType",index=False) 
                    dfLocality.to_excel(writer,sheet_name="Locality",index=False)            
                    os.makedirs(template_path, exist_ok=True)
                    sheet = workbook1.get_sheet_by_name('Property Assembly Detail')
                    sheet.delete_cols(8)
                    sheet.delete_cols(15)
                    sheet.insert_cols(3)                
                    workbook1.save(os.path.join(template_path,'Template for Existing Property-Integrated with ABAS.xlsx'))
                    workbook1.close()
                    print("Done")

                    Flag=False
                else:
                    print("file doesnot exist")
            if Flag : 
                break
                
                
            



            # templateFile = r"D:\eGov\Data\WS\Template\Template for Existing Property Detail.xlsx"
            # df1 = pd.read_excel(templateFile, 'Property Ownership Details')
            # df2 = pd.read_excel(templateFile, 'Master Data')
            # df3 = pd.read_excel(templateFile, 'Master_UsageType')
            # df = pd.read_excel(templateFile, 'Property Ownership Details')
            # workbook1 = openpyxl.load_workbook(templateFile,  read_only=True)   
            # writer = pd.ExcelWriter(templateFile, engine='openpyxl')   
            # writer.book = workbook1    
            # sheet = workbook1.get_sheet_by_name('Property Assembly Detail')


            # cbFile = os.path.join(r"D:\eGov\Data\WS\ABASPY\CC\CB Agra",'BEL_Template for Existing Property Detail_CBAgra.xlsx')
            # if os.path.exists(cbFile) : 
            #     workbook1 = openpyxl.load_workbook(cbFile)   
            #     writer = pd.ExcelWriter(cbFile, engine='openpyxl')   
            #     writer.book = workbook1   
            #     df1.to_excel(writer,sheet_name="Property Ownership Details",index=False) 
            #     df2.to_excel(writer,sheet_name="Master Data",index=False) 
            #     # df2 = df2.loc[:, ~df2.columns.str.contains('Unnamed')]
            #     # df2.drop(df2.columns[df2.columns.str.contains('Unnamed',case = False)],axis = 1, inplace = True)
            #     # print(df2)
            #     df3.to_excel(writer,sheet_name="Master_UsageType",index=False) 
            #     dfLocality.to_excel(writer,sheet_name="Locality",index=False)            
            #     os.makedirs(template_path, exist_ok=True)
            #     # workbook1.save(os.path.join(template_path,'Template for Existing Property Detail.xlsx'))
            #     # workbook1.close()
            #     # workbook1 = openpyxl.load_workbook(os.path.join(template_path,'Template for Existing Property Detail.xlsx'))   
            #     # writer = pd.ExcelWriter(cbFile, engine='openpyxl')   
            #     # writer.book = workbook1
            #     # dfProperty = pd.read_excel(os.path.join(template_path,'Template for Existing Property Detail.xlsx'),'Property Assembly Detail')
            #     # dfProperty.insert(3, "Property Type *", "")
            #     sheet = workbook1.get_sheet_by_name('Property Assembly Detail')
            #     sheet.delete_cols(8)
            #     sheet.delete_cols(15)
            #     sheet.insert_cols(3)                

            #     # dv = DataValidation(type="list", formula1='"Yes,No"', allow_blank=False, showDropDown = True)
            #     # sheet.datavalidation.DataValidationList('="Master Data"!$A$2:$A$4')
            #     # sheet.add_data_validation(dv)
            #     # dv.ranges.append('C2')
            #     # sheet.data_validation('C1:C5',{'validate': 'list', 'source': '="Master Data"!$A$2:$A$4'  })
            #     workbook1.save(os.path.join(template_path,'Template for Existing Property-Integrated with ABAS.xlsx'))
            #     workbook1.close()

            # # df.to_excel(template_file,sheet_name=cityname,index=False)
            # # workbook1 = openpyxl.load_workbook(template_file,  read_only=True)
            # # writer = pd.ExcelWriter(template_file, engine='openpyxl')   
            # # writer.book = workbook1        
            # # df.to_excel(writer,sheet_name=cityname,index=False,engine='openpyxl') 
            # # writer.save()
            # # writer.close()

            # os.makedirs(template_path, exist_ok=True)  
            # # df.to_excel(os.path.join(template_path,'Template for Existing Property Detail.xlsx'),index=False)
            # #Open existing excel file
            # templateFile = os.path.join(r"D:\eGov\Data\WS\Template",'Template for Existing Property Detail.xlsx')
            # workbook1 = openpyxl.load_workbook(templateFile)         
            # writer = pd.ExcelWriter(templateFile, engine='openpyxl')   
            # writer.book = workbook1    
            # sheet = workbook1.get_sheet_by_name('Property Assembly Detail')
            # sheet.insert_cols(0,"Add")
            # # add_column(workbook1,'Property Assembly Detail', ['new header', 'value1', 'value2'])      
            # #Add dataframe to excel file 
            # # df.to_excel(writer,sheet_name="Master_Locality/Mohalla",index=False,engine='openpyxl')                
            # workbook1.save(os.path.join(template_path,'Template for Existing Property Detail.xlsx'))
            # workbook1.close()
            # return
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
        # print("Done")    

def getLocalityData(cityname):
    data = []
    cityname = "agra"
    boundary_path = os.path.join(config.MDMS_LOCATION ,  cityname , "egov-location")
    
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
    dfLocality = pd.DataFrame(data,columns=['Locality Name','Code'])
    return dfLocality

def add_column(workbook,sheet_name, column):
    ws = workbook[sheet_name]
    new_column = ws.max_column + 1

    for rowy, value in enumerate(column, start=1):
        ws.cell(row=rowy, column=new_column, value=value)

if __name__ == "__main__":
    main()

