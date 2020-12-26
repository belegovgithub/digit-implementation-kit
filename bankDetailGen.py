from common import *
from config import config
import io
import os 
from  processing import process_bank_details
def main():
    Flag =False
    tenantMapping={}
    print(config.TENANT_JSON,"config.TENANT_JSON")
    with io.open(config.TENANT_JSON, encoding="utf-8") as f:
        cb_module_data = json.load(f)
    for found_index, module in enumerate(cb_module_data["tenants"]):
        #print(module["description"])
        tenantMapping[module["description"].lower()]=module["code"]
    print(tenantMapping)
    for root, dirs, files in os.walk(r"D:\CBData\Verified CB Data\CC", topdown=True):
        for name in dirs:
            #print (os.path.join(root, name))
            subfolder = os.path.join(root, name)
            bank_details_file =os.path.join(root, name,"Bank_Details_Template.xlsx")
            if os.path.exists(bank_details_file) :
                print(bank_details_file)
                # print(root)

                city = root.replace(r"D:\CBData\Verified CB Data\CC\CB ","" ).strip().lower()

                if city not in tenantMapping:
                    print("Not In city",city)
                    continue
                config.CITY_NAME = city
                config.TENANT_ID = tenantMapping[city]
                callBank(bank_details_file)
                Flag=False
        if Flag : 
            break


def callBank(bank_details_file):
    dfs = open_excel_file(bank_details_file)
    print("city",config.CITY_NAME)
    print("tenant",config.TENANT_ID)
    bank = process_bank_details.bank(dfs)    
    #replaceNone(bank,None,null)
    bankbranch = process_bank_details.bankbranch(bank,dfs)
    print("JSON Response ",json.dumps(bankbranch,indent=2))
    accountcodepurpose = process_bank_details.accountcodepurpose(dfs)
    chartaccount = process_bank_details.chartaccount(accountcodepurpose,dfs)
    fund = process_bank_details.fund(dfs)
    bankaccount = process_bank_details.bankaccount(bankbranch, chartaccount, fund,dfs)
    print(bankaccount) 
    
      

if __name__ == "__main__":
    main()
