from common import *
from config import config
import io
import os
import numpy
def main():
    print("CITY_MODULE_JSON",config.CITY_MODULE_JSON)
    with io.open(config.CITY_MODULE_JSON, encoding="utf-8") as f:
        tenants_data = json.load(f)
    print("tenant data",tenants_data["citymodule"])
    found = False
    for found_index, tenant in enumerate(tenants_data["citymodule"] ):
      for found_index1, t in enumerate(tenant["tenants"] ):  
        if t["code"] == config.TENANT_ID:
            found = True
            break


    cityModule_object = {
      "code": config.TENANT_ID      
    }
    import sys

    json.dump(cityModule_object, sys.stdout, indent=2)
    if config.ASSUME_YES:
        response = os.getenv("ASSUME_YES", None) or input("\nDo you want to append the data in repo (y/[n])? ")
    else:
        response = "y"

    if response.lower() == "y":
        with io.open(config.CITY_MODULE_JSON, mode="w", encoding="utf-8") as f:
            if not found:
                print("Tenant - " + config.TENANT_ID + " doesn't exists, adding details")
                for found_index, tenant in enumerate(tenants_data["citymodule"] ):
                  tenant["tenants"].append(cityModule_object)
                json.dump(tenants_data, f, indent=2,  ensure_ascii=False)

        print("Added the help to MDMS data")
    else:
        print("Not adding the help to MDMS data")


if __name__ == "__main__":
    main()
