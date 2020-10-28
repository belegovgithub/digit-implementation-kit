import json
import io
import os
from pathlib import Path
from config import config
from common import *

dfs = open_excel_file(config.BANK_WORKBOOK)
COL_INDEX = 2


def bank():
    bank = search_bank()
    if(len(bank['banks']) == 1):
        return bank['banks'][0]
    else:
        bank = get_sheet(dfs, config.SHEET_BANK_BRANCH)
        bank = bank.astype(str)
        INDEX_BANK_NAME = 10
        INDEX_BANK_CODE = 11
        bank_name = fix_value(bank.iloc[INDEX_BANK_NAME][COL_INDEX])
        bank_code = fix_value(bank.iloc[INDEX_BANK_CODE][COL_INDEX])

        bank_data = []
        bank_data.append({
                            "code": bank_code.strip(),
                            "name": bank_name.strip(),
                            "active": True,
                            "type": "I",
                            "tenantId": config.TENANT_ID
                        })
        auth_token = superuser_login()["access_token"]
        data = {
            "RequestInfo": {
                "authToken": auth_token
            },        
            "banks": bank_data
        }
        response = create_bank(data)
        print(response)
        print("bank created in DB.")
        return response['banks'][0]

def bankbranch(bank): 
    bankbranch  = search_bankbranch()  
    if(len(bankbranch['bankbranches']) == 1):
        return bankbranch['bankbranches'][0]
    else:
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
        INDEX_STATE = 12  

        cbName = fix_value(bankbranch.iloc[INDEX_CBNAME][COL_INDEX])
        branch_name = fix_value(bankbranch.iloc[INDEX_BANK_BRANCH][COL_INDEX])
        branch_code = fix_value(bankbranch.iloc[INDEX_BRANCH_CODE][COL_INDEX])
        branch_address = fix_value(bankbranch.iloc[INDEX_BRANCH_ADDRESS][COL_INDEX])
        pincode = fix_value(bankbranch.iloc[INDEX_PIN][COL_INDEX])
        contact_person = fix_value(bankbranch.iloc[INDEX_CONTACT_PERSON][COL_INDEX])
        person_desig = fix_value(bankbranch.iloc[INDEX_PERSON_DESIGNATION][COL_INDEX])
        phone_number = fix_value(bankbranch.iloc[INDEX_PHONE_NUMBER][COL_INDEX])
        micr = fix_value(bankbranch.iloc[INDEX_MICR][COL_INDEX])
        fax = fix_value(bankbranch.iloc[INDEX_FAX][COL_INDEX])
        state = fix_value(bankbranch.iloc[INDEX_STATE][COL_INDEX])

        bankbranch_data = []

        bankbranch_data.append({
                            "bank": bank,
                            "code": branch_code,
                            "name": branch_name,
                            "address": branch_address,
                            "address2": "",
                            "city": config.CITY_NAME,
                            "state": state,
                            "pincode": pincode,
                            "phone": phone_number,
                            "fax": fax,
                            "contactPerson": contact_person,
                            "active": True,
                            "description": "",
                            "micr": micr,
                            "tenantId": config.TENANT_ID,
                        })
        
        auth_token = superuser_login()["access_token"]
        data = {
            "RequestInfo": {
                "authToken": auth_token
            },        
            "bankbranches": bankbranch_data
        }
        response = create_bank(data)
        print("bank branch created in DB.")
        return response['banks'][0]


def accountcodepurpose():   
    accountcodepurpose = search_accountcodepurpose()
    if(len(accountcodepurpose['accountCodePurposes']) >= 1):
        return accountcodepurpose['accountCodePurposes'][0]
    else:        
        accountcodepurpose = get_sheet(dfs, config.SHEET_ACCOUNT_CODE_PURPOSE)
        accountcodepurpose = accountcodepurpose.astype(str)
        INDEX_PURPOSE = 0
        purpose = fix_value(bankbranch.iloc[INDEX_PURPOSE][COL_INDEX])
        accountcodepurpose_data = []

        accountcodepurpose_data.append({
                            "name": purpose,
                            "tenantId": config.TENANT_ID
                        })
        auth_token = superuser_login()["access_token"]
        data = {
            "RequestInfo": {
                "authToken": auth_token
            },        
            "accountCodePurposes": accountcodepurpose_data
        }
        response = create_accountcodepurpose(data)
        print("account code purpose created in DB.")
        return response['accountCodePurposes'][0]

def chartaccount(accountcodepurpose):   
    chartaccount = get_sheet(dfs, config.SHEET_CHART_ACCOUNT)
    chartaccount = chartaccount.astype(str)

def fund():       
    fund = search_fund()
    if(len(fund['funds']) >= 1):
        return fund['funds'][0]
    else:        
        fund = get_sheet(dfs, config.SHEET_FUND)
        fund = fund.astype(str)
        INDEX_FUND_NAME = 0
        NDEX_FUND_CODE = 0
        NDEX_FUND_IDENTIFIER = 0
        NDEX_FUND_LEVEL = 0
        name = fix_value(bankbranch.iloc[INDEX_FUND_NAME][COL_INDEX])
        code = fix_value(bankbranch.iloc[NDEX_FUND_CODE][COL_INDEX])
        identifier = fix_value(bankbranch.iloc[NDEX_FUND_IDENTIFIER][COL_INDEX])
        level = fix_value(bankbranch.iloc[NDEX_FUND_LEVEL][COL_INDEX])
        fund_data = []

        fund_data.append({
                            "name" :name,
                            "code" : code, 
                            "identifier" : identifier,
                            "level" : level,
                            "active" : True,
                            "tenantId": config.TENANT_ID
                        })
        auth_token = superuser_login()["access_token"]
        data = {
            "RequestInfo": {
                "authToken": auth_token
            },        
            "funds": fund_data
        }
        response = create_fund(data)
        print("fund created in DB.")
        return response['funds'][0]

def bankaccount():   
    bankaccount = get_sheet(dfs, config.SHEET_BANK_ACCOUNT)
    bankaccount = bankaccount.astype(str)



# if __name__ == "__main__":
#     main()

# def main():
#     bank()