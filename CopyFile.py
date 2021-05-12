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
from openpyxl import Workbook, utils
from openpyxl.worksheet.table import Table, TableStyleInfo
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.styles import PatternFill, Border, Side, Alignment, Protection, Font
from openpyxl.comments import Comment
from datetime import datetime, timedelta
from math import isnan
import shutil
def main():
    
    srcFolderPath =r"C:\Users\Admin\Downloads\Legacy_Data"
    destFolderPath =r"D:\eGov\Data\WS\Temp"
    with io.open(config.TENANT_JSON, encoding="utf-8") as f:
        cb_module_data = json.load(f)
        for found_index, module in enumerate(cb_module_data["tenants"]):
            if module["city"]["ulbGrade"]=="ST":
                continue
            cityname =module["code"].lower()[3:]
            config.errormsg=[]
            name = 'CB ' + cityname.lower()
            if(cityname != 'testing'):
                folder_name = os.path.join(destFolderPath,name)
                os.makedirs(folder_name, exist_ok=True)   
    
    waterFile = "Template for Existing Water Connection Detail.xlsx"
    sewerageFile = "Template for Existing Sewerage Connection Detail.xlsx"
    for root, dirs, files in os.walk(destFolderPath, topdown=True):
        for name in dirs:
            subFolder = os.path.join(root, name)
            cityname = subFolder.replace(r"D:\eGov\Data\WS\Temp\CB ","" ).strip().lower()
            city = "CB " + cityname
            # print(cityname)
            propertyFile ='Template for Existing Property-Integrated with ABAS-' + cityname + '.xlsx'
            for root1, dirs1, files1 in os.walk(srcFolderPath, topdown=True):
                for f in files1:
                    if os.path.exists(os.path.join(srcFolderPath,city,propertyFile)):
                        shutil.copy(os.path.join(srcFolderPath,city,propertyFile), os.path.join(destFolderPath,name)) 
                    # if os.path.exists(os.path.join(srcFolderPath,city,waterFile)):
                    #     shutil.copy(os.path.join(srcFolderPath,city,waterFile), os.path.join(destFolderPath,name)) 
                    if os.path.exists(os.path.join(srcFolderPath,city,sewerageFile)):
                        shutil.copy(os.path.join(srcFolderPath,city,sewerageFile), os.path.join(destFolderPath,name)) 

    srcFolderPath =r"C:\Users\Admin\Downloads\WaterSewerageTemplates"
    for root, dirs, files in os.walk(destFolderPath, topdown=True):
        for name in dirs:
            subFolder = os.path.join(root, name)
            cityname = subFolder.replace(r"D:\eGov\Data\WS\Temp\CB ","" ).strip().lower()
            city = "CB " + cityname
            # print(cityname)
            propertyFile ='Template for Existing Property-Integrated with ABAS-' + cityname + '.xlsx'
            for root1, dirs1, files1 in os.walk(srcFolderPath, topdown=True):
                for f in files1:
                    if os.path.exists(os.path.join(srcFolderPath,city,propertyFile)) and not os.path.exists(os.path.join(destFolderPath,city,propertyFile)):
                        shutil.copy(os.path.join(srcFolderPath,city,propertyFile), os.path.join(destFolderPath,name)) 
                    if os.path.exists(os.path.join(srcFolderPath,city,waterFile)) and not os.path.exists(os.path.join(destFolderPath,city,waterFile)):
                        shutil.copy(os.path.join(srcFolderPath,city,waterFile), os.path.join(destFolderPath,name)) 
                    if os.path.exists(os.path.join(srcFolderPath,city,sewerageFile)) and not os.path.exists(os.path.join(destFolderPath,city,sewerageFile)):
                        shutil.copy(os.path.join(srcFolderPath,city,sewerageFile), os.path.join(destFolderPath,name))


    
if __name__ == "__main__":
    main()