#from google.colab import drive
#drive.mount('/content/drive')
import json
import pandas as pd
import time
from datetime import datetime

msg = 'Birth Certificate Record Details'
print(msg)
def main():
  dfs = pd.read_excel('E:\EChhawani\BnD\RealData\delhi\Birth 2017 test small.xlsx', header=[2,3])
  json_str = dfs.to_json(orient='records')
  parsedjson = json.loads(json_str)
  jsoninput=json.dumps(parsedjson, indent=4)
  #print(jsoninput)
  KeyMap = {
   
"('Information of the Child', 'Date of Birth')" : "dateofbirth" ,

"('BIRTH REGISTRATION', 'Reporting Date')" : "dateofreport",

"('Information of the Child', 'First name')" : "firstname",

"('Information of the Child', 'Sex')" : "gender",

"('BIRTH REGISTRATION', 'Hospital Name')" : "hospitalname",

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

"('Permanent address of parents', 'House No.1')" : "houseno",

"('Remarks ', 'Unnamed: 52_level_1')":"remarks",
"('Remarks ', 'Unnamed: 53_level_1')":"remarks",
"('Remarks ', 'Unnamed: 54_level_1')":"remarks",
"('Remarks ', 'Unnamed: 55_level_1')":"remarks"

}
  RequiredJson = []
  output = {}
  output["birthFatherInfo"]={}
  output["birthMotherInfo"]={}
  output["birthPermaddr"]={}
  output["birthPresentaddr"]={}
  for row in parsedjson :
    for k,v  in row.items():
        if k == "('BIRTH REGISTRATION', 'Reporting Date')" :
            #print(type(row[k]))
            v=time.strftime('%d-%m-%Y', time.localtime(int(row[k])/1000))
            #v=datetime.datetime.strptime(v,'%d-%m-%Y')
            #v=.strftime('%d-%m-%Y', time.gmtime(row[k]/1000))
            #v=datetime.strptime((row[k]/1000), "%d%m%Y").date()
            k=KeyMap[k]
            output[k]=v
        elif k == "('Information of the Child', 'Date of Birth')" :
            print("check", row[k])

            v=time.strftime('%d-%m-%Y', time.localtime(int(row[k])/1000))
            #v=time.strftime('%d-%m-%Y', time.localtime(row[k]/1000))
            #v=time.strftime("%d-%m-%Y", time.gmtime(row[k]/1000))
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
        else :
           k=KeyMap[k]
           output[k]=v
           output["counter"]=1
           output["tenantid"]="pb.delhi" 
           output["hospitalid"]="delhi_1"
           #if k=='dateofreport' : 
             #output[k]=pd.to_datetime(output[k], format='%d-%m-%Y')
             #output[k] = datetime.strptime( output[k].astype('int').to_string() ,'%Y%m%d')
             #output[k].astype(str).apply(lambda x:datetime.datetime.strptime(x,'%Y%m%d'))
    RequiredJson.append(output)
  #RequiredOutputFormat=RequiredJson
  RequiredOutputFormat=json.dumps(RequiredJson) #indent=0
  print(RequiredOutputFormat)

if __name__ == '__main__':
  main()  