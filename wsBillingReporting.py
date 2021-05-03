from common import *
from config import config
import io
import os 
import sys
import pandas as pd
import copy
from collections import OrderedDict

def getDictValue(dictObj, key,defaultValue ="NOT DEFINED") :
    if key in dictObj : 
        return dictObj[key]
    return defaultValue



def main ():
    filter_keys=['ownershipCategory', 'ownerType', 'buildingSubType', 'majorUsageType', 'Pipe Size', 'PropertyLocation', 'propertyOwnershipCategory', 'buildingType', 'waterSource']
    NOT_DEFINED="NOT DEFINED"
    tenantMapping=[]
    cbMapping =[]
    print(config.TENANT_JSON)
    with io.open(config.TENANT_JSON, encoding="utf-8") as f:
        cb_module_data = json.load(f)
        for found_index, module in enumerate(cb_module_data["tenants"]):
            if module["code"].find(".")==-1 : 
              continue
            cbname = module["code"].split(".")[1]
            billPerJsonPath =os.path.join(config.MDMS_LOCATION,cbname,"ws-services-masters","billingPeriod.json")
            calcAttrJsonPath =os.path.join(config.MDMS_LOCATION,cbname,"ws-services-calculation","CalculationAttribute.json")
            billingSlabJsonPath =os.path.join(config.MDMS_LOCATION,cbname,"ws-services-calculation","WCBillingSlab.json")
             

            if os.path.isfile(billPerJsonPath) :

                WCBillingSlab=[]
                CalculationAttribute=[]
                billingPeriod=[]
                with io.open(billPerJsonPath, encoding="utf-8") as f:
                    billingPeriod =json.load(f)["billingPeriod"]
                with io.open(calcAttrJsonPath, encoding="utf-8") as f:
                    CalculationAttribute =json.load(f)["CalculationAttribute"]
                with io.open(billingSlabJsonPath, encoding="utf-8") as f:
                    WCBillingSlab =json.load(f)["WCBillingSlab"]
                for billingRow in billingPeriod:
                    for calcAttr in CalculationAttribute :
                        if calcAttr["name"] == billingRow["connectionType"] :
                            for wcBillSlab in WCBillingSlab : 
                                if wcBillSlab["connectionType"]==billingRow["connectionType"]  :
                                    cb_dict =OrderedDict()
                                    cb_dict["CB Name"]=cbname
                                    cb_dict["Is Billing Enabled"]=True
                                    cb_dict.update(billingRow)
                                    cb_dict["Is Calc Billing Enabled"]=getDictValue (calcAttr ,"active")
                                    
                                    if "filterAttribute"  in calcAttr : 
                                        cb_dict["filterAttribute"]= " ; ".join(getDictValue (calcAttr,"filterAttribute",[] ))
                                    else : 
                                        cb_dict["filterAttribute"]=NOT_DEFINED
                                    cb_dict["Calculation Attribute"]=getDictValue (calcAttr ,"attribute" )
                                    for filterkey in filter_keys :
                                        fkey =filterkey
                                        if filterkey =="majorUsageType" :
                                            fkey="buildingType"
                                        cb_dict[filterkey] =getDictValue (wcBillSlab ,fkey )
                                    cb_dict["Billng Id"]= getDictValue (wcBillSlab ,"id" )
                                    cb_dict["Billng Calculation Attribute"]= getDictValue (wcBillSlab ,"calculationAttribute" )
                                    cb_dict["Billng Calculation Attribute"]= getDictValue (wcBillSlab ,"calculationAttribute" )
                                    cb_dict["Billng Calculation Attribute"]= getDictValue (wcBillSlab ,"calculationAttribute" )
                                    cb_dict["Billng Calculation Attribute"]= getDictValue (wcBillSlab ,"calculationAttribute" )
                                    cb_dict["Minimum Charge"]= getDictValue (wcBillSlab ,"minimumCharge" )
                                    #cb_dict.update(wcBillSlab)
                                    slabs =getDictValue (wcBillSlab ,"slabs",[] ) 
                                    if len(slabs)>0 : 
                                        for slab in slabs : 
                                            slab_data = copy.deepcopy(cb_dict)
                                            slab_data.update(slab)
                                            cbMapping.append(slab_data)
                                    else : 
                                        cbMapping.append(cb_dict)


                    


            else : 
                cb_dict =OrderedDict()
                cb_dict["CB Name"]=cbname
                cb_dict["Is Billing Enabled"]=False
                cbMapping.append(cb_dict)
    with io.open(os.path.join(config.MDMS_LOCATION,"billing_mapping.json"), mode="w", encoding="utf-8") as f:
        json.dump(cbMapping, f, indent=2,  ensure_ascii=False, cls=DateTimeEncoder)  
    df = pd.read_json (json.dumps(cbMapping))
    df.to_excel(os.path.join(config.MDMS_LOCATION,"billing_mapping_data.xlsx"), index = None)
             
    print(os.path.join(config.MDMS_LOCATION,"billing_mapping.json"))

 



 
    return

   

 
if __name__ == "__main__":
    main()
