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

    data = {
        "RequestInfo": {
            "authToken": "{{access_token}}"
        },        
        "banks": bank_data
    }
    print(data)