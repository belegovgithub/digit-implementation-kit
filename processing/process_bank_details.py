import json
import io
import os
from pathlib import Path
from config import config
from common import *


COL_INDEX = 2


def bank(dfs):
    bank = search_bank()
    if(len(bank['banks']) == 1):
        print("Bank exist.")
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
        # auth_token = superuser_login()["access_token"]
        auth_token="8a3286ad-611a-486c-91d5-cdd448931547"
        data = {
            "RequestInfo": {
                "authToken": auth_token
            },        
            "banks": bank_data
        }
        #print("Bank Data",data)
        response = create_bank(data)
        print("bank created in DB.")
        return response['banks'][0]

def bankbranch(bank,dfs):
    bankbranch  = search_bankbranch()  
    if(len(bankbranch['bankBranches']) == 1):
        print("Bank Branch exist.")
        return bankbranch['bankBranches'][0]
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
        
        # auth_token = superuser_login()["access_token"]
        auth_token="8a3286ad-611a-486c-91d5-cdd448931547"
        data = {
            "RequestInfo": {
                "authToken": auth_token
            },        
            "bankBranches": bankbranch_data
        }
        response = create_bankbranch(data)
        print("bank branch created in DB.",response)
        return response['bankBranches'][0]


def accountcodepurpose(dfs):
    accountcodepurpose = search_accountcodepurpose()
    if(len(accountcodepurpose['accountCodePurposes']) >= 1):
        print("account code Purpose exist")
        return accountcodepurpose['accountCodePurposes'][0]
    else:        
        accountcodepurpose = get_sheet(dfs, config.SHEET_ACCOUNT_CODE_PURPOSE)
        accountcodepurpose = accountcodepurpose.astype(str)
        INDEX_PURPOSE = 0
        purpose = fix_value(accountcodepurpose.iloc[INDEX_PURPOSE][COL_INDEX])
        accountcodepurpose_data = []

        accountcodepurpose_data.append({
                            "name": purpose,
                            "tenantId": config.TENANT_ID
                        })
        # auth_token = superuser_login()["access_token"]
        auth_token="8a3286ad-611a-486c-91d5-cdd448931547"
        data = {
            "RequestInfo": {
                "authToken": auth_token
            },        
            "accountCodePurposes": accountcodepurpose_data
        }
        response = create_accountcodepurpose(data)
        print("account code purpose created in DB.")
        return response['accountCodePurposes'][0]

def chartaccount(accountcodepurpose,dfs):
    chartaccount = search_chartaccount()
    if(len(chartaccount['chartOfAccounts']) >= 1):
        print("Chart of Account exist")
        return chartaccount['chartOfAccounts'][0]
    else:
        chartaccount = get_sheet(dfs, config.SHEET_CHART_ACCOUNT)
        chartaccount = chartaccount.astype(str)
        INDEX_GLCODE = 0
        INDEX_NAME = 1
        glcode = fix_value(chartaccount.iloc[INDEX_GLCODE][COL_INDEX])
        name = fix_value(chartaccount.iloc[INDEX_NAME][COL_INDEX])
        chartaccount_data = []
        chartaccount_data.append({
                                "glcode": glcode,
                                "name": name,                            
                                "tenantId": config.TENANT_ID,
                                "type": "A",
                                "classification": 1,
                                "functionRequired": False,
                                "budgetCheckRequired": False,
                                "isActiveForPosting": True,
                                "accountCodePurpose": accountcodepurpose
                            })
        # auth_token = superuser_login()["access_token"]
        auth_token="8a3286ad-611a-486c-91d5-cdd448931547"
        data = {
            "RequestInfo": {
                "authToken": auth_token
            },        
            "chartOfAccounts": chartaccount_data
        }
        #print(data)
        response = create_chartaccount(data)
        print("chart of account created in DB.",response)
        return response['chartOfAccounts'][0]


def fund(dfs):      
    fund = search_fund()
    if(len(fund['funds']) >= 1):
        print("Fund exist")
        return fund['funds'][0]
    else:        
        fund = get_sheet(dfs, config.SHEET_FUND)
        fund = fund.astype(str)
        INDEX_FUND_NAME = 0
        NDEX_FUND_CODE = 1
        NDEX_FUND_IDENTIFIER = 2
        NDEX_FUND_LEVEL = 3
        name = fix_value(fund.iloc[INDEX_FUND_NAME][COL_INDEX])
        code = fix_value(fund.iloc[NDEX_FUND_CODE][COL_INDEX])
        identifier = fix_value(fund.iloc[NDEX_FUND_IDENTIFIER][COL_INDEX])
        level = fix_value(fund.iloc[NDEX_FUND_LEVEL][COL_INDEX])
        fund_data = []

        fund_data.append({
                            "name" :name,
                            "code" : code.zfill(2), 
                            "identifier" : identifier,
                            "level" : level,
                            "active" : True,
                            "tenantId": config.TENANT_ID
                        })
        # auth_token = superuser_login()["access_token"]
        auth_token="8a3286ad-611a-486c-91d5-cdd448931547"
        data = {
            "RequestInfo": {
                "authToken": auth_token
            },        
            "funds": fund_data
        }
        #print(data)
        response = create_fund(data)
        print("fund created in DB.")
        return response['funds'][0]

def bankaccount(bankbranch, chartaccount, fund,dfs):
    bankaccount = search_bankaccount()
    if(len(bankaccount['bankAccounts']) >= 1):
        print("Bank Account exist")
        return bankaccount['bankAccounts'][0]
    else:    
        bankaccount = get_sheet(dfs, config.SHEET_BANK_ACCOUNT)
        bankaccount = bankaccount.astype(str)
        INDEX_ACCOUNT_NO = 2
        INDEX_ACCOUNT_TYPE = 4
        INDEX_DESC = 6

        acc = fix_value(bankaccount.iloc[INDEX_ACCOUNT_NO][COL_INDEX])
        accType = fix_value(bankaccount.iloc[INDEX_ACCOUNT_TYPE][COL_INDEX])
        desc = fix_value(bankaccount.iloc[INDEX_DESC][COL_INDEX])
        bankaccount_data = []
        bankaccount_data.append({
                                    "accountNumber": acc,
                                    "accountType": accType,
                                    "active": True,
                                    "description": desc,
                                    "type": "RECEIPTS_PAYMENTS",
                                    "tenantId": config.TENANT_ID,
                                    "bankBranch": bankbranch,
                                    "chartOfAccount": chartaccount,
                                    "fund": fund

                                })
        # auth_token = superuser_login()["access_token"]
        auth_token="8a3286ad-611a-486c-91d5-cdd448931547"
        data = {
            "RequestInfo": {
                "authToken": auth_token
            },        
            "bankAccounts": bankaccount_data
        }
        response = create_bankaccount(data)
        print("bank account created in DB.")
        return response['bankAccounts'][0]


# if __name__ == "__main__":
#     main()

# def main():
#     bank()