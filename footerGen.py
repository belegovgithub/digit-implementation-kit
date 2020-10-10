from common import *
from config import config
import io
import os
import numpy
def main():
    print("FOOTER_JSON",config.FOOTER_JSON)
    with io.open(config.FOOTER_JSON, encoding="utf-8") as f:
        tenants_data = json.load(f)
    print("tennt data",tenants_data)
    found = False
    for found_index, tenant in enumerate(tenants_data["footer"]):
        if tenant["code"] == config.TENANT_ID:
            found = True
            break


    footer_object = {
      "code": config.TENANT_ID,
      "service": "TL",
      "receiptFooterContent": [
        {
          "disclaimer": "PDF_STATIC_LABEL_CONSOLIDATED_RECEIPT_DISCLAIMER_1",
          "order": "1."
        },
        {
          "disclaimer": "PDF_STATIC_LABEL_CONSOLIDATED_RECEIPT_DISCLAIMER_2",
          "order": "2."
        },
        {
          "disclaimer": "PDF_STATIC_LABEL_CONSOLIDATED_RECEIPT_DISCLAIMER_3",
          "order": "3."
        }
      ],
      "billFooterContent": [
        {
          "disclaimer": "nocNeighbour1",
          "order": "1."
        },
        {
          "disclaimer": "nocNeighbour2",
          "order": "2."
        },
        {
          "disclaimer": "planCert",
          "order": "3."
        },
        {
          "disclaimer": "buildingPhoto",
          "order": "4."
        }
      ]
    }
    import sys

    json.dump(footer_object, sys.stdout, indent=2)

    if config.ASSUME_YES:
        response = os.getenv("ASSUME_YES", None) or input("\nDo you want to append the data in repo (y/[n])? ")
    else:
        response = "y"

    if response.lower() == "y":
        with io.open(config.FOOTER_JSON, mode="w", encoding="utf-8") as f:
            if found:
                print("Tenant - " + config.TENANT_ID + " already exists, overwriting")
                assert tenants_data["footer"][found_index][
                           "code"] == config.TENANT_ID, "Updating for correct tenant id"
                tenants_data["footer"][found_index] = footer_object
            else:
                print("Tenant - " + config.TENANT_ID + " doesn't exists, adding details")
                tenants_data["footer"].append(footer_object)
            json.dump(tenants_data, f, indent=2,  ensure_ascii=False)

        print("Added the footer to MDMS data")
    else:
        print("Not adding the footer to MDMS data")


if __name__ == "__main__":
    main()
