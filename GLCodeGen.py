from common import *
from config import config
import io
import os
import numpy
def main():
    print("MCOLLECT_JSON",config.MCOLLECT_JSON)
    with io.open(config.MCOLLECT_JSON, encoding="utf-8") as f:
        tenants_data = json.load(f)
    print("tenant data",tenants_data)
    found = False
    for found_index, tenant in enumerate(tenants_data["Help"]):
        if tenant["tenant"] == config.TENANT_ID:
            found = True
            break

    dfs = open_excel_file(config.MCOLLECT_WORKBOOK)
    glcodes = get_sheet(dfs, config.SHEET_MCOLLECT)
    glcodes = glcodes.astype(str)
    offset = 1

    INDEX_TENANT_ULB_NAME = 0
    INDEX_GLCODE = 1
    INDEX_CB_CODE = 2
    INDEX_DEPT_CODE = 3 
    INDEX_FUND = 4
    INDEX_GLCODE = get_column_index(glcodes, config.COLUMN_GL_CODE) or 4
    INDEX_CB_CODE = get_column_index(glcodes, config.COLUMN_CB_NAME) or 5
    INDEX_DEPT_CODE = get_column_index(glcodes, config.COLUMN_DEPT_CODE) or 6
    INDEX_FUND = get_column_index(glcodes, config.COLUMN_FUND_NAME) or 7

    glcodes_data = glcodes.apply(lambda row: {"code": row[INDEX_GLCODE].strip(),
                                        "glcode": row[INDEX_GLCODE].strip(),
                                        "dept": row[INDEX_DEPT_CODE].strip(),
                                        "fund": row[INDEX_FUND].strip()}
                            , axis=1)

    final_data = {
        "tenantId": config.TENANT_ID,
        "moduleName": "mCollect",
        "BillingService": [
            glcodes_data
        ]
    }

    import sys

    json.dump(final_data, sys.stdout, indent=2)

    if config.ASSUME_YES:
        response = os.getenv("ASSUME_YES", None) or input("\nDo you want to append the data in repo (y/[n])? ")
    else:
        response = "y"

    if response.lower() == "y":
        mCollect_path = config.MDMS_LOCATION / config.CITY_NAME.lower() / "mCollect"
        os.makedirs(mCollect_path, exist_ok=True)       

        with open(os.path.join(mCollect_path , "GLCode.json"), "w") as f:
            json.dump(final_data, f, indent=2)


if __name__ == "__main__":
    main()
