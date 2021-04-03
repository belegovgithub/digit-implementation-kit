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


    # for root, dirs, files in os.walk(r"D:\eGov\Data\WS\Template\Property1", topdown=True):
    #     for name in dirs:
    #         for root, dirs, files in os.walk(r"D:\eGov\Data\WS\Template\src", topdown=True):
    #             for f in files:
    #                 shutil.copy(os.path.join(r"D:\eGov\Data\WS\Template\src",f), os.path.join("D:\eGov\Data\WS\Template\Property1",name)) 
            
    logFile = open(r"D:\temp\Logfile.txt", "w")
    logFile.write("Woops! I have added the content!\n")
    logFile.write("Woops! I have deleted the content!")
    logFile.close()

    
if __name__ == "__main__":
    main()