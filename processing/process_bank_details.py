import json
import io
import os
from pathlib import Path
from config import config
from common import *

dfs = open_excel_file(config.BANK_WORKBOOK)
COL_INDEX = 2


def bank():
    bank  = get_sheet(dfs, config.SHEET_BANK_BRANCH)
    bank = bank.astype(str)
    INDEX_BANK_NAME = 10
    INDEX_BANK_CODE = 11
    bank_name = fix_value(bankbranch.iloc[INDEX_BANK_NAME][COL_INDEX])
    bank_code = fix_value(bankbranch.iloc[INDEX_BANK_CODE][COL_INDEX])

    bank_data = []
    bank_data.append({
                        "code": bank_code.strip(),
                        "name": bank_name.strip(),
                        "active": True,
                        "type": "I",
                        "tenantId": config.TENANT_ID
                    })

    data = {
        "RequestInfo": {
            "authToken": "{{access_token}}"
        },        
        "banks": bank_data
    }

    auth_token = superuser_login()["access_token"]
    response = upsert_localization(auth_token, data)
    print(response)
    #print("bank created in DB.")

def bankbranch():   
    bankbranch = get_sheet(dfs, config.SHEET_BANK_BRANCH)
    bankbranch = bankbranch.astype(str)

    INDEX_CBNAME = 0
    INDEX_BANK_BRANCH = 1
    INDEX_BRANCH_CODE = 2
    INDEX_BRANCH_ADDRESS = 3
    INDEX_PIN = 4
    INDEX_CONTACT_PERSON = 5
    INDEX_PERSON_DESIGNATION = 6
    INDEX_PHONE_NUMBER = 7
    INDEX_MICR = 8
    INDEX_FAX = 9    

    cbName = fix_value(bankbranch.iloc[INDEX_CBNAME][COL_INDEX])
    branch_name = fix_value(bankbranch.iloc[INDEX_BANK_BRANCH][COL_INDEX])
    branch_code = fix_value(bankbranch.iloc[INDEX_BRANCH_CODE][COL_INDEX])
    branch_address = fix_value(bankbranch.iloc[INDEX_BRANCH_ADDRESS][COL_INDEX])
    pincode = fix_value(bankbranch.iloc[INDEX_PIN][COL_INDEX])
    contact_person = fix_value(bankbranch.iloc[INDEX_CONTACT_PERSON][COL_INDEX])
    person_desig = fix_value(bankbranch.iloc[INDEX_PERSON_DESIGNATION][COL_INDEX])
    phone_number = fix_value(bankbranch.iloc[INDEX_PHONE_NUMBER][COL_INDEX])


    # "bankBranches": [
    #     {
    #         "id": "2",
    #         "bank": {
    #             "id": "10",
    #             "code": "AXIS",
    #             "name": "AXIS Bank",
    #             "description": "",
    #             "active": true,
    #             "type": "I",
    #             "tenantId": "pb.agra",
    #             "createdBy": null,
    #             "lastModifiedBy": null,
    #             "createdDate": "2020-07-04T14:55:48.338+0530",
    #             "lastModifiedDate": null,
    #             "deleteReason": null
    #          },
    #         "code": "AXIS0001907",
    #         "name": "East_Street_Branch",
    #         "address": "AXIS Bank, KP Housing Society, Gen.",
    #         "address2": "Thimaya Road, East Street, Camp",
    #         "city": "Agra",
    #         "state": "Uttar Pradesh",
    #         "pincode": "411001",
    #         "phone": "9313098841",
    #         "fax": null,
    #         "contactPerson": "Prachi Agarwal",
    #         "active": true,
    #         "description": null,
    #         "micr": "411240008",
    #         "tenantId": "pb.agra",
    #         "createdBy": null,
    #         "lastModifiedBy": null,
    #         "createdDate": "2020-06-09T20:23:55.313+0530",
    #         "lastModifiedDate": "2020-06-09T20:23:55.313+0530",
    #         "deleteReason": null
    #     }
    # ]


def bankaccount():   
    bankaccount = get_sheet(dfs, config.SHEET_BANK_ACCOUNT)
    bankaccount = bankaccount.astype(str)

def accountcodepurpose():   
    accountcodepurpose = get_sheet(dfs, config.SHEET_ACCOUNT_CODE_PURPOSE)
    accountcodepurpose = accountcodepurpose.astype(str)

def chartaccount():   
    chartaccount = get_sheet(dfs, config.SHEET_CHART_ACCOUNT)
    chartaccount = chartaccount.astype(str)

def fund():   
    fund = get_sheet(dfs, config.SHEET_FUND)
    fund = fund.astype(str)


def get_code(prefix, code):
    import re
    patt = re.compile(r"[-.\s'\"+]", re.I)
    return (patt.sub("_", prefix) + "_" + patt.sub("_", code)).upper()


def process_boundary_file(auth_token, boundary_path, generate_file=True, write_localization=True):
    locale_data = []

    with open(boundary_path, mode="r") as f:
        data = json.load(f)
        used_codes = set()
        for b in data["TenantBoundary"]:
            boundary_type = b["hierarchyType"]["code"]
            tenant_id = b["boundary"]["code"]

            locale_module = "rainmaker-" + tenant_id

            for l1 in b["boundary"]["children"]:
                code = get_code(tenant_id + "_" + boundary_type + "_ZONE", l1["code"])
                if code not in used_codes:
                    used_codes.add(code)
                    locale_data.append({
                        "code": code,
                        "message": l1["name"],
                        "module": locale_module,
                        "locale": "en_IN"
                    })

                for l2 in l1["children"]:
                    code = get_code(tenant_id + "_" + boundary_type + "_BLOCK", l2["code"])
                    if code not in used_codes:
                        used_codes.add(code)
                        locale_data.append({
                            "code": code,
                            "message": l2["name"],
                            "module": locale_module,
                            "locale": "en_IN"
                        })

                    for l3 in l2.get("children", []):
                        code = get_code(tenant_id + "_" + boundary_type, l3["code"])
                        if code not in used_codes:
                            used_codes.add(code)
                            locale_data.append({
                                "code": code,
                                "message": l3["name"],
                                "module": locale_module,
                                "locale": "en_IN"
                            })

            outputpath = Path(".") / "localization" / config.CONFIG_ENV / (
                    "boundary_" + boundary_type + "_" + tenant_id + ".json")

            data = {
                "RequestInfo": {
                    "authToken": "{{access_token}}"
                },
                "tenantId": tenant_id,
                "messages": locale_data
            }

            if generate_file:
                with io.open(outputpath, mode="w") as f:
                    # print(json.dumps(locale_data, indent=2))
                    json.dump(data
                              , indent=2, fp=f)
            #print(data)
            if write_localization:
                localize_response = upsert_localization(auth_token, data)
    print("Boundary localization for english is pushed.")
            #print(localize_response)


def process_boundary(auth_token):
    for folder in os.scandir(config.MDMS_LOCATION):
        boundary_path = Path(folder.path) / "egov-location" / "boundary-data.json"
        print(boundary_path)

        if os.path.isfile(boundary_path):
            process_boundary_file(auth_token, boundary_path)

def process_CB_localization(CBNAME, district, state):
    locale_data = []
    locale_module = "pb." + config.CITY_NAME.lower()
    locale_data.append({
                        "code": "TENANT_TENATS_PB_"+ CBNAME,
                        "message": config.CITY_NAME,
                        "module": locale_module,
                        "locale": "en_IN"
                    })
    locale_data.append({
                        "code": "PB_"+ CBNAME + "_" + CBNAME + "LABEL",
                        "message": district,
                        "module": locale_module,
                        "locale": "en_IN"
                    })
    locale_data.append({
                        "code": "MYCITY_"+ CBNAME + "_" + "STATE_LABEL",
                        "message": state,
                        "module": locale_module,
                        "locale": "en_IN"
                    })
    data = {
        "RequestInfo": {
            "authToken": "{{access_token}}"
        },
        "tenantId": config.TENANT_ID,
        "messages": locale_data
    }
    print(locale_data)
    auth_token = superuser_login()["access_token"]
    localize_response = upsert_localization(auth_token, data)
    print("Tenant localization for english is pushed.")
    
if __name__ == "__main__":
    main()

def main():
    bank()