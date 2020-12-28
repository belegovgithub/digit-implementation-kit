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
import math 

ROLE_CODES = {"RO": "RO", "GRO": "GRO", "PGR-CE": "CSR", "TL Counter Employee": "TL_CEMP",
              "TL Doc Verifier": "TL_DOC_VERIFIER", "TL Field Inspector": "TL_FIELD_INSPECTOR", "TL Approver": "TL_APPROVER", "mCollect Employee": "UC_EMP", "ADMIN": "STADMIN"}


def getValue(df, row,colName,defValue="") :
    if not pd.isna(row[df.columns.get_loc(colName)] ) : 
        return str(row[df.columns.get_loc(colName)]).strip() 
    else : 
        return defValue if defValue is not None else row[df.columns.get_loc(colName)] 
def getMobileNumber(df, row,colName,defValue="") :
    if not pd.isna(row[df.columns.get_loc(colName)] ) : 
        number =row[df.columns.get_loc(colName)]
        if isinstance(number, numpy.float64) : 
            return math.trunc(number )
        else :
            return str(number).strip() 
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

def loadDesig():
 designationData={ 
  "Hindi Typist": "DESIG_43",
  "Octroi Moharir": "DESIG_65",
  "Assistant Engneer": "DESIG_45",
  "Sainitary Inspector": "DESIG_28",
  "Deputy Chief Executive Officer": "DESIG_25",
  "Revenue Inspector": "DESIG_28",
  "Account Clerk": "DESIG_34",
  "Environment Superintendent": "DESIG_39",
  "Pharmacy officer": "DESIG_74",
  "Chief Executive Officer": "DESIG_26",
  "Electric & Water Supply Foreman": "DESIG_75",
  "Asst. Enggineer": "DESIG_45",
  "Surgeon": "DESIG_76",
  "Principal": "DESIG_68",
  "Assistant Medical Officer": "DESIG_3",
  "Sectional Enggineer": "DESIG_1",
  "Resident Medical Officer": "DESIG_3",
  "Clerk": "DESIG_34",
  "Horticulturist": "DESIG_49",
  "Computer Programmer": "DESIG_48",
  "Asst. Accountant": "DESIG_41",
  "Chief Cantt. Engineering": "DESIG_51",
  "Bill Collector": "DESIG_58",
  "Electrician": "DESIG_59",
  "Administrating Officer": "DESIG_35",
  "Junior Assistant": "DESIG_27",
  "Assistant": "DESIG_71",
  "Officer In Charge": "DESIG_50",
  "Junior Engineer": "DESIG_44",
  "Health & Sanitation Superintendent": "DESIG_39",
  "Head Master": "DESIG_68",
  "Superintendent": "DESIG_39",
  "Junior clerk": "DESIG_36",
  "Typist": "DESIG_43",
  "Sub Asst. Engineer": "DESIG_45",
  "Tax Suprintendent": "DESIG_39",
  "Tax Collector": "DESIG_58",
  "Revenue Clerk": "DESIG_34",
  "Store Keeper": "DESIG_77",
  "Dak Opr": "DESIG_42",
  "Chief Revenue Suprintendent": "DESIG_38",
  "Office Superintendant": "DESIG_39",
  "Jr Enggineer (Electrical)": "DESIG_44",
  "Assistant Engineer": "DESIG_45",
  "Juniuor Clerk": "DESIG_36",
  "Cantonment Executive Engineer": "DESIG_51",
  "Forest Ranger": "DESIG_46",
  "Junior Clerk": "DESIG_36",
  "Residential Medical Officer": "DESIG_3",
  "Revenue Supdt": "DESIG_39",
  "Office Superintendent": "DESIG_39",
  "Office Suprintendent": "DESIG_39",
  "Chief Accountant": "DESIG_41",
  "Municipal Engineer": "DESIG_51",
  "Sanitary Supdt.": "DESIG_39",
  "Office.Supdt.": "DESIG_39",
  "Revenue Supdt.": "DESIG_39",
  "Office Supdt.": "DESIG_39",
  "Junior Engineer (Civil)": "DESIG_44",
  "Daftary": "DESIG_61",
  "Overseer (JE Civil)": "DESIG_44",
  "Revenue and Tax Suprintendent": "DESIG_39",
  "Head Clerk": "DESIG_30",
  "Steno": "DESIG_60",
  "Tax Inspector": "DESIG_28",
  "Ward Boy": "DESIG_79",
  "Revenue Suprintendent": "DESIG_39",
  "Second Division Clerk": "DESIG_30",
  "Cantonment Engineer": "DESIG_51",
  "Revenue Collector": "DESIG_58",
  "Tax Superintendent": "DESIG_39",
  "Executive Officer": "DESIG_35",
  "Peon": "DESIG_34",
  "Plumber": "DESIG_62",
  "Health Superintendent": "DESIG_39",
  "Junior Grade Clerk": "DESIG_36",
  "Sanitary Suprintendent": "DESIG_39",
  "Data Entry Operator": "DESIG_47",
  "Accountant": "DESIG_41",
  "Stenographer": "DESIG_60",
  "Pound Keeper": "DESIG_73",
  "Lower Division Clerk": "DESIG_36",
  "Office Supdt.-cum-Acctt.": "DESIG_39",
  "Upper Division Clerk": "DESIG_30",
  "Health Supervisor": "DESIG_70",
  "Selection Grade Clerk": "DESIG_30",
  "Sanitary Inspector": "DESIG_28",
  "Medical Officer": "DESIG_35",
  "Tax & Revenue Superintendent": "DESIG_39",
  "Junior Engineer (E&M)": "DESIG_44",
  "Drafstman": "DESIG_61",
  "Moharrar": "DESIG_35",
  "Superintendent (SWM)": "DESIG_39",
  "Cashier": "DESIG_33",
  "Office Supt": "DESIG_39",
  "Dispatcher (U/r 7)": "DESIG_35",
  "Assistant Programmer": "DESIG_67",
  "Programmer": "DESIG_48",
  "Sr. Programmer": "DESIG_48",
  "Sub Engineer": "DESIG_45",
  "Asst Engineer": "DESIG_45",
  "Jr. Electrical": "DESIG_44",
  "Junior Electrician": "DESIG_44",
  "Pump Operator": "DESIG_31",
  "Electric Lineman": "DESIG_59",
  "Senior Grade Clerk": "DESIG_30",
  "Revenue Supt": "DESIG_39",
  "Senior clerk": "DESIG_30",
  "Draftsman": "DESIG_61",
  "Senior Sanitary Inspector": "DESIG_69",
  "L&RS Suprintendent": "DESIG_39",
  "Record Keeper": "DESIG_78",
  "Personal Assistant": "DESIG_66"
 }
 return designationData 


def loadDept():
 departmentData={
  "": "DEPT_",
  "Office": "DEPT_1",
  "Executive Officer": "DEPT_1",
  "Health & Sanitation": "DEPT_3",
  "Sanitation": "DEPT_3",
  "Electricity & Water Supply": "DEPT_11",
  "Electric & Water Supply Department": "DEPT_11",
  "Water/Electricity/Engineering": "DEPT_11",
  "Water Supply Department": "DEPT_11",
  "Water Department": "DEPT_11",
  "Engineering Department": "DEPT_12",
  "Engineering Branch (Civil - B&R": "DEPT_12",
  "Tax Branch": "DEPT_13",
  "Tax Department": "DEPT_13",
  "Electrical and Water Supply": "DEPT_14",
  "Electricity Department": "DEPT_14",
  "Accounts": "DEPT_25",
  "Account": "DEPT_25",
  "Accounts Branch": "DEPT_25",
  "Revenue Section": "DEPT_37",
  "Revenue Department": "DEPT_37",
  "Revenue": "DEPT_37",
  "Main Branch": "DEPT_38",
  "Hotriculture": "DEPT_41",
  "Horticulture": "DEPT_41",
  "Admin": "DEPT_43",
  "Administration": "DEPT_43",
  "Administration/Accounts": "DEPT_43",
  "Cantt General Hospital": "DEPT_45",
  "Hospital": "DEPT_45",
  "Tax & Revenue Branch": "DEPT_46",
  "Revenue & Tax": "DEPT_46",
  "Information Technology": "DEPT_47",
  "IT": "DEPT_47",
  "Land": "DEPT_48",
  "School": "DEPT_49",
  "Receipt and Dispatch Branch": "DEPT_50",
  "Yojna": "DEPT_51",
  "Civil": "DEPT_52",
  "Health Branch": "DEPT_53",
  "Birth & Death": "DEPT_54",
  "Store": "DEPT_55",
  "Legal Branch": "DEPT_56",
  "E&M": "DEPT_57",
  "Secretary/General Administration Branch": "DEPT_43",
  "Public Works Department":"DEPT_44"
}
 return departmentData
def caller() : 
    tenantMapping={}
    print(config.TENANT_JSON,"config.TENANT_JSON")
    with io.open(config.TENANT_JSON, encoding="utf-8") as f:
        cb_module_data = json.load(f)
    for found_index, module in enumerate(cb_module_data["tenants"]):
        #print(module["description"])
        tenantMapping[module["description"].lower()]=module["code"]
        
    if not os.path.exists(os.path.join(config.HRMS_CMD_FOLDER,"LOGS")) : 
        os.mkdir(os.path.join(config.HRMS_CMD_FOLDER,"LOGS"))

    for root, dirs, files in os.walk(config.HRMS_CMD_FOLDER, topdown=True):
        for name in dirs:
            
            #print (os.path.join(root, name))
            subfolder = os.path.join(root, name)
            user_info_file =os.path.join(root, name,"User_Role Mapping.xlsx")
            if os.path.exists(user_info_file)   :
                c = root.replace(os.path.join( config.HRMS_CMD_FOLDER,  "CB "),"").lower()
                if c not in tenantMapping : 
                    print("CITY NOT FOUND",c)
                    continue
                    
                
                tenantId =tenantMapping[c]
                #print(user_info_file)
                #print("tenantid : ", tenantId)
                config.CITY_NAME=tenantId.replace("pb.","").strip().upper()
                config.HRMS_WORKBOOK=user_info_file
                print(config.CITY_NAME)
                #print(config.HRMS_WORKBOOK) 
                main()

                
def main():
    ## load default config
    userList =[]
    load_employee_creation_config()
    city = config.CITY_NAME
    tenant_id = config.TENANT + "." + city.lower()
    # if tenant_id!='pb.mhow' :
    #     return
    post_data_list=[]
    post_data_resp_list=[]
    filePath = config.HRMS_WORKBOOK  #os.path.join(config.BOUNDARIES_FOLDER, config.HRMS_EXCEL_NAME)
    print(filePath)
    if not os.path.isfile(filePath) :
        raise Exception("File Not Found ",filePath)

    auth_token = superuser_login()["access_token"]
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
 
    # if config.HRMS_CREATE_STADMIN  : 
    #     df =df.append(createSTADMIN(), ignore_index=True)
        #print("stadmin--",df)
    # if config.HRMS_CREATE_DEV_USER : 
    #     df =df.append(createDEV(), ignore_index=True)

    departmentData = loadDept()
    designationData= loadDesig()
    #print(df) 
    for ind in df.index:
 
        row = df.iloc[ind] 
        #print(row)
        headers = {'Content-Type': 'application/json'}
        details = []
        roles = []
        assignments=[]
        is_primary = True
        mobile_number = getMobileNumber(df,row,"Employee Mobile Number*",None )    
        name = getValue(df,row,"Employee Full Name*" ,None  ) 
        if pd.isna(name) or  pd.isna(mobile_number) : 
            continue
        #mobile_number=int(mobile_number)
        departments = getValue(df,row,"Department*" ,"" ) 
        role_codes = getValue(df,row,"Role Name*" ,"" ) 
        role_names = role_codes
        designation = designationData[getValue(df,row,"Designation*" ,"" )]
        #print("designation--",designation)  
        password = "Bel@1234"
        username = getValue(df,row,"Login Id UAT" ,"" )   
            
        gender = getValue(df,row,"Gender*" ,"M" )    
        fName = getValue(df,row,"Father/ Husband Name*" ,"FATHER NAME" )  
        empType =getValue(df,row,"Nature of Employment *" ,"PERMANENT" )    
        dob =getTime(df,row,"Employee Date of Birth*" )  
        emailId =getValue(df,row,"Employee Email Address*" ,"" )  
        joiningDate =getTime(df,row,"Appointed From Date*" )  
        #print("joiningDate--",joiningDate)
        address =getValue(df,row,"Correspondance Address*" ,"" )  

 
        ## Check for empty rows 
        
        
        print("========================",username,name,mobile_number,"==========================")
        # if username !="MHOW_MukeshPrajapati" :
        #   continue
        existing_employees = get_employees_by_id(
            auth_token, username, tenant_id)
        #print(existing_employees)

        roles_needed =  set(map(lambda role : ROLE_CODES[role.strip()], role_codes.split("|")))
        roles_needed.discard(None)
        if len(roles_needed)==0 : 
          continue
        roles_needed.add("EMPLOYEE")
        if 'UC_EMP' in roles_needed:
          roles_needed.add("LR_CEMP")
        if 'TL_APPROVER' in roles_needed:
          roles_needed.add("LR_APPROVER_CEO")
        print("roles_needed---",roles_needed)
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
                code =departmentData[department]
                #print("department Code",code)
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
        #print("assignments--",assignments)

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
        #print(post_data)
        post_data_list.append(post_data)
        print("--------")
        #print(post_response.json())
        post_data_resp_list.append(post_response.json())
        
        if post_response.status_code == 202 : 
            print ("User Created : ",username)
            userList.append([username])
            update_user_password(auth_token, tenant_id, username, "Bel@1234")
        print("==================================================")
        
        print("\n\n")
    dateStr=datetime.now().strftime("%d%m%Y%H%M%S")
    # Save the request /response of newly created user in same  folder for reference
    with io.open(os.path.join(config.HRMS_CMD_FOLDER,"LOGS","hrms-request_"+str(city)+"_"+str(dateStr)+".json"), mode="w", encoding="utf-8") as f:
        json.dump(post_data_list, f, indent=2,  ensure_ascii=False, cls=DateTimeEncoder)
    with io.open(os.path.join(config.HRMS_CMD_FOLDER,"LOGS","hrms-response_"+str(city)+"_"+str(dateStr)+".json"), mode="w", encoding="utf-8") as f:
        json.dump(post_data_resp_list, f, indent=2,  ensure_ascii=False, cls=DateTimeEncoder)
    with io.open(os.path.join(r"/content/drive/MyDrive/Workspace/Verified CB Data","user.csv") , mode="a+", newline="") as f:
        write = csv.writer(f) 
        print("User LIst ",userList)
        write.writerow([config.CITY_NAME]) 
        write.writerows(userList) 

if __name__ == "__main__":
    caller()
