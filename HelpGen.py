from common import *
from config import config
import io
import os
import numpy
def main():
    print("HELP_JSON",config.HELP_JSON)
    with io.open(config.HELP_JSON, encoding="utf-8") as f:
        tenants_data = json.load(f)
    print("tenant data",tenants_data)
    found = False
    for found_index, tenant in enumerate(tenants_data["Help"]):
        if tenant["tenant"] == config.TENANT_ID:
            found = True
            break


    help_object = {
      "tenant": config.TENANT_ID,
      "code": "TL",
      "URL": "https://github.com/belegovgithub/webaccess/raw/master/pdf/{}/TradeTypeSubtypeDetails_{}.pdf".format(config.CITY_NAME.lower(),config.CITY_NAME)
    }
    import sys

    json.dump(help_object, sys.stdout, indent=2)

    response = os.getenv("ASSUME_YES", None) or input("\nDo you want to append the data in repo (y/[n])? ")

    if response.lower() == "y":
        with io.open(config.HELP_JSON, mode="w", encoding="utf-8") as f:
            if found:
                print("Tenant - " + config.TENANT_ID + " already exists, overwriting")
                assert tenants_data["Help"][found_index][
                           "tenant"] == config.TENANT_ID, "Updating for correct tenant id"
                tenants_data["Help"][found_index] = help_object
            else:
                print("Tenant - " + config.TENANT_ID + " doesn't exists, adding details")
                tenants_data["Help"].append(help_object)
            json.dump(tenants_data, f, indent=2,  ensure_ascii=False)

        print("Added the help to MDMS data")
    else:
        print("Not adding the help to MDMS data")


if __name__ == "__main__":
    main()
