from common import *
from config import config
import io
import os 
import sys
from common import superuser_login
from PropertyTax import *
import pandas as pd
import openpyxl
import collections
import re
from CreateWaterConnection import *
from CreateSewerageConnection import *

# class CreateProprty(Property):
#     def __init__(self, *args, **kwargs):
#         super(CreateProprty, self).__init__()
#         self.additional_details = {}
#         self.property_details = [PropertyDetail(owners=[], additional_details={
#             "inflammable": False,
#             "heightAbove36Feet": False
#         })]


# def readExcel():
#     wb = openpyxl.load_workbook(os.path.join(filePath,fileName+".xlsx"))

INDEX_SL_NO = 0
INDEX_ABAS_PROPERTY_ID = 1
INDEX_OLD_PROPERTY_ID = 2
INDEX_PROPERTY_TYPE = 3
INDEX_TOTAL_LAND_AREA = 4
INDEX_TOTAL_CONSTRUCTED_AREA = 5
INDEX_USAGE_TYPE = 6
INDEX_TENANT_REGIONNAME = 7
INDEX_TENANT_REGIONCODE = 8
INDEX_TENANT_LATITUDE = 9
INDEX_TENANT_LONGITUDE = 10
INDEX_TENANT_CONTACT = 12
INDEX_TENANT_EMAIL = 13
INDEX_TENANT_ADDRESS = 14
INDEX_TENANT_FB = 17
INDEX_TENANT_TWITTER = 18
INDEX_TENANT_POPULATION = 20
INDEX_TENANT_GRADE = "Cantonment Board"
INDEX_STATE = 30
INDEX_CITY_HINDI = 31
INDEX_DISTRICT_HINDI = 32
INDEX_STATE_HINDI = 33


def main():
    Flag =False
    tenantMapping={}
    count = 0
    with io.open(config.TENANT_JSON, encoding="utf-8") as f:
        cb_module_data = json.load(f)
        for found_index, module in enumerate(cb_module_data["tenants"]):
            if module["city"]["ulbGrade"]=="ST":
                continue
            tenantMapping[module["code"].lower()]=module["code"].lower()[3:]

    # Iterate all cbs
    # for root, dirs, files in os.walk(r"D:\eGov\Data\WS\Template\Property", topdown=True):
    #     for name in dirs:          
    #         subfolder = os.path.join(root, name)         
    #         city = subfolder.replace(r"D:\eGov\Data\WS\Template\Property\CB ","" ).strip().lower()
    #         city = "pb." + city

    #         if city not in tenantMapping:
    #             print("Not In city",city)
    #             continue
    #         cityname = tenantMapping[city]
    #         print(cityname)
    #         propertyFile =os.path.join(root, name,'Template for Existing Property-Integrated with ABAS-' + cityname + '.xlsx')
    #         waterFile = os.path.join(root, name,"Template for Existing Water Connection Detail.xlsx")
    #         sewerageFile = os.path.join(root, name,"Template for Existing Sewerage Connection Detail.xlsx")
    #         logfile = open(os.path.join(root, name,"Logfile.txt"), "w")            
    #         # validate = enterDefaultMobileNo(propertyFile, tenantMapping, cityname, waterFile, sewerageFile,logfile) 
    #         # if(validate == False):                
    #         #     print('Data validation Failed for mobile entry, Please check the log file.') 
    #         #     return
    #         validate =  validateDataForProperty(propertyFile, logfile)            
    #         if(validate == False):                
    #             print('Data validation for property Failed, Please check the log file.') 
    #             # return
    #         else:
    #             print('Data validation for property success.')
    #         # if os.path.exists(propertyFile) :                  
    #         #     wb_property = openpyxl.load_workbook(propertyFile) 
    #         #     sheet1 = wb_property.get_sheet_by_name('Property Assembly Detail')   
    #         #     sheet2 = wb_property.get_sheet_by_name('Property Ownership Details')
    #         #     localitySheet = wb_property.get_sheet_by_name('Locality')
    #         #     df = pd.read_excel(propertyFile, sheet_name='Locality', usecols=['Locality Name', 'Code'])
    #         #     locality_data = {}
    #         #     for ind in df.index: 
    #         #         locality_data[df['Locality Name'][ind]] =  df['Code'][ind]    
    #         #     createPropertyJson(sheet1, sheet2, locality_data,cityname, logfile, root, name)                
    #         #     wb_property.save(propertyFile)        
    #         #     wb_property.close()
    #         # else:
    #         #     print("Property File doesnot exist for ", cityname) 
            
    #         if os.path.exists(waterFile) : 
    #             ProcessWaterConnection(propertyFile, waterFile, logfile, root, name,  cityname)  
    #         else:
    #             print("Water File doesnot exist for ", cityname) 
    #         logfile.close()

    # Doing for one cb at a time
    cityname = 'varanasi'
    root = r'D:\eGov\Data\WS\Template\WaterSewerageTemplates'
    name = 'CB ' + cityname.lower()
    propertyFile =os.path.join(root, name,'Template for Existing Property-Integrated with ABAS-' + cityname + '.xlsx')
    waterFile = os.path.join(root, name, "Template for Existing Water Connection Detail.xlsx")
    sewerageFile = os.path.join(root, name, "Template for Existing Sewerage Connection Detail.xlsx")
    logfile = open(os.path.join(root, name, "Logfile.txt"), "w")            
    # validate = enterDefaultMobileNo(propertyFile, tenantMapping, cityname, waterFile, sewerageFile,logfile) 
    # if(validate == False):                
    #     print('Data validation Failed for mobile entry, Please check the log file.') 
    #     return
    
    if os.path.exists(propertyFile) :  
        validate =  validateDataForProperty(propertyFile, logfile)            
        if(validate == False):                
            print('Data validation for property Failed, Please check the log file.') 
            # return
        else:
            print('Data validation for property success.')                
        wb_property = openpyxl.load_workbook(propertyFile) 
        sheet1 = wb_property.get_sheet_by_name('Property Assembly Detail')   
        sheet2 = wb_property.get_sheet_by_name('Property Ownership Details')
        localitySheet = wb_property.get_sheet_by_name('Locality')
        df = pd.read_excel(propertyFile, sheet_name='Locality', usecols=['Locality Name', 'Code'])
        locality_data = {}
        for ind in df.index: 
            locality_data[df['Locality Name'][ind]] =  df['Code'][ind]    
        # createPropertyJson(sheet1, sheet2, locality_data,cityname, logfile, root, name)                
        # wb_property.save(propertyFile)        
        # wb_property.close()
    else:
        print("Property File doesnot exist for ", cityname) 
    
    if os.path.exists(waterFile) : 
        ProcessWaterConnection(propertyFile, waterFile, logfile, root, name,  cityname)  
    else:
        print("Water File doesnot exist for ", cityname) 

    if os.path.exists(sewerageFile) : 
        ProcessSewerageConnection(propertyFile, sewerageFile, logfile, root, name,  cityname)  
    else:
        print("Water File doesnot exist for ", cityname) 
    logfile.close()        


def validateDataForProperty(propertyFile, logfile):
    validated = True
    reason = ''
    try:
        wb_property = openpyxl.load_workbook(propertyFile) 
        sheet1 = wb_property.get_sheet_by_name('Property Assembly Detail')   
        sheet2 = wb_property.get_sheet_by_name('Property Ownership Details')
        abas_ids = []        
        reason = 'Property file validation starts.\n'
        print(reason)
        logfile.write(reason)
        print('no. of rows in Property file sheet 1: ', sheet1.max_row) 
        for row in sheet1.iter_rows(min_row=3, max_col=42, max_row=sheet1.max_row,values_only=True): 
            if pd.isna(row[0]):
                validated = False
                reason = 'Sl no. column is empty\n'
                logfile.write(reason)
                break
            if pd.isna(row[1]):
                validated = False
                reason = 'Property File sheet1 data validation failed for sl no. '+ str(row[0]) + ', abas property id  is empty.\n'
                logfile.write(reason)
            if pd.isna(row[27]):
                validated = False
                reason = 'Property File sheet1 data validation failed for sl no. '+ str(row[0]) + ',  ownership type is empty.\n'
                logfile.write(reason)
            if(str(row[27]) != "Multiple Owners"):
                if pd.isna(row[28]):
                    validated = False
                    reason = 'Property File sheet1 data validation failed for sl no. '+ str(row[0]) + ', name is empty.\n'
                    logfile.write(reason)
                if pd.isna(row[29]):
                    validated = False
                    reason = 'Property File data sheet1 validation failed for sl no. '+ str(row[0]) + ', mobile no. is empty.\n'
                    logfile.write(reason)
                elif(len(str(row[29]).strip()) != 10):
                    validated = False
                    reason = 'Property File data sheet1 validation failed, Mobile number not correct for sl no. '+ str(row[0]) +'\n'
                    logfile.write(reason)
                if not pd.isna(row[28]):
                    if not bool(re.match("[a-zA-Z \\.]+$",str(row[28]))):
                        validated = False
                        reason = 'Name has invalid characters for sl no. '+ str(row[0]) +'\n'
                        logfile.write(reason)
            if pd.isna(row[7]):
                validated = False
                reason = 'Property File data validation failed for sl no. '+ str(row[0]) + ', usage category is empty.\n'
                logfile.write(reason)
            elif(str(row[7]).strip() == 'Commercial ( Nonresidential )' or str(row[7]).strip() == 'Institutional ( Nonresidential )'
                    or str(row[7]).strip() == 'Industrial ( Nonresidential )' or str(row[7]).strip() == 'Others ( Nonresidential )'):
                if pd.isna(row[8]):
                    validated = False
                    reason = 'Property File data validation failed for sl no. '+ str(row[0]) + ', sub usage category is empty.\n'
                    logfile.write(reason)
            

        for index in range(3, sheet1.max_row):
            try: 
                if pd.isna(sheet1['A{0}'.format(index)].value):
                    validated = False
                    reason = 'Sl no. column is empty\n'
                    logfile.write(reason)
                    break
                abas_ids.append(sheet1['B{0}'.format(index)].value.strip())
            except Exception as ex:
                print("validateDataForProperty Exception: abas id is empty: ",ex)
        duplicate_ids = [item for item, count in collections.Counter(abas_ids).items() if count > 1]
        if(len(duplicate_ids) >= 1):
            validated = False
            reason = 'Property File data validation failed. ' +'Duplicate abas property id for '+ str(duplicate_ids) +'\n'
            logfile.write(reason)        
        for row in sheet2.iter_rows(min_row=3, max_col=12, max_row=sheet2.max_row,values_only=True):
            if not pd.isna(row[0]):
                if pd.isna(row[3]):
                    validated = False
                    reason = 'Property File data validation failed for abas id  '+ str(row[0]) + ', mobile no. is empty in multiple owner sheet.\n'
                    logfile.write(reason)
                if pd.isna(row[2]):
                    validated = False
                    reason = 'Property File data validation failed for abas id  '+ str(row[0]) + ', name is empty.\n'
                    logfile.write(reason)
                if(len(str(row[3])) != 10):
                    validated = False
                    reason = 'Property File data validation failed, Mobile number not correct for abas id '+ str(row[0]) +'\n'
                    logfile.write(reason)
                if not pd.isna(row[2]):
                    if not bool(re.match("[a-zA-Z \\.]+$",str(row[2]))):
                        validated = False
                        reason = 'Property File data validation failed, Name has invalid characters for abas id '+ str(row[0]) +'\n'
                        logfile.write(reason)
    except Exception as ex:
        print("validateDataForProperty Exception: ",ex)
    reason = 'Property file validation ends.\n'
    print(reason)
    logfile.write(reason)
    return validated

                    
def enterDefaultMobileNo(propertyFile, tenantMapping, cityname, waterFile, sewerageFile, logfile):
    validated = True
    search_key = 'pb.'+ cityname
    res = list(tenantMapping.keys()).index(search_key)
    res = res+1
    res = res* 100000
    mobileNumber = 3000000000 + res + 0
    owner_obj = {}
    try:
        if os.path.exists(propertyFile) : 
            wb_property = openpyxl.load_workbook(propertyFile) 
            sheet1 = wb_property.get_sheet_by_name('Property Assembly Detail')   
            sheet2 = wb_property.get_sheet_by_name('Property Ownership Details')        
            for i in range(3, sheet1.max_row):
                abas_id = sheet1['B{0}'.format(i)].value.strip()
                for row in sheet1.iter_rows(min_row=i, max_col=42, max_row=i,values_only=True):                    
                    owner = {}               
                    owner['mobileNumber'] = getValue(str(row[29]).strip(),str,"")
                    owner['ownerType'] = str(row[27]).strip()
                    if abas_id not in owner_obj:
                        owner_obj[abas_id] = []
                    owner_obj[abas_id].append(owner)
            index = 2
            for row in sheet1.iter_rows(min_row=3, max_col=42, max_row=sheet1.max_row,values_only=True):
                index = index + 1
                if pd.isna(row[1]):
                    continue 
                if (str(row[27]).strip() != 'Multiple Owners'):
                    if pd.isna(row[29]):
                        mobileNumber = mobileNumber + 1                    
                        value = 'AD{0}'.format(index) + '    ' +str(mobileNumber) + '\n'
                        logfile.write(value)
                        sheet1['AD{0}'.format(index)].value = mobileNumber
            index = 1
            for row in sheet2.iter_rows(min_row=2, max_col=5, max_row=sheet2.max_row,values_only=True): 
                index = index + 1 
                if pd.isna(row[0]):
                    print("empty abas id in property file sheet2 while property validation")
                    logfile.write("empty abas id in property file sheet2 while property validation")
                    return 
                if pd.isna(row[3]):
                    mobileNumber = mobileNumber + 1
                    value = 'D{0}'.format(index) + '    ' +str(mobileNumber) + '\n'
                    logfile.write(value)
                    sheet2['D{0}'.format(index)].value = mobileNumber
            wb_property.save(propertyFile)        
            wb_property.close()
        else:
            print("Property File doesnot exist for ", cityname)  

        if os.path.exists(waterFile) :
            wb_water = openpyxl.load_workbook(waterFile) 
            water_sheet = wb_water.get_sheet_by_name('Water Connection Details') 
            index = 2
            for row in water_sheet.iter_rows(min_row=3, max_col=5, max_row=water_sheet.max_row,values_only=True):
                index = index + 1
                if pd.isna(row[0]):
                    continue
                if(str(row[3]).strip() == 'No'):
                    if pd.isna(row[4]):
                        mobileNumber = mobileNumber + 1
                        value = 'E{0}'.format(index) + '    ' +str(mobileNumber) + '\n'
                        logfile.write(value)
                        water_sheet['E{0}'.format(index)].value = mobileNumber
                
            wb_water.save(waterFile)        
            wb_water.close()
            wb_water = openpyxl.load_workbook(waterFile) 
            water_sheet = wb_water.get_sheet_by_name('Water Connection Details')
            for row in water_sheet.iter_rows(min_row=3, max_col=5, max_row=water_sheet.max_row,values_only=True):
                if pd.isna(row[0]):
                    continue
                if(str(row[3]).strip() == 'Yes'):
                    for obj in owner_obj[str(row[1]).strip()]:
                        if(len(obj['mobileNumber']) == 0):
                            validated = False
                            reason = 'Mobile number in property is not available as in water template same as owner detail for abas id. '+ str(row[1]).strip() +'\n'
                            print(reason)
                            logfile.write(reason)
        else:
            print("Water File doesnot exist for ", cityname)  

        if os.path.exists(sewerageFile) :
            wb_sewerage = openpyxl.load_workbook(sewerageFile) 
            sewerage_sheet = wb_sewerage.get_sheet_by_name('Sewerage Connection Details') 
            index = 2
            for row in sewerage_sheet.iter_rows(min_row=3, max_col=5, max_row=sewerage_sheet.max_row,values_only=True):
                index = index + 1
                if pd.isna(row[0]):
                    continue
                if(str(row[3]).strip() == 'No'):
                    if pd.isna(row[4]):
                        mobileNumber = mobileNumber + 1
                        value = 'E{0}'.format(index) + '    ' +str(mobileNumber) + '\n'
                        logfile.write(value)
                        sewerage_sheet['E{0}'.format(index)].value = mobileNumber
                
            wb_sewerage.save(sewerageFile)        
            wb_sewerage.close()
            wb_sewerage = openpyxl.load_workbook(sewerageFile) 
            sewerage_sheet = wb_sewerage.get_sheet_by_name('Sewerage Connection Details') 
            for row in sewerage_sheet.iter_rows(min_row=3, max_col=10, max_row=sewerage_sheet.max_row,values_only=True):
                if pd.isna(row[0]):
                    continue
                if(str(row[3]).strip() == 'Yes'):
                    for obj in owner_obj[str(row[1]).strip()]:
                        if(len(obj['mobileNumber']) == 0):
                            validated = False
                            reason = 'Mobile number in property is not available as in sewerage template same as owner detail for abas id. '+ str(row[1]).strip() +'\n'
                            logfile.write(reason)

        else:
            print("Sewerage File doesnot exist for ", cityname) 
    except Exception as ex:
        print("enterDefaultMobileNo Exception: ",ex)

    return validated

def createPropertyJson(sheet1, sheet2, locality_data,cityname, logfile,root, name):
    # abas_ids_multiple_owner = []
    # for index in range(2, sheet2.max_row):
    #     abas_ids_multiple_owner.append(sheet2['A{0}'.format(index)].value)
    createdCount = 0
    searchedCount = 0
    notCreatedCount = 0

    multiple_owner_obj = {}
    for i in range(2, sheet2.max_row):   
        try:     
            abas_id = sheet2['A{0}'.format(i)].value.strip()
            for row in sheet2.iter_rows(min_row=i, max_col=12, max_row=i,values_only=True):                    
                owner = Owner()
                Owner.status = 'ACTIVE'
                owner.name = getValue(str(row[2]).strip(),str,"NAME")
                owner.mobileNumber = getValue(str(row[3]).strip(),str,"3000000000")
                owner.emailId = getValue(str(row[4]).strip(),str,"")
                owner.gender = process_gender(str(row[5]).strip())
                owner.fatherOrHusbandName = getValue(str(row[7]).strip(),str,"Guardian")
                owner.relationship =  process_relationship(str(row[8]).strip())
                owner.sameAsPeropertyAddress = getValue(str(row[9]).strip(),str,"Yes")            
                owner.ownerType =  process_special_category(str(row[11]).strip())
                if abas_id not in multiple_owner_obj:
                    multiple_owner_obj[abas_id] = []
                multiple_owner_obj[abas_id].append(owner)
        except Exception as ex:
            print("createPropertyJson Exception: ",ex)
    index = 2
    for row in sheet1.iter_rows(min_row=3, max_col=42, max_row=sheet1.max_row,values_only=True):       
        try:   
            index = index + 1  
            property = Property()  
            property.abasPropertyId =  getValue(str(row[1]).strip(),str,None)
            if pd.isna(property.abasPropertyId):
                print("empty Abas id in property file")
                return     
            
            locality = Locality()
            address  = Address()
            owner = Owner()
            unit = Unit()
            constructionDetail = ConstructionDetail()
            institution = Institution()
            additionalDetail = AdditionalDetails()
            tenantId = 'pb.'+ cityname
            property.tenantId = tenantId
            
            property.oldPropertyId =  getValue(str(row[2]).strip(),str,None)
            property.propertyType = process_property_type(str(row[3]).strip())
            property.landArea = getValue(row[4],int,1) 
            property.superBuiltUpArea = getValue(row[5],int,1) 
            property.usageCategory = process_usage_type(str(row[7]).strip())
            property.subUsageCategory = process_sub_usage_type(str(row[8]).strip())   
            if pd.isna(row[13]):
                locality.code = "LOCAL_OTHERS"   
            else:    
                locality.code = locality_data[row[13].strip()]
            address.city = cityname
            address.locality = locality
            address.location = process_location(str(row[20]).strip())
            address.street = getValue(row[16].strip(),str,"")
            address.buildingName = getValue(row[17].strip(),str,"")
            address.doorNo = getValue(str(row[18]).strip(),str,"")
            address.pincode = getValue(str(row[19]).strip(),str,"")
            correspondence_address = get_propertyaddress(address.doorNo,address.buildingName,getValue(str(row[13]).strip(),str,"Others"),cityname)
            unit.occupancyType = process_occupancy_type(str(row[9]).strip())
            unit.arv = getValue(row[21],int,0) 
            if(len(property.subUsageCategory) == 0):
                unit.usageCategory = property.usageCategory
            else:                
                unit.usageCategory = property.subUsageCategory
            constructionDetail.builtUpArea = getValue(row[5],int,1) 
            unit.construction_detail = constructionDetail        
            property.address = address
            property.units = []
            property.units.append(unit)
            property.owners = []
            # converter = lambda  x,y  : x  if x is not pd.isna else y
            property.noOfFloors = getValue(row[10],int,1) 
            property.noOfFlats = getValue(row[11],int,0) 
            financial_year = getValue(row[23],str,"2020-2021").replace("-20", "-")
            property.financialYear = financial_year
            property.ownershipCategory = process_ownership_type(str(row[27]).strip())     
            if(property.ownershipCategory == 'INDIVIDUAL.SINGLEOWNER'):
                owner.status = 'ACTIVE'            
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
                
                property.owners.append(owner)
            elif(property.ownershipCategory == 'INSTITUTIONALPRIVATE'):
                owner.status = 'ACTIVE'
                owner.name = getValue(str(row[28]).strip(),str,"NAME")
                owner.mobileNumber = getValue(str(row[29]).strip(),str,"3000000000")
                owner.emailId = getValue(str(row[30]).strip(),str,"")
                owner.sameAsPeropertyAddress = getValue(str(row[35]).strip(),str,"Yes")
                owner.correspondenceAddress = getValue(str(row[36]).strip(),str,"")
                institution.name = getValue(str(row[38]).strip(),str,"Institution")
                institution.type = process_private_institution_type(str(row[39]).strip())
                institution.designation = getValue(str(row[40]).strip(),str,"Designation")
                owner.altContactNumber = getValue(str(row[41]).strip(),str,"1000000000")
                if(owner.sameAsPeropertyAddress ==  'Yes'):
                    owner.correspondenceAddress = correspondence_address
                else: 
                    owner.correspondenceAddress = getValue(str(row[36]).strip(),str,"Correspondence")
                property.institution = institution
                property.owners.append(owner)
            elif(property.ownershipCategory == 'INSTITUTIONALGOVERNMENT'):
                owner.status = 'ACTIVE'
                owner.name = getValue(str(row[28]).strip(),str,"NAME")
                owner.mobileNumber = getValue(str(row[29]).strip(),str,"3000000000")
                owner.emailId = getValue(str(row[30]).strip(),str,"")
                owner.sameAsPeropertyAddress = getValue(str(row[35]).strip(),str,"Yes")
                owner.correspondence_address = getValue(str(row[36]).strip(),str,"")
                institution.name = getValue(str(row[38]).strip(),str,"Institution")
                institution.type = process_govt_institution_type(str(row[39]).strip())
                institution.designation = getValue(str(row[40]).strip(),str,"Designation")
                owner.altContactNumber = getValue(str(row[41]).strip(),str,"1000000000")
                owner.sameAsPeropertyAddress = getValue(str(row[35]).strip(),str,"Yes")
                if(owner.sameAsPeropertyAddress ==  'Yes'):
                    owner.correspondenceAddress = correspondence_address
                else: 
                    owner.correspondenceAddress = getValue(str(row[36]).strip(),str,"Correspondence")
                property.institution = institution
                property.owners.append(owner)
            elif(property.ownershipCategory == 'INDIVIDUAL.MULTIPLEOWNERS'):
                for owner_obj in multiple_owner_obj[property.abasPropertyId]:
                    owner = owner_obj
                    owner.status = 'ACTIVE'  
                    if(owner.sameAsPeropertyAddress ==  'Yes'):
                        owner.correspondenceAddress = correspondence_address
                    else: 
                        owner.correspondenceAddress = getValue(str(row[36]).strip(),str,"Correspondence")
                    property.owners.append(owner)

                # occurances = [i for i,x in enumerate(abas_ids_multiple_owner) if x == property.abas_property_id]
                # for i in occurances:                
                #     for row in sheet2.iter_rows(min_row=i+2, max_col=12, max_row=i+2,values_only=True):                    
                #         owner = Owner()
                #         owner.status = 'ACTIVE'
                #         owner.name = getValue(str(row[2]).strip(),str,"NAME")
                #         owner.mobileNumber = getValue(str(row[3]).strip(),str,"3000000001")
                #         owner.emailId = getValue(str(row[4]).strip(),str,"")
                #         owner.gender = process_gender(str(row[5]).strip())
                #         owner.fatherOrHusbandName = getValue(str(row[7]).strip(),str,"Guardian")
                #         owner.relationship =  process_relationship(str(row[8]).strip())
                #         owner.sameAsPeropertyAddress = getValue(str(row[9]).strip(),str,"Yes")
                #         if(owner.sameAsPeropertyAddress ==  'Yes'):
                #             owner.correspondenceAddress = correspondence_address
                #         else: 
                #             owner.correspondenceAddress = getValue(str(row[10]).strip(),str,"Correspondence")
                #         owner.ownerType =  process_special_category(str(row[11]).strip())
                #         property.owners.append(owner)

            additionalDetail.isRainwaterHarvesting = False
            property.additional_details= additionalDetail
            property.source = 'MUNICIPAL_RECORDS'
            property.channel = 'MIGRATION'
            property.creationReason = 'DATA_UPLOAD'
            # print('property ', property.get_property_json())
            auth_token = superuser_login()["access_token"]
            status, res = property.search_abas_property(auth_token, tenantId, property.abasPropertyId)
        except Exception as ex:
            print("createPropertyJson Exception: ",ex)

        if(len(res['Properties']) == 0):
            statusCode, res = property.upload_property(auth_token, tenantId, property.abasPropertyId,root, name,)
            with io.open(os.path.join(root, name,"property_create_res.json"), mode="w", encoding="utf-8") as f:
                json.dump(res, f, indent=2,  ensure_ascii=False)
            propertyId = ''
            if(statusCode == 200 or statusCode == 201):
                for found_index, resProperty in enumerate(res["Properties"]):
                    propertyId = resProperty["propertyId"]
                    value = 'B{0}'.format(index) + '    ' + str(propertyId) + '\n'
                    logfile.write(value)
                    sheet1['AQ{0}'.format(index)].value = propertyId
                    reason = 'property created for abas id ' + str(property.abasPropertyId)
                    logfile.write(reason)
                    print(reason)
                    createdCount = createdCount + 1
            else:
                reason = 'property not created status code '+ str(statusCode) + ' for abas id ' + str(property.abasPropertyId) + ' response: ', str(res)  + '\n'
                logfile.write(reason)
                print(reason)
                notCreatedCount = notCreatedCount + 1
        else:
            reason = 'property already exist for abas id '+ str(property.abasPropertyId) + '\n'
            logfile.write(reason)
            print(reason)
            searchedCount = searchedCount + 1

    reason = 'property created count: '+ str(createdCount)
    print(reason)
    reason = 'property not created count: '+ str(notCreatedCount)
    print(reason)
    reason = 'property searched count: '+ str(searchedCount)
    print(reason)
    

        # except:
        #     print("Something went wrong in sl no ", row[0])

def get_propertyaddress(doorNo, buildingName,locality,cityname):
    return doorNo + ' ' + buildingName + ' ' +locality + ' ' + cityname

def process_location(value):
    location_MAP = {
        "Inside Civil Area (Bazar Area)": "CIVIL",
        "Outside Civil Area (Bungalow Area)": "BUNGLOW",
        "Outside Cantonment Area": "OUTSIDE",
        "None": "CIVIL"
    }
    return location_MAP[value]

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

def process_private_institution_type(value):
    private_institution_MAP = {
        "None": "OTHERSPRIVATEINSTITUITION",
        "Private company": "PRIVATECOMPANY",
        "NGO": "NGO",
        "Private Trust": "PRIVATETRUST",
        "Private Board": "PRIVATEBOARD",
        "Other Private Institution": "OTHERSPRIVATEINSTITUITION"        
    }
    return private_institution_MAP[value]

def process_govt_institution_type(value):
    govt_institution_MAP = {
        "None": "OTHERGOVERNMENTINSTITUITION",
        "CB Government": "ULBGOVERNMENT",
        "state Government": "INSTITUTIONALGOVERNMENT",
        "Central Government": "CENTRALGOVERNMENT",
        "Other Government Institution": "OTHERGOVERNMENTINSTITUITION"
    }
    return govt_institution_MAP[value]

def process_property_type(value):
    PT_MAP = {
        "None": "BUILTUP.SHAREDPROPERTY",
        "Vacant Land": "VACANT",
        "Flat/Part of the building": "BUILTUP.SHAREDPROPERTY",
        "Independent Building": "BUILTUP.INDEPENDENTPROPERTY"
    }
    return PT_MAP[value]

def process_occupancy_type(value):
    OC_MAP = {
        "None": "SELFOCCUPIED",
        "Self-Occupied": "SELFOCCUPIED",
        "Rented": "RENTED",
        "Unoccupied": "UNOCCUPIED"
    }
    return OC_MAP[value]

def process_usage_type(value):
    USAGE_MAP = {
        "Residential": "RESIDENTIAL",
        "Nonresidential ( Nonresidential )": "NONRESIDENTIAL.NONRESIDENTIAL",
        "Commercial ( Nonresidential )": "NONRESIDENTIAL.COMMERCIAL",
        "Industrial ( Nonresidential )": "NONRESIDENTIAL.INDUSTRIAL",
        "Institutional ( Nonresidential )": "NONRESIDENTIAL.INSTITUTIONAL",
        "Others ( Nonresidential )": "NONRESIDENTIAL.OTHERS",
        "Mixed": "MIXED",
        "Slum": "SLUM",
        "None": "RESIDENTIAL"
    }
    return USAGE_MAP[value]

def process_sub_usage_type(value):  
    SUB_USAGE_MAP = {
        'None':'' ,'Animal Dairy(Below 10 Cattle)':'NONRESIDENTIAL.COMMERCIAL.ANIMALDAIRYLESS' , 'Animal Dairy(Above 10 Cattle)':'NONRESIDENTIAL.COMMERCIAL.ANIMALDAIRYMORE' , 'Bank':'NONRESIDENTIAL.COMMERCIAL.BANK' , 'Dhobi':'NONRESIDENTIAL.COMMERCIAL.DHOBI' , 'Dyers':'NONRESIDENTIAL.COMMERCIAL.DYERS' , 'Movie Theatre':'NONRESIDENTIAL.COMMERCIAL.ENTERTAINMENT.MOVIETHEATRE' , 'Multiplex':'NONRESIDENTIAL.COMMERCIAL.ENTERTAINMENT.MULTIPLEX' , 'Marriage Palace':'NONRESIDENTIAL.COMMERCIAL.EVENTSPACE.MARRIAGEPALACE' , 'Ac Restaurant':'NONRESIDENTIAL.COMMERCIAL.FOODJOINTS.ACRESTAURANT' , 'Non Ac Restaurant':'NONRESIDENTIAL.COMMERCIAL.FOODJOINTS.NONACRESTAURANT' , 'Bhojanalaya/Tea Shop/Halwai Shop':'NONRESIDENTIAL.COMMERCIAL.FOODJOINTS.TEA' , 'Hotels':'NONRESIDENTIAL.COMMERCIAL.HOTELS' , 'Pathlab':'NONRESIDENTIAL.COMMERCIAL.MEDICALFACILITY.PATHLAB' , 'Private Dispensary':'NONRESIDENTIAL.COMMERCIAL.MEDICALFACILITY.PVTDISPENSARY' , 'Private Hospital':'NONRESIDENTIAL.COMMERCIAL.MEDICALFACILITY.PVTHOSPITAL' , 'Office Space(Less Than 10 Persons)':'NONRESIDENTIAL.COMMERCIAL.OFFICESPACELESS' , 'Office Space(More Than 10 Persons)':'NONRESIDENTIAL.COMMERCIAL.OFFICESPACEMORE' , 'Other Commercial Usage':'NONRESIDENTIAL.COMMERCIAL.OTHERCOMMERCIALSUBMINOR.OTHERCOMMERCIAL' , 'Petrol Pump':'NONRESIDENTIAL.COMMERCIAL.PETROLPUMP' , 'Grocery Store':'NONRESIDENTIAL.COMMERCIAL.RETAIL.GROCERY' , 'Malls':'NONRESIDENTIAL.COMMERCIAL.RETAIL.MALLS' , 'Pharmacy':'NONRESIDENTIAL.COMMERCIAL.RETAIL.PHARMACY' , 'Showroom':'NONRESIDENTIAL.COMMERCIAL.RETAIL.SHOWROOM' , 'Service Centre':'NONRESIDENTIAL.COMMERCIAL.SERVICECENTER' , 'Statutory Organisation':'NONRESIDENTIAL.COMMERCIAL.STATUTORY.STATUTORYORGANISATION' , 'Manufacturing Facility(Less Than 10 Persons)':'NONRESIDENTIAL.INDUSTRIAL.MANUFACTURINGFACILITY.MANUFACTURINGFACILITYLESS' , 'Manufacturing Facility(More Than 10 Persons)':'NONRESIDENTIAL.INDUSTRIAL.MANUFACTURINGFACILITY.MANUFACTURINGFACILITYMORE' , 'Other Industrial Usage':'NONRESIDENTIAL.INDUSTRIAL.OTHERINDUSTRIALSUBMINOR.OTHERINDUSTRIAL' , 'Godown/Warehouse':'NONRESIDENTIAL.INDUSTRIAL.WAREHOUSE.WAREHOUSE' , 'College':'NONRESIDENTIAL.INSTITUTIONAL.EDUCATIONAL.COLLEGES' , 'Other Private Educational Institute':'NONRESIDENTIAL.INSTITUTIONAL.EDUCATIONAL.OTHEREDUCATIONAL' , 'Polytechnic':'NONRESIDENTIAL.INSTITUTIONAL.EDUCATIONAL.POLYTECHNICS' , 'School':'NONRESIDENTIAL.INSTITUTIONAL.EDUCATIONAL.SCHOOL' , 'Training Institute':'NONRESIDENTIAL.INSTITUTIONAL.EDUCATIONAL.TRAININGINSTITUTES' , 'Govt. Aided Educational Institute':'NONRESIDENTIAL.INSTITUTIONAL.EDUCATIONALGOVAIDED.GOVAIDEDEDUCATIONAL' , 'Historical Building':'NONRESIDENTIAL.INSTITUTIONAL.HISTORICAL.HISTORICAL' , 'Stray Animal Care Center':'NONRESIDENTIAL.INSTITUTIONAL.HOMESFORSPECIALCARE.ANIMALCARE' , 'Home For The Disabled / Destitute':'NONRESIDENTIAL.INSTITUTIONAL.HOMESFORSPECIALCARE.DISABLEDHOME' , 'Old Age Homes':'NONRESIDENTIAL.INSTITUTIONAL.HOMESFORSPECIALCARE.OLDAGEHOMES' , 'Orphanage':'NONRESIDENTIAL.INSTITUTIONAL.HOMESFORSPECIALCARE.ORPHANAGE' , 'Others':'NONRESIDENTIAL.INSTITUTIONAL.OTHERINSTITUTIONALSUBMINOR.OTHERINSTITUTIONAL' , 'Community Hall':'NONRESIDENTIAL.INSTITUTIONAL.PUBLICFACILITY.COMMUNITYHALL' , 'Govt. Hospital & Dispensary':'NONRESIDENTIAL.INSTITUTIONAL.PUBLICFACILITY.GOVTHOSPITAL' , 'Public Libraries':'NONRESIDENTIAL.INSTITUTIONAL.PUBLICFACILITY.LIBRARIES' , 'Golf Club':'NONRESIDENTIAL.INSTITUTIONAL.RECREATIONAL.GOLFCLUB' , 'Social Club':'NONRESIDENTIAL.INSTITUTIONAL.RECREATIONAL.SOCIALCLUB' , 'Sports Stadium':'NONRESIDENTIAL.INSTITUTIONAL.RECREATIONAL.SPORTSSTADIUM' , 'Religious':'NONRESIDENTIAL.INSTITUTIONAL.RELIGIOUSINSTITUITION.RELIGIOUS' , 'Cremation/ Burial Ground':'NONRESIDENTIAL.OTHERS.PUBLICFACILITY.CREMATIONBURIAL'
    }
    return SUB_USAGE_MAP[value]

def process_ownership_type(value):
    Ownsership_MAP = {
        "None": "INDIVIDUAL.SINGLEOWNER",
        "Single Owner": "INDIVIDUAL.SINGLEOWNER",
        "Multiple Owners": "INDIVIDUAL.MULTIPLEOWNERS",
        "Institutional- Private": "INSTITUTIONALPRIVATE",
        "Institutional- Government": "INSTITUTIONALGOVERNMENT"
    }
    return Ownsership_MAP[value]

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

