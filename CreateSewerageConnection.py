from common import *
from config import config
import io
import os 
import sys
from common import superuser_login
from SewerageConnection import *
from PropertyTax import *
import pandas as pd
import openpyxl

def main():
    Flag =False
    
def ProcessSewerageConnection(propertyFile, sewerageFile, logfile, root, name,  cityname) :
    wb_property = openpyxl.load_workbook(propertyFile) 
    propertySheet = wb_property.get_sheet_by_name('Property Assembly Detail') 
    wb_sewerage = openpyxl.load_workbook(sewerageFile) 
    sewerageSheet = wb_sewerage.get_sheet_by_name('Sewerage Connection Details')  
    print('no. of rows in sewerage file: ', sewerageSheet.max_row) 
    validate = validateSewerageData(propertySheet, sewerageFile, logfile, cityname)  
    if(validate == False):                
        print('Data validation for sewerage Failed, Please check the log file.') 
        # return
    else:
        print('Data validation for sewerage success.')
    # createSewerageJson(propertySheet, sewerageSheet, cityname, logfile, root, name)   
    # wb_sewerage.save(sewerageFile)        
    # wb_sewerage.close()

def validateSewerageData(propertySheet, sewerageFile, logfile, cityname):
    validated = True
    wb_sewerage = openpyxl.load_workbook(sewerageFile) 
    sewerage_sheet = wb_sewerage.get_sheet_by_name('Sewerage Connection Details') 
    index = 2
    reason = 'sewerage file validation starts.\n'
    print(reason)
    logfile.write(reason)
    abas_ids = [] 
    try:
        for index in range(3, propertySheet.max_row):
            if pd.isna(propertySheet['A{0}'.format(index)].value):
                validated = False
                reason = 'Sewerage File data validation failed, Sl no. column is empty'
                logfile.write(reason)
                break
            abas_ids.append(propertySheet['B{0}'.format(index)].value.strip())   
    except Exception as ex:
        print("validateSewerageData Exception: ", ex)
    for row in sewerage_sheet.iter_rows(min_row=3, max_col=22, max_row=sewerage_sheet.max_row,values_only=True):        
        index = index + 1
        try:
            if pd.isna(row[1]):
                break
            if pd.isna(row[0]):
                validated = False
                reason = 'Sewerage File data validation failed, Sl no. column is empty\n'
                logfile.write(reason)
            if pd.isna(row[1]):
                validated = False
                reason = 'Sewerage File data validation failed for sl no. '+ str(row[0]) + ', abas id is empty.\n'
                logfile.write(reason) 
            if pd.isna(row[2]):
                validated = False
                reason = 'Sewerage File data validation failed for sl no. '+ str(row[0]) + ', old connection number is empty.\n'
                logfile.write(reason)
            if pd.isna(row[3]):
                validated = False
                reason = 'Sewerage File data validation failed for sl no. '+ str(row[0]) + ', same as property address cell is empty.\n'
                logfile.write(reason)
            if(str(row[3]).strip() == 'No'):
                if pd.isna(row[4]) or pd.isna(row[5]):
                    validated = False
                    reason = 'Sewerage File data validation failed for sl no. '+ str(row[0]) + ', mobile number or name is empty.\n'
                    logfile.write(reason) 
                if not pd.isna(row[5]):
                    if not bool(re.match("[a-zA-Z \\.]+$",str(row[5]))):
                        validated = False
                        reason = 'Sewerage File data validation failed, Name has invalid characters for sl no. '+ str(row[0]) +'\n'
                        logfile.write(reason)  
            
            if not pd.isna(row[1]):
                if str(row[1]).strip() not in abas_ids:
                    validated = False
                    reason = 'there is no abas id available in property data for sewerage connection sl no. '+ str(row[0]) +'\n'
                    logfile.write(reason) 
        except Exception as ex:
            print("validateSewerageData Exception: ", row[0], '   ', ex)
    reason = 'sewerage file validation ends.\n'
    print(reason)
    logfile.write(reason) 
    return validated


def createSewerageJson(propertySheet, sewerageSheet, cityname, logfile, root, name):
    createdCount = 0
    searchedCount = 0
    notCreatedCount = 0
    owner_obj = {}
    for i in range(3, propertySheet.max_row):    
        try:    
            abas_id = propertySheet['B{0}'.format(i)].value.strip()
            for row in propertySheet.iter_rows(min_row=i, max_col=42, max_row=i,values_only=True):                    
                owner = Owner()
                address = Address()
                address.buildingName = getValue(row[17].strip(),str,"")
                address.doorNo = getValue(str(row[18]).strip(),str,"")
                correspondence_address = get_propertyaddress(address.doorNo,address.buildingName,getValue(str(row[13]).strip(),str,"Others"),cityname)
                owner.name = getValue(str(row[28]).strip(),str,"NAME")
                owner.mobileNumber = getValue(str(row[29]).strip(),str,"3000000000")
                owner.emailId = getValue(str(row[30]).strip(),str,"")
                owner.gender = process_gender(str(row[31]).strip())
                owner.fatherOrHusbandName = getValue(str(row[33]).strip(),str,"Guardian")
                owner.relationship =  process_relationship(str(row[34]).strip())
                owner.sameAsPeropertyAddress = getValue(str(row[35]).strip(),str,"Yes")
                if(owner.sameAsPeropertyAddress ==  'Yes'):
                    owner.correspondenceAddress = correspondence_address
                else: 
                    owner.correspondenceAddress = getValue(str(row[36]).strip(),str,"Correspondence")
                owner.ownerType =  process_special_category(str(row[37]).strip())
                if abas_id not in owner_obj:
                    owner_obj[abas_id] = []
                owner_obj[abas_id].append(owner)
        except Exception as ex:
            print("createSewerageJson Exception: ", row[0], '   ', ex)
    index = 2
    for row in sewerageSheet.iter_rows(min_row=3, max_col=19, max_row=sewerageSheet.max_row, values_only=True):
        try:  
            index = index + 1
            abasPropertyId =  getValue(str(row[1]).strip(),str,None)  
            property = Property() 
            auth_token = superuser_login()["access_token"]
            tenantId = 'pb.'+ cityname
            property.tenantId = tenantId
            if pd.isna(abasPropertyId):
                print("empty Abas id in sewerage file")
                return
            
            status, res = property.search_abas_property(auth_token, tenantId, abasPropertyId)        
            with io.open(os.path.join(root, name,"property_search_res.json"), mode="w", encoding="utf-8") as f:
                json.dump(res, f, indent=2,  ensure_ascii=False) 
            propertyId = ''
            if(len(res['Properties']) >= 1):
                for found_index, resProperty in enumerate(res["Properties"]):
                    propertyId = resProperty["propertyId"]
                    break
                sewerageConnection = SewerageConnection()
                connectionHolder = ConnectionHolder()
                processInstance = ProcessInstance()
                additionalDetail = AdditionalDetail()
                sewerageConnection.connectionHolders = []
                if(str(row[3]).strip() == 'Yes'):
                    sewerageConnection.connectionHolders = None
                else:
                    connectionHolder.name = getValue(str(row[5]).strip(),str,"NAME")
                    connectionHolder.mobileNumber = getValue(str(row[4]).strip(),str,"3000000000")
                    connectionHolder.fatherOrHusbandName = getValue(str(row[9]).strip(),str,"Guardian")
                    connectionHolder.emailId = getValue(str(row[6]).strip(),str,"")
                    connectionHolder.correspondenceAddress = getValue(str(row[12]).strip(),str,"Correspondence")
                    connectionHolder.relationship = process_relationship(str(row[10]).strip())
                    connectionHolder.ownerType = process_special_category(str(row[13]).strip())
                    connectionHolder.gender = process_gender(str(row[7]).strip())
                    connectionHolder.sameAsPropertyAddress = False
                    sewerageConnection.connectionHolders.append(connectionHolder)
                
                sewerageConnection.oldConnectionNo = getValue(str(row[2]).strip(),str,None)
                sewerageConnection.drainageSize = getValue(str(row[14]).strip(),float,0.25)
                sewerageConnection.proposedDrainageSize = getValue(str(row[14]).strip(),float,0.25)
                if(sewerageConnection.waterSource != 'OTHERS'):
                    sewerageConnection.waterSubSource = sewerageConnection.waterSource.split('.')[1]                
                else:
                    sewerageConnection.waterSubSource = ''
                    sewerageConnection.sourceInfo = 'Other'
                sewerageConnection.propertyOwnership  = process_propertyOwnership(str(row[11]).strip())
                sewerageConnection.noOfWaterClosets = getValue(str(row[15]).strip(),int,1)
                sewerageConnection.proposedWaterClosets = getValue(str(row[15]).strip(),int,1)
                sewerageConnection.noOfToilets = getValue(str(row[16]).strip(),int,1)
                sewerageConnection.proposedToilets = getValue(str(row[16]).strip(),int,1)
                
                additionalDetail.locality = ''
                sewerageConnection.additionalDetails = additionalDetail
                processInstance.action = 'ACTIVATE_CONNECTION'
                sewerageConnection.tenantId = tenantId
                sewerageConnection.propertyId = propertyId
                sewerageConnection.processInstance = processInstance
                sewerageConnection.water = False
                sewerageConnection.sewerage = True
                sewerageConnection.service = 'Sewerage'
                sewerageConnection.applicationType = 'NEW_SEWERAGE_CONNECTION'
                sewerageConnection.applicationStatus = 'CONNECTION_ACTIVATED'
                sewerageConnection.source = 'MUNICIPAL_RECORDS'
                sewerageConnection.channel = 'DATA_ENTRY'
                sewerageConnection.status = 'ACTIVE'
        except Exception as ex:
            print("createSewerageJson Exception: ", row[0], '   ', ex)

            auth_token = superuser_login()["access_token"]
            status, res = sewerageConnection.search_sewerage_connection(auth_token, tenantId, sewerageConnection.oldConnectionNo)               
            with io.open(os.path.join(root, name,"sewerage_search_res.json"), mode="w", encoding="utf-8") as f:
                json.dump(res, f, indent=2,  ensure_ascii=False)  
            if(len(res['SewerageConnections']) == 0):
                statusCode, res = sewerageConnection.upload_sewerage(auth_token, tenantId, sewerageConnection.oldConnectionNo, root, name)
                with io.open(os.path.join(root, name,"sewerage_create_res.json"), mode="w", encoding="utf-8") as f:
                    json.dump(res, f, indent=2,  ensure_ascii=False)  
                sewerageconnectionNo = '' 
                if(statusCode == 200 or statusCode == 201):
                    for found_index, resProperty in enumerate(res["SewerageConnections"]):
                        connectionNo = resProperty["connectionNo"]
                        value = 'B{0}'.format(index) + '    ' + str(connectionNo) + '\n'
                        logfile.write(value)
                        sheet1['T{0}'.format(index)].value = connectionNo
                        reason = 'sewerage connection created for abas id ' + str(property.abasPropertyId)
                        logfile.write(reason)
                        print(reason)
                        createdCount = createdCount + 1
                else:
                    reason = 'sewerage not created status code '+ str(statusCode)+ ' for abas id ' + str(property.abasPropertyId) + ' response: '+ str(res) + '\n'
                    logfile.write(reason)
                    print(reason)
                    notCreatedCount = notCreatedCount + 1
            else:
                reason = 'sewerage connection exist for abas id ' + str(property.abasPropertyId)
                logfile.write(reason)
                print(reason)
                searchedCount = searchedCount + 1
                        
        else:
            reason = 'property does not exist for abas id '+ str(property.abasPropertyId) + '\n'
            logfile.write(reason)
            

    reason = 'sewerage created count: '+ str(createdCount)
    print(reason)
    reason = 'sewerage not created count: '+ str(notCreatedCount)
    print(reason)
    reason = 'sewerage searched count: '+ str(searchedCount)
    print(reason)


def getTime(dateObj,defValue=None) :
    try : 
        if not isinstance(dateObj, datetime) and type(dateObj) is str: 
            dateStr =dateObj.strip() 
            if "/" in dateStr : 
                dateObj=datetime.strptime(dateStr, '%d/%m/%Y') 
            elif "." in dateStr : 
                dateObj=datetime.strptime(dateStr, '%d.%m.%Y') 
            else : 
                dateObj=datetime.strptime(dateStr, '%d-%m-%Y') 
        milliseconds = int((dateObj - datetime(1970, 1, 1)).total_seconds())*1000
        return milliseconds
    except Exception as ex:
        print("Error in time conversion ",dateObj,ex)
    return None

def get_propertyaddress(doorNo, buildingName,locality,cityname):
    return doorNo + ' ' + buildingName + ' ' +locality + ' ' + cityname


def process_relationship(value):
    relationship_MAP = {
        "Parent": "PARENT",
        "Spouse": "SPOUSE",
        "Gurdian": "GUARDIAN",
        "None": "PARENT"
    }
    return relationship_MAP[value]

def process_gender(value):
    gender_MAP = {
        "Male": "MALE",
        "Female": "FEMALE",
        "Transgender": "TRANSGENDER",
        "None": "MALE"       
    }
    return gender_MAP[value]

def process_connection_type(value):
    connection_MAP = {
        "Metered": "Metered",
        "Non-Metered": "Non Metered",
        "None": "Non Metered"     
    }
    return connection_MAP[value]

def process_propertyOwnership(value):
    propertyOwnership_MAP = {
        "None": "HOR",
        "HOR": "HOR",
        "Tenant": "TENANT"
    }
    return propertyOwnership_MAP[value]

def process_connection_permission(value):
    connection_permission_MAP = {
        "Authorized": "AUTHORIZED",
        "Unauthorized": "UNAUTHORIZED",
        "None": "AUTHORIZED"
    }
    return connection_permission_MAP[value]

def process_special_category(value):
    special_category_MAP = {
        "Freedom fighter": "FREEDOMFIGHTER",
        "Widow": "WIDOW",
        "Handicapped": "HANDICAPPED",
        "Below Poverty Line": "BPL",
        "Defense Personnel": "DEFENSE",
        "Employee/Staff of CB": "STAFF",
        "None of the above": "NONE",
        "None":"NONE"
    }
    return special_category_MAP[value]

def getValue(value,dataType,defValue="") :
    if(value == None or value == 'None'): 
        return defValue    
    else : 
        return dataType(value)

if __name__ == "__main__":
    main()    
    type         


