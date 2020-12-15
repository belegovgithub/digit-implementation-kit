import requests
import csv
from common import *
from config import config ,load_employee_creation_config
from common import superuser_login, get_employee_types, get_employee_status, add_role_to_user, get_employees_by_phone, \
    get_employees_by_id 
from config import config
import io
import os
import numpy
import pandas as pd
from datetime import datetime, timedelta

ROLE_CODES = {"RO": "RO", "GRO": "GRO", "PGR-CE": "CSR", "TL Counter Employee": "TL_CEMP",
              "TL Doc Verifier": "TL_DOC_VERIFIER", "TL Field Inspector": "TL_FIELD_INSPECTOR", "TL Approver": "TL_APPROVER", "mCollect Employee": "UC_EMP" ,"STADMIN" :"STADMIN" }

def getValue(df, row,colName,defValue="") :
    if not pd.isna(row[df.columns.get_loc(colName)] ) : 
        return str(row[df.columns.get_loc(colName)]).strip() 
    else : 
        return defValue if defValue is not None else row[df.columns.get_loc(colName)] 

def getCodeForName(dictArr, name) :
    obj = next((item for item in dictArr if item.get("name") and item["name"] == name), None)
    #print("getCodeForName",obj)
    return obj['code'] if obj is not None else None 
    
def getTime(df, row,colName,defValue=None) :
    try : 
        dObj = row[df.columns.get_loc(colName)]
        if not isinstance(dObj, datetime) and type(dObj) is str: 
            dateStr =row[df.columns.get_loc(colName)].strip() 
            if "/" in dateStr : 
                dObj=datetime.strptime(dateStr, '%d/%m/%Y') 
            elif "." in dateStr : 
                dObj=datetime.strptime(dateStr, '%d.%m.%Y') 
            else : 
                dObj=datetime.strptime(dateStr, '%d-%m-%Y') 
        milliseconds = int((dObj - datetime(1970, 1, 1)).total_seconds())*1000
        return milliseconds
    except Exception as ex:
        print("Error in time conversion ",row[df.columns.get_loc(colName)],ex)
    return None


def createSTADMIN():
    return {
        "Role Name*": "STADMIN",
        "Login Id UAT": "STADMIN_" + config.CITY_NAME.upper(),
        "Employee Mobile Number*": config.HRMS_STADMIN_PHONE_NUMBER,
        "Employee Date of Birth*": config.HRMS_STADMIN_DOB,
        "Appointed From Date*": config.HRMS_STADMIN_JOINING,
        "Employee Full Name*": "CB Admin",
        "Designation*": config.HRMS_DEF_DESIG,
        "Department*": config.HRMS_DEF_DEPT
    } 

def createDEV():
    return {
        "Role Name*": config.HRMS_DEV_ROLES,
        "Login Id UAT": "DEV_" + config.CITY_NAME.upper(),
        "Employee Mobile Number*": config.HRMS_DEV_PHONE_NUMBER,
        "Employee Date of Birth*": config.HRMS_STADMIN_DOB,
        "Appointed From Date*": config.HRMS_STADMIN_JOINING,
        "Employee Full Name*": "CB Admin",
        "Designation*": config.HRMS_DEF_DESIG,
        "Department*": config.HRMS_DEF_DEPT
    }



def main():
    ## load default config
    load_employee_creation_config()
    city = config.CITY_NAME
    tenant_id = config.TENANT + "." + city.lower()
    post_data_list=[]
    post_data_resp_list=[]
    filePath = config.HRMS_WORKBOOK  #os.path.join(config.BOUNDARIES_FOLDER, config.HRMS_EXCEL_NAME)
    print(filePath)
    if not os.path.isfile(filePath) :
        raise Exception("File Not Found ",filePath)

    #auth_token = superuser_login()["access_token"]
    auth_token = 'ef9d6e42-526c-4c29-8e70-6d27a9694aef'
    DEPT_LIST =(mdms_call(auth_token, "common-masters", 'Department')["MdmsRes"]["common-masters"]["Department"])
    DESIG_LIST =(mdms_call(auth_token, "common-masters", 'Designation')["MdmsRes"]["common-masters"]["Designation"])
    #print("DESIG_LIST--",DESIG_LIST)
    print("auth token ", auth_token)
    start_row = 0
    dfs = open_excel_file(filePath)
    df = get_sheet(dfs, config.HRMS_SHEET_NAME)
    
    #df = df.replace('nan','')
    #print(df.columns)
    #print(config.CITY_NAME.upper())
 
    if config.HRMS_CREATE_STADMIN  : 
        df =df.append(createSTADMIN(), ignore_index=True)
        #print("stadmin--",df)
    if config.HRMS_CREATE_DEV_USER : 
        df =df.append(createDEV(), ignore_index=True)


    #print(df) 
    for ind in df.index:
 
        row = df.iloc[ind] 
        print(row)
        headers = {'Content-Type': 'application/json'}
        details = []
        roles = []
        assignments=[]
        is_primary = True
        departments = getValue(df,row,"Department*" ,"" ) 
        role_codes = getValue(df,row,"Role Name*" ,"" ) 
        role_names = role_codes
        designation = getCodeForName(DESIG_LIST, getValue(df,row,"Designation*" ,"" ))
        #print("designation--",designation)  
        password = "Bel@1234"
        username = getValue(df,row,"Login Id UAT" ,"" )   
        mobile_number = getValue(df,row,"Employee Mobile Number*",None )    
        name = getValue(df,row,"Employee Full Name*" ,None  )     
        gender = getValue(df,row,"Gender*" ,"M" )    
        fName = getValue(df,row,"Father/ Husband Name*" ,"FATHER_NAME" )  
        empType =getValue(df,row,"Nature of Employment *" ,"PERMANENT" )    
        dob =getTime(df,row,"Employee Date of Birth*" )  
        emailId =getValue(df,row,"Employee Email Address*" ,"" )  
        joiningDate =getTime(df,row,"Appointed From Date*" )  
        print("joiningDate--",joiningDate)
        address =getValue(df,row,"Correspondance Address*" ,"" )  

 
        ## Check for empty rows 
        
        if pd.isna(name) or  pd.isna(mobile_number) : 
            continue
        print("========================",name,mobile_number,"==========================")
        print("UserNAME",username)
        existing_employees = get_employees_by_id(
            auth_token, username, tenant_id)
        print(existing_employees)

        existing_employees = get_employees_by_id(
            auth_token, username, tenant_id)
        print("existing_employees",existing_employees)
        roles_needed =  set(map(lambda role : ROLE_CODES[role.strip()], role_codes.split("|")))
        roles_needed.add("EMPLOYEE")
        #print("roles_needed",roles_needed)
        for role  in roles_needed:
            roles.append({"code": role, "name": config.ROLE_CODE_MAP[role], "tenantId": tenant_id})

        if existing_employees:
            # This employee already exists
            existing_mobilenumber = existing_employees[0]['mobileNumber']
            roles_currently = set(
                map(lambda role: role['code'], existing_employees[0]['roles']))
            ask_for_role_update = False
            if existing_mobilenumber != mobile_number:
                print(
                    "The employee {} already exist with mobile number {}. You have specified a different mobile number {}".format(
                        username, existing_mobilenumber, mobile_number))
                ask_for_role_update = True
            else:
                print("Employee", username, tenant_id, name, mobile_number, "already exists - ",
                      len(existing_employees))

            if roles_needed.issubset(roles_currently):
                print("The employee already has all required roles. Nothing needed")
            else:
                if ask_for_role_update:
                    username_update = input(
                        "Would you like to add " + role_codes + " to " + username + "[Use n for skip]? ")
                    if username_update.lower() == "n":
                        print(
                            "Skipping adding required roles to user - {}".format(username))
                        continue
                else:
                    print("Adding required roles to user - {}".format(username))
                add_role_to_user(auth_token, username, tenant_id,
                                 roles_needed - roles_currently)
            continue

        ### Get Employee By Phone Detail 
        existing_employees = get_employees_by_phone(
            auth_token, mobile_number, tenant_id)

        if existing_employees:
            info = map(lambda emp: "(username={}, mob={}, name={}, roles={}".format(
                emp["userName"],
                emp["mobileNumber"],
                emp["name"],
                "|".join(map(lambda role: role["code"], emp["roles"]))), existing_employees)
            print("{} Employee(s) with mobile number {} already exists".format(len(existing_employees),
                                                                               mobile_number), list(info))
            if len(existing_employees) > 1:
                username_update = input(
                    "Which user would you like to update with " + role_codes + " [Use n for skip]? ")
            else:
                username_update = input(
                    "Will you like to add the " + role_codes + " to user {} [Yn]? ".format(
                        existing_employees[0]["userName"]))
                if username_update.strip().lower() == "n":
                    print("Skipping the user creation for {}".format(username))
                    continue
                else:
                    username_update = existing_employees[0]["userName"]

            if username_update.strip().lower() == "n":
                print("Skipping the user creation for {}".format(username))
                continue
            else:
                employee_found = list(
                    filter(lambda emp: emp["userName"] == username_update, existing_employees))
                if not employee_found:
                    print("Cannot find employee with username - " + username_update)
                else:
                    roles_currently = set(
                        map(lambda role: role['code'], employee_found[0]['roles']))
                    add_role_to_user(auth_token, username_update,
                                     tenant_id, roles_needed - roles_currently)
            continue
        
        # IF Employee does not exist in system
        
        if designation is not None : 
            for department in departments.split("|"):
                code =getCodeForName(DEPT_LIST, department)
                if code is not None : 
                    assignments.append({
                        "fromDate": joiningDate,
                        "toDate": None,
                        "department": code,
                        "isCurrentAssignment": True,
                        "designation": designation ,
                        "reportingTo": "",
                        "isHod": True
                    })
        print("assignments--",assignments)

        post_data = {
            "RequestInfo": {
                "authToken": auth_token
            },
            "Employees": [
                {
                    "user": {
                        "name": name,
                        "userName": username,
                        "fatherOrHusbandName": fName,
                        "mobileNumber": mobile_number,
                        "emailId" :emailId,
                        "gender": "MALE" if gender == "M" else "FEMALE",
                        "dob": dob,
                        "roles": roles,
                        "tenantId": tenant_id,
                        "correspondenceAddress": address,
                        "type": "EMPLOYEE"
                    },
                    "code": username,
                    "dateOfAppointment": joiningDate,
                    "employeeType": "PERMANENT",
                    "employeeStatus": "EMPLOYED",
                    "jurisdictions": [
                        {
                            "hierarchy": "REVENUE",
                            "boundary": tenant_id,
                            "boundaryType": "City",
                            "tenantId": tenant_id
                        }
                    ],
                    "active": True,
                    "assignments":assignments,
                    "serviceHistory": [

                    ],
                    "education": [
                    ],
                    "tests": [
                    ],
                    "tenantId": tenant_id
                }
            ]
        }

        post_response = requests.post(url=config.HOST + '/egov-hrms/employees/_create', headers=headers,
                                      json=post_data)
        print("==================================================")
        print(post_data)
        post_data_list.append(post_data)
        print("--------")
        print(post_response.json())
        post_data_resp_list.append(post_response.json())
        
        if post_response.status_code == 202 : 
            print ("User Created : ",username)
            update_user_password(auth_token, tenant_id, username, "Bel@1234")
        print("==================================================")
        print("\n\n")

    # Save the request /response of newly created user in same  folder for reference
    with io.open(os.path.join(config.BOUNDARIES_FOLDER,"hrms-request.json"), mode="w", encoding="utf-8") as f:
        json.dump(post_data_list, f, indent=2,  ensure_ascii=False, cls=DateTimeEncoder)
    with io.open(os.path.join(config.BOUNDARIES_FOLDER,"hrms-response.json"), mode="w", encoding="utf-8") as f:
        json.dump(post_data_resp_list, f, indent=2,  ensure_ascii=False, cls=DateTimeEncoder)

if __name__ == "__main__":
    main()
