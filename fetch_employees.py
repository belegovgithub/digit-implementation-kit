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

def get_hrms_employees(auth_token, **kwargs):
    data = requests.post(url=config.HOST + '/egov-hrms/employees/_search',
                            json={
                                **{
                                    "RequestInfo": {
                                        "authToken": auth_token
                                    }
                                }, **kwargs,
                            })
    return data.json()["Employees"]
   

def main() : 
    output_folder = r"D:\CB\UsersList\Users"
    load_employee_creation_config()
    auth_token = superuser_login()["access_token"]
    df = pd.DataFrame(columns=['TenantID', 'LoginID', 'Roles'])
    existing_employees = get_hrms_employees( auth_token  )
    with io.open(os.path.join(output_folder, "users.json"), mode="w", encoding="utf-8") as f:
        json.dump(existing_employees, f, indent=2,  ensure_ascii=False, cls=DateTimeEncoder)
    for emp in existing_employees : 
        user =emp["user"]
        roles =user["roles"] 
        li = [item.get('name') for item in roles]
        row ={
            'TenantID' : user["tenantId"],
            'LoginID' :  user["userName"],
            'Roles' : " , ".join(li)
        }
        df= df.append(row, ignore_index=True)
    df.to_csv(os.path.join(output_folder,"users.csv"))
     
        
if __name__ == "__main__":
    main()
