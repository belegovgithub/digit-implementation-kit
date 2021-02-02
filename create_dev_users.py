import requests
import csv
from common import *
from config import config, load_employee_creation_config
from common import superuser_login, get_employee_types, get_employee_status, add_role_to_user, get_employees_by_phone, \
    get_employees_by_id
from config import config
import io
import os
import numpy
import pandas as pd
from datetime import datetime, timedelta,date
from json import JSONEncoder

 

post_data_list=[]
post_data_resp_list=[]

def getValue(df, row, colName, defValue=""):
    if not pd.isna(row[df.columns.get_loc(colName)]):
        return str(row[df.columns.get_loc(colName)]).strip()
    else:
        return defValue if defValue is not None else row[df.columns.get_loc(colName)]


def getCodeForName(dictArr, name):
    obj = next((item for item in dictArr if item.get(
        "name") and item["name"] == name), None)
    # print("getCodeForName",obj)
    return obj['code'] if obj is not None else None


def getTime(df, row, colName, defValue=None):
    try:
        dObj = row[df.columns.get_loc(colName)]
        if not isinstance(dObj, datetime) and type(dObj) is str:
            dateStr = row[df.columns.get_loc(colName)].strip()
            if "/" in dateStr:
                dObj = datetime.strptime(dateStr, '%d/%m/%Y')
            elif "." in dateStr:
                dObj = datetime.strptime(dateStr, '%d.%m.%Y')
            else:
                dObj = datetime.strptime(dateStr, '%d-%m-%Y')
        milliseconds = int((dObj - datetime(1970, 1, 1)).total_seconds())*1000
        return milliseconds
    except Exception as ex:
        print("Error in time conversion ",
              row[df.columns.get_loc(colName)], ex)
    return None


def createSTADMIN():
    return {
        "Role Name*": "STADMIN",
        "Employee ID*": "STADMIN_" + config.CITY_NAME.upper(),
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
        "Employee ID*": "DEV_" + config.CITY_NAME.upper(),
        "Employee Mobile Number*": config.HRMS_DEV_PHONE_NUMBER,
        "Employee Date of Birth*": config.HRMS_STADMIN_DOB,
        "Appointed From Date*": config.HRMS_STADMIN_JOINING,
        "Employee Full Name*": "CB Admin",
        "Designation*": config.HRMS_DEF_DESIG,
        "Department*": config.HRMS_DEF_DEPT
    }


def createCall(auth_token, name, mobile_number, roles, tenant_id):
    username = name + "_"+tenant_id.split('.')[1][0:4].upper()
    post_data = {
        "RequestInfo": {
            "authToken": auth_token
        },
        "Employees": [
            {
                "user": {
                    "name": name,
                    "userName": username,
                    "fatherOrHusbandName": "FATHER_NAME",
                    "mobileNumber": mobile_number,
                    "emailId": "vipinpublicdomain@gmail.com",
                    "gender": "MALE",
                    "dob": datetime.strptime("01/01/1986", '%d/%m/%Y'),
                    "roles": roles,
                    "tenantId": tenant_id,
                    "correspondenceAddress": "ABC",
                    "type": "EMPLOYEE"
                },
                "code": username,
                "dateOfAppointment": datetime.strptime("01/01/2005", '%d/%m/%Y'),
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
                "assignments":  [
                    {
                        "fromDate": 571017600000,
                        "toDate": None,
                        "department": "DEPT_39",
                        "isCurrentAssignment": True,
                        "designation": "DESIG_48",
                        "reportingTo": "",
                        "isHod": True
                    }
                ],
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
    return post_data
    # post_response = requests.post(url=config.HOST + '/egov-hrms/employees/_create', headers={'Content-Type': 'application/json'},
    #                                   json=post_data)


def createEmployee(auth_token, name,username, tenant_id, mobile_number,role_codes, DEPT_LIST, DESIG_LIST):
    headers = {'Content-Type': 'application/json'}
    details = []
    roles = []
    assignments = []
    is_primary = True
    departments = "Information Technology"
    
    designation = getCodeForName(DESIG_LIST, "Programmer")  
    role_names = role_codes
    password = "Bel@1234"
    
    gender = "M"
    fName = "FATHER_NAME"
    empType = "PERMANENT"
    dob =504921600000
    emailId = "vipinpublicdomain@gmail.com"
    joiningDate = 1104537600000
    address = ""

    ## To Keep the same hierachy as in create_employee_script_hrms
    for x in range(1):
 
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
        #post_data=json.dumps(post_data, cls=DateTimeEncoder)
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

 
ROLE_CODES = {"RO": "RO", "GRO": "GRO", "PGR-CE": "CSR", "TL Counter Employee": "TL_CEMP",
              "TL Doc Verifier": "TL_DOC_VERIFIER", "TL Field Inspector": "TL_FIELD_INSPECTOR", "TL Approver": "TL_APPROVER", "mCollect Employee": "UC_EMP", "STADMIN": "STADMIN",
              "SW_CEMP":"SW_CEMP","SW_DOC_VERIFIER":"SW_DOC_VERIFIER","SW_FIELD_INSPECTOR":"SW_FIELD_INSPECTOR","SW_APPROVER":"SW_APPROVER","SW_CLERK":"SW_CLERK",
               "WS_CEMP":"WS_CEMP","WS_DOC_VERIFIER":"WS_DOC_VERIFIER","WS_FIELD_INSPECTOR":"WS_FIELD_INSPECTOR","WS_APPROVER":"WS_APPROVER","WS_CLERK":"WS_CLERK", 
              
              }

def main():
    # load default config
    print("TENANT_JSON", config.TENANT_JSON)
    auth_token = superuser_login()["access_token"]
    DEPT_LIST =(mdms_call(auth_token, "common-masters", 'Department')["MdmsRes"]["common-masters"]["Department"])
    DESIG_LIST =(mdms_call(auth_token, "common-masters", 'Designation')["MdmsRes"]["common-masters"]["Designation"])
 

    with io.open(config.TENANT_JSON, encoding="utf-8") as f:
        tenants_data = json.load(f)
    for found_index, tenant in enumerate(tenants_data["tenants"]):
        print("=========================")
        if(len(tenant['code'].split('.')) > 1):
            tenant_id = tenant['code']
            if tenant_id != 'pb.testing':
                continue
            cityCode ="5_"+tenant_id.split('.')[1][0:4].upper()
            #State Admin
            # username = "STADMIN" + cityCode
            # roles ="STADMIN"
            # createEmployee(auth_token, "CB Admin",username , tenant_id, "8197292570",roles, DEPT_LIST, DESIG_LIST)
            # Challan Counter Employee
            username = "WS_CLERK" + cityCode
            roles ="WS_CLERK"
            createEmployee(auth_token, "BEL Water Employee",username , tenant_id, "6666600601",roles, DEPT_LIST, DESIG_LIST)
            username = "WS_APPROVER" + cityCode
            roles ="WS_APPROVER"
            createEmployee(auth_token, "BEL Water Employee",username , tenant_id, "6666600602",roles, DEPT_LIST, DESIG_LIST)
            username = "WS_FIELD_INSPECTOR" + cityCode
            roles ="WS_FIELD_INSPECTOR"
            createEmployee(auth_token, "BEL Water Employee",username , tenant_id, "6666600603",roles, DEPT_LIST, DESIG_LIST)
            
            username = "WS_DOC_VERIFIER" + cityCode
            roles ="WS_DOC_VERIFIER"
            createEmployee(auth_token, "BEL Water Employee",username , tenant_id, "6666600604",roles, DEPT_LIST, DESIG_LIST)
            
            username = "WS_CEMP" + cityCode
            roles ="WS_CEMP"
            createEmployee(auth_token, "BEL Water Employee",username , tenant_id, "6666600605",roles, DEPT_LIST, DESIG_LIST)
  
            
            username = "SW_CLERK" + cityCode
            roles ="SW_CLERK"
            createEmployee(auth_token, "BEL Water Employee",username , tenant_id, "6666600611",roles, DEPT_LIST, DESIG_LIST)
            username = "SW_APPROVER" + cityCode
            roles ="SW_APPROVER"
            createEmployee(auth_token, "BEL Water Employee",username , tenant_id, "6666600612",roles, DEPT_LIST, DESIG_LIST)
            username = "SW_FIELD_INSPECTOR" + cityCode
            roles ="SW_FIELD_INSPECTOR"
            createEmployee(auth_token, "BEL Water Employee",username , tenant_id, "6666600613",roles, DEPT_LIST, DESIG_LIST)
            
            username = "SW_DOC_VERIFIER" + cityCode
            roles ="SW_DOC_VERIFIER"
            createEmployee(auth_token, "BEL Water Employee",username , tenant_id, "6666600614",roles, DEPT_LIST, DESIG_LIST)
            
            username = "SW_CEMP" + cityCode
            roles ="SW_CEMP"
            createEmployee(auth_token, "BEL Water Employee",username , tenant_id, "6666600615",roles, DEPT_LIST, DESIG_LIST)
 
 
            
            # # PGR Counter Employee
            # username = "PGR_CE" + cityCode
            # roles ="PGR-CE"
            # createEmployee(auth_token, "PGR Counter Employee",username , tenant_id, "8197292572",roles, DEPT_LIST, DESIG_LIST)
            # # PGR RO Employee
            # username = "PGR_RO" + cityCode
            # roles ="RO"
            # createEmployee(auth_token, "PGR RO",username , tenant_id, "8197292573",roles, DEPT_LIST, DESIG_LIST)
            # # PGR RO Employee
            # username = "PGR_GRO" + cityCode
            # roles ="GRO"
            # createEmployee(auth_token, "PGR GRO",username , tenant_id, "8197292574",roles, DEPT_LIST, DESIG_LIST)
            #break
    dateStr=datetime.now().strftime("%d%m%Y%H%M%S")
    print(dateStr )
    print(post_data_list)
    print("BOUNDARIES_FOLDER",config.BOUNDARIES_FOLDER)
    with io.open(os.path.join(config.BOUNDARIES_FOLDER,"hrms-request"+str(dateStr)+".json"), mode="w", encoding="utf-8") as f:
        json.dump(post_data_list, f, indent=2,  ensure_ascii=False , cls=DateTimeEncoder)
    with io.open(os.path.join(config.BOUNDARIES_FOLDER,"hrms-response"+str(dateStr)+".json"), mode="w", encoding="utf-8") as f:
        json.dump(post_data_resp_list, f, indent=2,  ensure_ascii=False, cls=DateTimeEncoder)


if __name__ == "__main__":
    main()
