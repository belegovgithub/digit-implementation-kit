from common import *
from config import config
import io
import os
import numpy
def main():
    print("TENANTINFO_JSON",config.TENANTINFO_JSON)
    with io.open(config.TENANTINFO_JSON, encoding="utf-8") as f:
        tenants_data = json.load(f)
    #print("tennt data",tenants_data)
    found = False
    for found_index, tenant in enumerate(tenants_data["tenantInfo"]):
        if tenant["code"] == config.TENANT_ID:
            found = True
            break

    #dfs = open_excel_file(os.path.join(config.BOUNDARIES_FOLDER,config.TENANT_DETAIL_EXCEL_NAME))
    dfs = open_excel_file(config.TENANT_WORKBOOK)

    tenant = get_sheet(dfs, config.SHEET_TENANT_DETAILS)
    
    INDEX_TENANT_ULB_NAME = 0
    INDEX_TENANT_WEBSITE = 11
    INDEX_TENANT_CITYCODE = 3
    INDEX_TENANT_LOCALNAME = 2
    INDEX_TENANT_DISTRICTNAME = 5
    INDEX_TENANT_DISTRICTCODE = 6
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
    INDEX_TENANT_MALE_POPULATION = 21
    INDEX_TENANT_FEMALE_POPULATION = 22
    INDEX_TENANT_LITERACY_RATE = 24
    INDEX_TENANT_LANGUAG_SPOKEN_1 = 25
    INDEX_TENANT_LANGUAG_SPOKEN_2 = 26
    INDEX_TENANT_LANGUAG_SPOKEN_3 = 27


    COL_INDEX=2
    # ° N
    # ° E

    ulbName = fix_value(tenant.iloc[INDEX_TENANT_ULB_NAME][COL_INDEX])
    website = fix_value(tenant.iloc[INDEX_TENANT_WEBSITE][COL_INDEX])
    citycode = fix_value(tenant.iloc[INDEX_TENANT_CITYCODE][COL_INDEX])
    local_name = fix_value(tenant.iloc[INDEX_TENANT_LOCALNAME][COL_INDEX])
    district_name = fix_value(tenant.iloc[INDEX_TENANT_DISTRICTNAME][COL_INDEX])
    district_code = fix_value(tenant.iloc[INDEX_TENANT_DISTRICTCODE][COL_INDEX])
    region_name = fix_value(tenant.iloc[INDEX_TENANT_REGIONNAME][COL_INDEX])
    region_code = fix_value(tenant.iloc[INDEX_TENANT_REGIONCODE][COL_INDEX])
    grade = fix_value(INDEX_TENANT_GRADE)
    lat = float(fix_value(tenant.iloc[INDEX_TENANT_LATITUDE][COL_INDEX]))
    long = float(fix_value(tenant.iloc[INDEX_TENANT_LONGITUDE][COL_INDEX]))
    contact = fix_value(tenant.iloc[INDEX_TENANT_CONTACT][COL_INDEX])
    email = fix_value(tenant.iloc[INDEX_TENANT_EMAIL][COL_INDEX])
    address = fix_value(tenant.iloc[INDEX_TENANT_ADDRESS][COL_INDEX])
    fb = fix_value(tenant.iloc[INDEX_TENANT_FB][COL_INDEX])
    twitter = fix_value(tenant.iloc[INDEX_TENANT_TWITTER][COL_INDEX])
    logoIdPdf=config.CITY_NAME.lower()+".png"
    regionCode=fix_value(tenant.iloc[INDEX_TENANT_TWITTER][COL_INDEX])
    municipalityName=fix_value(tenant.iloc[INDEX_TENANT_TWITTER][COL_INDEX])
    population=fix_value(tenant.iloc[INDEX_TENANT_POPULATION][COL_INDEX])
    malePopulation = fix_value(tenant.iloc[INDEX_TENANT_MALE_POPULATION][COL_INDEX])
    femalePopulation = fix_value(tenant.iloc[INDEX_TENANT_FEMALE_POPULATION][COL_INDEX])
    literacyRate = fix_value(tenant.iloc[INDEX_TENANT_LITERACY_RATE][COL_INDEX])
    languageSpoken1 = fix_value(tenant.iloc[INDEX_TENANT_LANGUAG_SPOKEN_1][COL_INDEX])
    languageSpoken2 = fix_value(tenant.iloc[INDEX_TENANT_LANGUAG_SPOKEN_2][COL_INDEX])
    languageSpoken3 = fix_value(tenant.iloc[INDEX_TENANT_LANGUAG_SPOKEN_3][COL_INDEX])
    thisdict = {
        "hindi": "HN",
        "english": "EN",
        "marathi": "MA",
        "telugu": "TE",
        "kumauni": "KU",
        "bengali": "BE",
        "tamil": "TA",
        "gujarati": "GU",
        "urdu": "UR",
        "kannada": "KA",
        "odia": "OD",
        "malayalam": "ML",
        "punjabi": "PU"
    }
    languageArr =[]
    if str(languageSpoken1).lower() in thisdict : 
        languageArr.append(thisdict[languageSpoken1.lower()])
    if str(languageSpoken2).lower() in thisdict : 
        languageArr.append(thisdict[languageSpoken2.lower()])
    if str(languageSpoken3).lower() in thisdict : 
        languageArr.append(thisdict[languageSpoken3.lower()])
    tenantInfo_object = {        
      "code": config.TENANT_ID,
      "districtCode": config.CITY_NAME,
      "population": population,
      "malePopulation": malePopulation,
      "femalePopultion": femalePopulation,
      "languagesSpoken": languageArr    
    }
    import sys

    json.dump(tenantInfo_object, sys.stdout, indent=2)

    if config.ASSUME_YES:
        response = os.getenv("ASSUME_YES", None) or input("\nDo you want to append the data in repo (y/[n])? ")
    else:
        response = "y"

    if response.lower() == "y":
        with io.open(config.TENANTINFO_JSON, mode="w", encoding="utf-8") as f:
            if found:
                print("Tenant Info - " + config.TENANT_ID + " already exists, overwriting")
                assert tenants_data["tenantInfo"][found_index][
                           "code"] == config.TENANT_ID, "Updating for correct tenant id"
                tenants_data["tenantInfo"][found_index] = tenantInfo_object
            else:
                print("Tenant Info - " + config.TENANT_ID + " doesn't exists, adding details")
                tenants_data["tenantInfo"].append(tenantInfo_object)
            json.dump(tenants_data, f, indent=2,  ensure_ascii=False)

        print("Added the tenant Info to MDMS data")
    else:
        print("Not adding the tenant Info to MDMS data")


if __name__ == "__main__":
    main()
