KeyMap = {
   
"('Information of the Child', 'Date of Birth')" : "dateofbirth" ,

"('BIRTH REGISTRATION', 'Reporting Date')" : "dateofreport",

"('Information of the Child', 'First name')" : "firstname",

"('Information of the Child', 'Sex')" : "gender",

"('BIRTH REGISTRATION', 'Hospital Name')" : "hospitalid",

"('Informants Information', 'Name')" : "informantsaddress",

"('Informants Information', 'Address')" : "informantsname",

"('Information of the Child', 'Last name')" : "lastname",

"('Information of the Child', 'Middle name')" : "middlename",

"('Place of birth', 'Place of birth (House / Hoispital / Others)')" : "placeofbirth",

"('BIRTH REGISTRATION', 'Registration No')" : "registrationno",

"('Remarks ', 'Unnamed: 51_level_1')" : "remarks",

"(\"Father's Information\", 'First name')" : "firstname",

"(\"Father's Information\", 'Middle name')" : "middlename",

"(\"Father's Information\", 'Last name')" :  "lastname",

"(\"Father's Information\", 'Aadhaar Number')" : "aadharno",

"(\"Father's Information\", 'Education Qualification')" : "education",

"(\"Father's Information\", 'Email Id')" : "emailid",

"(\"Father's Information\", 'Mobile No ')" : "mobileno",

"(\"Father's Information\", 'Nationality ')" : "nationality",

"(\"Father's Information\", 'Profession ')" : "proffession",

"(\"Father's Information\", 'Religion ')" : "religion",

"(\"Mother's Information\", 'First name')" : "firstname",

"(\"Mother's Information\", 'Middle name')" : "middlename",

"(\"Mother's Information\", 'Last name')":  "lastname",

"(\"Mother's Information\", 'Aadhaar Number')" : "aadharno",

"(\"Mother's Information\", 'Education Qualification')" : "education",

"(\"Mother's Information\", 'Email Id')" : "emailid",

"(\"Mother's Information\", 'Mobile No')" : "mobileno",

"(\"Mother's Information\", 'Nationality ')" : "nationality",

"(\"Mother's Information\", 'Profession ')" : "proffession",

"(\"Mother's Information\", 'Religion ')" : "religion",

"('Permanent address of parents', 'Bldg.No & Name')" : "buildingno",

"('Permanent address of parents', 'City Name')" : "city",

"('Permanent address of parents', 'Country (India/Nepal/Others)')" : "country",

"('Permanent address of parents', 'District')" : "district",

"('Permanent address of parents', 'House No')" : "houseno",

"('Permanent address of parents', 'Locality/Post Office')" : "locality",

"('Permanent address of parents', 'Pin Number')" : "pinno",

"('Permanent address of parents', 'State')" : "state",

"('Permanent address of parents', 'Street / Lane Name')" : "streetname",

"('Permanent address of parents', 'Tehsil')" : "tehsil",

"('Address of parents at the time of Birth of the Child', 'Bldg.No & Name')" : "buildingno",

"('Address of parents at the time of Birth of the Child', 'City Name')" : "city",

"('Address of parents at the time of Birth of the Child', 'Country (India/Nepal/Others)')" : "country",

"('Address of parents at the time of Birth of the Child', 'District')" : "district",

"('Address of parents at the time of Birth of the Child', 'House No.')" : "houseno",

"('Address of parents at the time of Birth of the Child', 'Locality/Post Office')" : "locality",

"('Address of parents at the time of Birth of the Child', 'Pin Number')" : "pinno",

"('Address of parents at the time of Birth of the Child', 'State')" : "state",

"('Address of parents at the time of Birth of the Child', 'Street / Lane Name')" : "streetname",

"('Address of parents at the time of Birth of the Child', 'Tehsil')" : "tehsil",

"('Permanent address of parents', 'House No.1')" :"houseno",

"('Remarks ', 'Unnamed: 52_level_1')":"remarks",
"('Remarks ', 'Unnamed: 53_level_1')":"remarks",
"('Remarks ', 'Unnamed: 54_level_1')":"remarks",
"('Remarks ', 'Unnamed: 55_level_1')":"remarks",
"('Remarks ', 'Unnamed: 56_level_1')":"remarks",

}

genderMap = {"male":1,"female":2,"transgender":3, None: None}

hospitalMap = {
     None : "",
    "BASE HOSPITAL DELHI CANTT-10" : "delhi_1",
    "CANTONMENT HOSPITAL DELHI CANTT-10" : "delhi_2",
    "ARMY HOSPITAL R&R DELHI CANTT-10" : "delhi_3",
    "SOOD MEDICAL CENTRE DELHI CANTT-10" : "delhi_4",
    "जतोग मिलिट्री अस्पताल " : "jutogh_1",
    "कमला नेहरू अस्पताल शिमला " : "jutogh_2",
    "सैक्शन  अस्पताल जतोग " : "jutogh_3"
}

#from google.colab import drive
#drive.mount('/content/drive')
import json
import pandas as pd
import time
import os
import glob

def getListOfFiles(dirName,jsonFileMaximumDataLimit):
     listOfDir = os.listdir(dirName) 
     for dir in listOfDir:
        SubdirPath=dirName+'/'+dir
        files_list =list()
        file_list = glob.glob(SubdirPath+"/*.xlsx")
        for fileName in file_list :
            RequiredJsonFormationCode(fileName,"pb."+dir,jsonFileMaximumDataLimit)

def RequiredJsonFormationCode(filepath,TenantId,jsonFileMaximumDataLimit) :
  dfs = pd.read_excel(filepath, header=[0,1],dtype={14:str,24:str,37:str,47:str})
  #print(dfs.info(verbose=True))
  json_str = dfs.to_json(orient='records')
  parsedjson = json.loads(json_str)
  RequiredJson = []
  FinalOutput={}
  for row in parsedjson :
    output = {}
    output["birthFatherInfo"]={}
    output["birthMotherInfo"]={}
    output["birthPermaddr"]={}
    output["birthPresentaddr"]={}
    for k,v  in row.items():
        if k == "('BIRTH REGISTRATION', 'Reporting Date')" :
            v= time.strftime('%d-%m-%Y', time.localtime(int(row[k])/1000)) if (row[k] != None) else ""
            k=KeyMap[k]
            output[k]=v
        elif k == "('Information of the Child', 'Date of Birth')" :
            v=time.strftime('%d-%m-%Y', time.localtime(int(row[k])/1000)) if (row[k] != None) else ""
            k=KeyMap[k]
            output[k]=v    
        elif "Father" in k :
            output["birthFatherInfo"][KeyMap[k]]=v
        elif "Mother" in k :
            output["birthMotherInfo"][KeyMap[k]]=v
        elif "Permanent" in k :
            output["birthPermaddr"][KeyMap[k]]=v
        elif "Address of parents at the time of Birth of the Child" in k :
            output["birthPresentaddr"][KeyMap[k]]=v
        elif k== "('Information of the Child', 'Sex')"  : 
             k=KeyMap[k]
             v = v.replace(" ","").lower() if (v != None) else None
             v= genderMap[v]
             output[k]=v
        elif k== "('BIRTH REGISTRATION', 'Hospital Name')" :
             k=KeyMap[k]
             output[k]= hospitalMap.get(k)
             if hospitalMap.get(k)=="":
               print("Unknown hospital ",k) 
        elif ( k== "('Permanent address of parents', 'Pin Number')" or k== "('Address of parents at the time of Birth of the Child', 'Pin Number')" ):
             k=KeyMap[k]
             if type(v) != type(None) :
                output[k]=int(v)
        else :
            if (KeyMap.get(k) != None):
              k=KeyMap.get(k)
              output[k]=v
            else:
              print("Unknown Column: ",k)
            output["counter"]=1
            output["tenantid"]=TenantId  
    FinalOutput=output
    RequiredJson.append(FinalOutput)
  #RequiredOutputFormat=RequiredJson
  RequiredOutputFormat=json.dumps(RequiredJson ,indent=4) #indent=0
  #print(RequiredOutputFormat)
  with open(filepath.replace(".xlsx",".txt"), 'w') as writefile:
    writefile.write(RequiredOutputFormat)

def main():
  
  ### if user give FullFilePath, use this code
  #fullPath='/content/drive/My Drive/BEL (Private Folder)/BirthCerts/Contonment_List/dalhousie/dalhousie_Data.xlsx'
  #tenantId="pb.delhi"
  JsonFileMaximumDataLimit=4000
  #RequiredJsonFormationCode(fullPath,tenantId)
  #if user give only MainPath, use this code
  Mainpath='/content/drive/My Drive/BEL (Private Folder)/BirthCerts/Contonment_List/trial'
  getListOfFiles(Mainpath,JsonFileMaximumDataLimit)
if __name__ == '__main__':
  main()