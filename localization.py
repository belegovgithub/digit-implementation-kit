from common import *
from config import config
import io
import os
import numpy
 
def process_CB_localization(CBNAME, district, district_code, state):
    locale_data = []
    locale_module = "rainmaker-common"
    locale_data.append({
                        "code": "TENANT_TENANTS_PB_"+ CBNAME,
                        "message": config.CITY_NAME,
                        "module": locale_module,
                        "locale": "en_IN"
                    })
    locale_data.append({
                        "code": "PB_"+ CBNAME + "_" + district_code + "_LABEL",
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
        "tenantId": config.TENANT,
        "messages": locale_data
    }
    auth_token = superuser_login()["access_token"]
    localize_response = upsert_localization(auth_token, data)
    print(localize_response)
    print("Tenant localization for english is pushed.")
def main():
    filePath=r"D:\egovSrc\DGDE_Water And Sewarage Data\DataTemplates"
    fileName="rainmaker-ws"
    sheetName="ws-source"
    moduleName="rainmaker-ws"
    dfs = open_excel_file(os.path.join(filePath,fileName+".xlsx"))

    df = get_sheet(dfs, sheetName)
    #print(df)
    #df = df.replace('nan','NA')
    #df["message"] = df["message"].replace(numpy.nan, 'NA', regex=True)
    #df['hindi message'] =df['hindi message'].replace(numpy.nan, 'NA', regex=True)
    #df = df.fillna('NA')
    localization_data_en=[]
    localization_data_hi=[]
    for ind in df.index: 
        localization_data_en.append({
                        "code":df['code'][ind]  ,
                        "message": df['message'][ind],
                        "module": moduleName,
                        "locale": "en_IN"
                    })
        localization_data_hi.append({
                        "code":df['code'][ind]  ,
                        "message": df['hindi message'][ind],
                        "module": moduleName,
                        "locale": "hi_IN"
                    })
    #print(localization_data_hi)


    data_en = {
        "RequestInfo": {
            "authToken": "{{access_token}}"
        },
        "tenantId": config.TENANT,
        "messages": localization_data_en
    }
    data_hi = {
        "RequestInfo": {
            "authToken": "{{access_token}}"
        },
        "tenantId": config.TENANT,
        "messages": localization_data_hi
    }
    with io.open(os.path.join(filePath,fileName+"-en.json"), mode="w", encoding="utf-8") as f:
        json.dump(data_en, f, indent=2,  ensure_ascii=False)
    with io.open(os.path.join(filePath,fileName+"-hi.json"), mode="w", encoding="utf-8") as f:
        json.dump(data_hi, f, indent=2,  ensure_ascii=False)
  
    auth_token = superuser_login()["access_token"]
    print("auth_token   ", auth_token)
    localize_response = upsert_localization(auth_token, data_en)
    print("English data resp : " ,localize_response)
    localize_response = upsert_localization(auth_token, data_hi)
    print("Hindi data resp : " ,localize_response)

if __name__ == "__main__":
    main()
