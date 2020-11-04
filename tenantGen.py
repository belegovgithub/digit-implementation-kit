from common import *
from config import config
import io
import os
import numpy
from processing.generate_localization_data import process_CB_localization
from processing.generate_localization_data import process_CB_localization_Hindi
def main():
    print("TENANT_JSON",config.TENANT_JSON)
    with io.open(config.TENANT_JSON, encoding="utf-8") as f:
        tenants_data = json.load(f)
    #print("tenant data",tenants_data)
    found = False
    for found_index, tenant in enumerate(tenants_data["tenants"]):
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
    INDEX_STATE = 30
    INDEX_CITY_HINDI = 31
    INDEX_DISTRICT_HINDI = 32
    INDEX_STATE_HINDI = 33

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
    state = fix_value(tenant.iloc[INDEX_STATE][COL_INDEX])
    city_hindi = fix_value(tenant.iloc[INDEX_CITY_HINDI][COL_INDEX])
    district_hindi = fix_value(tenant.iloc[INDEX_DISTRICT_HINDI][COL_INDEX])
    state_hindi = fix_value(tenant.iloc[INDEX_STATE_HINDI][COL_INDEX])
    tenant_object = {
        "code": config.TENANT_ID,
        "name": ulbName,
        "description": config.CITY_NAME,
        "logoId": "https://raw.githubusercontent.com/belegovgithub/webaccess/master/images/{}logo.png".format(config.CITY_NAME.lower()),
        "logoIdPdf": logoIdPdf ,
        "imageId": None,
        "domainUrl": website,
        "type": "CITY",
        "twitterUrl": twitter,
        "facebookUrl": fb,
        "emailId": email,
        "OfficeTimings": {
            "Mon - Fri": "9.00 AM - 5.00 PM"
        },
        "city": {
            "name": config.CITY_NAME,
            "localName": local_name,
            "districtCode": str(int(float(district_code))) if district_code else None,
            "districtName": district_name,
            "regionName": region_name,
            "ulbGrade": grade,
            "longitude": long,
            "latitude": lat,
            "shapeFileLocation": None,
            "captcha": None,
            "code": citycode,
            "regionCode": region_code,
            "municipalityName": ulbName,
            "population": population
        },
        "address": str(address),
        "contactNumber": str(contact)
    }
    import sys

    json.dump(tenant_object, sys.stdout, indent=2)
    if config.ASSUME_YES:
        response = os.getenv("ASSUME_YES", None) or input("\nDo you want to append the data in repo (y/[n])? ")
    else:
        response = "y"
        
    if response.lower() == "y":
        with io.open(config.TENANT_JSON, mode="w", encoding="utf-8") as f:
            if found:
                print("Tenant - " + config.TENANT_ID + " already exists, overwriting")
                assert tenants_data["tenants"][found_index][
                           "code"] == config.TENANT_ID, "Updating for correct tenant id"
                tenants_data["tenants"][found_index] = tenant_object
            else:
                print("Tenant - " + config.TENANT_ID + " doesn't exists, adding details")
                tenants_data["tenants"].append(tenant_object)
            json.dump(tenants_data, f, indent=2,  ensure_ascii=False)

        print("Added the tenant to MDMS data")
    else:
        print("Not adding the tenant to MDMS data")
    process_CB_localization(config.CITY_NAME.upper(),district_name,district_code,state)
    process_CB_localization_Hindi(config.CITY_NAME.upper(),district_code, city_hindi, district_hindi, state_hindi)

if __name__ == "__main__":
    main()
