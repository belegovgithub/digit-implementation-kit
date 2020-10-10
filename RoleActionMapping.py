from common import *
from config import config
import io
import os
import numpy
from pathlib import Path
import pandas as pd
## To Generate Role action Mapping from data.
def main():
    #config.MDMS_LOCATION=r"/content/egov-mdms-data/data/pg"
    action_path=os.path.join(config.MDMS_LOCATION,"ACCESSCONTROL-ACTIONS-TEST","actions-test.json")
    with io.open(action_path, encoding="utf-8") as f:
        action_data = json.load(f)
    role_action_path=os.path.join(config.MDMS_LOCATION,"ACCESSCONTROL-ROLEACTIONS","roleactions.json")
    with io.open(role_action_path, encoding="utf-8") as f:
        role_action_data = json.load(f)
    
    role_path=os.path.join(config.MDMS_LOCATION,"ACCESSCONTROL-ROLES","roles.json")
    with io.open(role_path, encoding="utf-8") as f:
        role_data = json.load(f)
 

    actions ={}
    for found_index, action in enumerate(action_data["actions-test"]) :
        #print(found_index,role)
        actions[action["id"]]=action

    roles ={}
    for found_index, role in enumerate(role_data["roles"]) :
        #print(found_index,role)
        roles[role["code"]]=role
    names=["Role","RoleName","ActionId","Action name","Action url","Action displayName","Action serviceCode","Action code","Action path"]
    df =pd.DataFrame(columns=names)
    invalidActionList=[]
    invalidRoleList=[]
    for found_index, roleaction in enumerate(role_action_data["roleactions"]) :
      if  roleaction["rolecode"] in roles  :
        if roleaction["actionid"] in actions :
          dictObj ={
              "Role" : roleaction["rolecode"] , 
              "RoleName" : roles[roleaction["rolecode"]]["name"],
              "ActionId" : roleaction["actionid"],
              "Action name" : actions[roleaction["actionid"]]["name"],
              "Action url" : actions[roleaction["actionid"]]["url"],
              "Action displayName" : actions[roleaction["actionid"]]["displayName"] if  "displayName" in actions[roleaction["actionid"]] else "",
              "Action serviceCode" : actions[roleaction["actionid"]]["serviceCode"] if  "serviceCode" in actions[roleaction["actionid"]] else ""  ,
              "Action code" : actions[roleaction["actionid"]]["code"] if  "code" in actions[roleaction["actionid"]] else "",
              "Action path" : actions[roleaction["actionid"]]["path"] if  "path" in actions[roleaction["actionid"]] else "" 

          }
          df = df.append(dictObj , ignore_index=True)
        else : 
          invalidActionList.append(roleaction["actionid"]) 
          #print ( "No Action Exist for ", roleaction["actionid"])  
      else : 
        invalidRoleList.append(roleaction["rolecode"])
        #print ("No Role Action Exist for ",roleaction["rolecode"] ,roleaction["actionid"])

    print("Invalid Actions :: ",invalidActionList)
    print("Invalid Roles :: ",invalidRoleList)
    #roles[roleaction["rolecode"]]=role
    df.to_csv(os.path.join(config.MDMS_LOCATION,"USR_ROLEMAPPING.csv"),  header=True,index=False)
 
if __name__ == "__main__":
    main()