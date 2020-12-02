import math
import time
from math import isnan
import io
import os
import numpy
import xlrd as xlrd
import xlwt
from common import superuser_login, open_excel_file, get_sheet, fix_value
from config import config, load_config
import requests
import json

#from tlPreprocessor import create_trade_n_accessory_data
 
def main():
    tenants = [
        "pb.amritsar"
    ]

    INDEX_CATEGORY = 1
    INDEX_SLNO = 2
    INDEX_SUB_CATEGORY = 3
    INDEX_TRADE_AVAILABLE = 4
    INDEX_UOM = 5
    INDEX_RATE_TYPE = 6
    INDEX_RANGE1_FROM = 7
    INDEX_RANGE1_TO = 8
    INDEX_RANGE1_RATE = 9
    INDEX_RANGE2_FROM = 10
    INDEX_RANGE2_TO = 11
    INDEX_RANGE2_RATE = 12
    INDEX_RANGE3_FROM = 13
    INDEX_RANGE3_TO = 14
    INDEX_RANGE3_RATE = 15
    INDEX_RANGE4_FROM = 16
    INDEX_RANGE4_TO = 17
    INDEX_RANGE4_RATE = 18
    INDEX_RANGE5_FROM = 19
    INDEX_RANGE5_TO = 20
    INDEX_RANGE5_TO = 21
    INDEX_APPLICATION_FEE = 22

    thisdict = {
        "Eating Establishments": "EATING",
        "Veterinary Trades & trades dealing with animal products": "VETERINARY",
        "Medical Establishments": "MEDICAL",
        "Flammables": "DANGEROUS",
        "Small Scale Industries/Small & Medium factories": "MEDIUM",
        "Other Establishment/Offices (Non eating/non medical)": "OTHER"        
    }

    for tenant in tenants:
        print(tenant)
        # response = os.getenv("ASSUME_YES", None) or input(
        #     "Your ENV is \"{}\" , You want to proceed (y/[n])?".format(config.CONFIG_ENV))
        # if response.lower() == "n":
        #     os._exit(0)

        config.CITY_NAME = tenant.replace(" ", "").replace("pb.", "")
        load_config()

        tenant_id = config.TENANT_ID

        auth_token = superuser_login()["access_token"]

        slabs = requests.post(config.HOST + "/tl-calculator/billingslab/_search?tenantId=" + tenant_id, json={
            "RequestInfo": {
                "authToken": auth_token
            }
        })

        existing_slab_data = {get_slab_id(slab): slab for slab in slabs.json()["billingSlab"]}

        # print(json.dumps(existing_slab_data, indent=2))
        source_file = config.BASE_PPATH / "source" / "{}.xlsx".format(tenant_id)
        # create_trade_n_accessory_data(tenant_id, source_file, destination_path=config.BASE_PPATH / "source",
        #                             template_file_path="source/template.xlsx")

        #dfs = open_excel_file(config.BASE_PPATH / "source" / "{}.processed.xls".format(tenant_id))
        dfs = open_excel_file(config.TRADE_RATE_WORKBOOK)
        data = get_sheet(dfs, config.SHEET_TRADERATE)
        
        #category = fix_value(data.iloc[INDEX_TENANT_ULB_NAME][INDEX_CATEGORY])

        # data.fillna(value=0)
        columns = ["tenantid", "id", "licensetype", "structuretype", "tradetype", "accessorycategory", "type", "uom",
                "fromuom", "touom", "rate", "createdtime", "createdby", "lastmodifiedtime", "lastmodifiedby"]
        fields = {field: index for index, field in enumerate([])}
        count=0
        new_slabs = {}
        update_slabs = {}
        slabs_processed = set()
        for id, row in data.iterrows():
            row_data = row.to_dict()
            print(row_data)
            slab_id = get_slab_id(row_data)

            if slab_id in slabs_processed:
                print("Problem detected, duplicate slab id " + slab_id)

            slabs_processed.add(slab_id)
            count = count + 1
            print(count)
            if slab_id not in existing_slab_data:
                if type(row_data["rate"]) is str:
                    row_data["rate"] = row_data["rate"].strip()

                    if row_data["rate"]:
                        row_data["rate"] = float(row_data["rate"])
                    else:
                        row_data["rate"] = math.nan

                if not math.isnan(row_data["rate"]):
                    new_slabs[slab_id] = row_data
            else:
                if numpy.isnan(row_data["rate"]):
                    row_data["rate"] = 0.0

                if row_data["rate"] != existing_slab_data[slab_id]["rate"]:
                    update_slabs[slab_id] = row_data
                    update_slabs[slab_id]["id"] = existing_slab_data[slab_id]["id"]

        # print(new_slabs, update_slabs)

        new_slabs_data = []
        update_slabs_data = []

        for slab_id, row_data in new_slabs.items():
            new_slabs_data.append(get_slab_object(row_data))

        for slab_id, row_data in update_slabs.items():
            update_slabs_data.append(get_slab_object(row_data))

        # print(new_slabs_data, json.dumps(update_slabs_data, indent=2))

        if new_slabs_data:
            # print(json.dumps(new_slabs_data, indent=2))
            res = requests.post(config.HOST + "/tl-calculator/billingslab/_create?tenantId={}".format(tenant_id), json={
                "RequestInfo": {
                    "authToken": auth_token
                },
                "billingSlab": new_slabs_data
            })

            print(json.dumps(res.json(), indent=2))

        if update_slabs_data:
            print("Updating changed billing slabs")
            print(json.dumps(update_slabs_data, indent=2))
            res = requests.post(config.HOST + "/tl-calculator/billingslab/_update?tenantId={}".format(tenant_id), json={
                "RequestInfo": {
                    "authToken": auth_token
                },
                "billingSlab": update_slabs_data
            })

            print(json.dumps(res.json(), indent=2))


def remove_nan(data, default=None):
    if type(data) in (float, int) and math.isnan(data):
        return default

    if type(data) is str:
        data = data.strip()

    return data


def get_slab_object(row_data):
    data = {
        "tenantId": tenant_id,
        "licenseType": remove_nan(row_data["licenseType"]),
        "structureType": remove_nan(row_data["structureType"]),
        "tradeType": remove_nan(row_data["tradeType"]),
        "accessoryCategory": remove_nan(row_data["accessoryCategory"]),
        "type": remove_nan(row_data["type"]),
        "uom": remove_nan(row_data["uom"]),
        "fromUom": remove_nan(row_data["fromUom"]),
        "toUom": remove_nan(row_data["toUom"]),
        "rate": remove_nan(row_data["rate"], default=0.0),
        "applicationFee": remove_nan(row_data["applicationFee"], default=0.0)
    }

    if "id" in row_data and type(row_data['id']) is str and len(row_data["id"]) > 6:
        data["id"] = row_data["id"]

    return data


def get_slab_id(slab):
    fields = ["licenseType", "structureType", "tradeType", "accessoryCategory", "type", "uom", "fromUom", "toUom"]
    data = []

    for field in fields:
        value = slab[field]
        if type(value) is not str and value is not None and isnan(value):
            value = None
        if value == "N.A.":
            value = None
        elif value == "NULL":
            value = None
        elif value == "Infinite":
            value = "Infinity"

        if type(value) is float:
            value = int(value)

        data.append(str(value or "-"))

    return "|".join(data)

if __name__ == "__main__":
    main()