from common import *
from config import config
import io
import os 
import sys
import pandas as pd
import copy
from collections import OrderedDict
from pandas import ExcelWriter


def getDictValue(dictObj, key,defaultValue ="NOT DEFINED") :
    if key in dictObj : 
        return dictObj[key]
    return defaultValue


BILLING_SLAB_LIST =['propertyOwnershipCategory', 'connectionType', 'calculationAttribute', 'buildingType', 'PropertyLocation', 'slabs', 'waterSource', 'minimumCharge', 'ownershipCategory', 'buildingSubType', 'motorCharge', 'ownerType', 'id', 'unAuthorizedConnection', 'maximumCharge', 'authorizedConnection', 'maintenanceCharge']

filter_keys=["authorizedConnection",'propertyOwnershipCategory','ownershipCategory', 'ownerType', 'buildingSubType',
 'majorUsageType',   'PropertyLocation',   'buildingType', 'waterSource']
NOT_DEFINED="NOT DEFINED"
EMPTY_VALUE =None
lst =["Water consumption","No. of taps"]
attributeMasterData={
    "authorizedConnection" :{
        "path":r"ws-services-masters\authorizedConnection.json",
        "key" : "authorizedConnection",
    },
    "propertyOwnershipCategory":{
        "path":r"PropertyTax\PropertyOwnershipCategory.json",
        "key" : "PropertyOwnershipCategory",
    },
    "ownershipCategory": {
        "path":r"PropertyTax\OwnerShipCategory.json",
        "key" : "OwnerShipCategory",
    },
    "ownerType":{
        "path":r"PropertyTax\OwnerType.json",
        "key" : "OwnerType",
    },
    "buildingSubType":{
        "path": r"ws-services-masters\waterUsage.json",
        "key" : "waterUsage",
    },
    "majorUsageType":{
        "path": r"ws-services-masters\waterUsage.json",
        "key" : "waterUsage",
    },
    "PropertyLocation":{
        "path": r"PropertyTax\PropertyLocation.json",
        "key" : "PropertyLocation",
    },
    "buildingType":{
        "path": r"ws-services-masters\waterUsage.json",
        "key" : "waterUsage",
    },
    "waterSource":{
        "path":r"ws-services-masters\waterSource.json",
        "key" : "waterSource",
    }

}

CANNONICAL_NAME ={
  "ownershipCategory": "Owner Type Of Property",
  "calculationAttribute": "Unit Of Measurement",
  "attribute" :"Unit Of Measurement",
  "propertyOwnershipCategory": "Connection Owned By",
  "buildingType": "Water Usage ",
  "majorUsageType": "Water Major Usage",
  "ownerType": "Category Of Connection Holder",
  "connectionType": "Connection Type",
  "waterSource": "Source Of Water",
  "authorizedConnection": "Connection Authorization",
  "buildingSubType": "Water Sub Usage",
  "maintenanceCharge": "Maintance Charge",
  "PropertyLocation": "Location Of Property",
  "id": "Billing Slab Id",
  "minimumCharge": "Minimum Bill Charge",
  "motorCharge": "Motor Charge",
  "maximumCharge": "Maximum Bill Charge", 
  "cbname" :"CB Name",
  "filterAttribute": "Data Filter Param",
  "type": "Calculation Type",
  "meterCharge": "Meter Charges",
  "to": "Slab To",
  "from": "Slab From",
  "charge": "Per Unit Charge",
  "billingAppliable":"Bill Applicable",
  "billingCycle":"Billing Cycle",
  "connectionType" :"Connection Type",
#   "demandGenerationDateMillis":"Bill Generation Day",
#   "demandExpiryDate":"Bill Expiry Day",
#   "demandEndDateMillis":"Bill Due Day",
#   "calcAttrDefined":"Validation On calculation",
#   "calcJsonParamActive" :"Validation On CalculationJson Active",
#   "validationBillingSlabCalculionMismatch":"Calculation Attribute Mismatch",
#   "validationInvalidFilterValue" : "Invalid Filter Parameter",
#   "validationFilterValueNotDefined" :"Filter Value Not Defined In Slabs",
 
}

def addKeyToDict(dict, key,value) :
    if key in CANNONICAL_NAME :
        if CANNONICAL_NAME[key] not in dict : 
            dict[CANNONICAL_NAME[key]]=value



BILLING_SLAB_TEMPLATE={
  "ownershipCategory": None,
  "calculationAttribute": "M",
  "propertyOwnershipCategory": None,
  "buildingType": None,
  "ownerType": None,
  "connectionType": "M",
  "waterSource": None,
  "slabs": [],
  "authorizedConnection": None,
  "buildingSubType": None,
  "maintenanceCharge": 0,
  "PropertyLocation": None,
  "id": "M",
  "minimumCharge": 0,
  "motorCharge": 0,
  "maximumCharge": 0, 
}

BILL_TEMPLATE={
  "type": "FLAT",
  "meterCharge": 0,
  "to": "M",
  "from": "M",
  "charge": 0
}


def main ():
     
    cbMapping=[]
    for key in attributeMasterData : 
        data =attributeMasterData[key]
        if os.path.isfile(os.path.join(config.MDMS_LOCATION,data["path"] )) :
            with io.open(os.path.join(config.MDMS_LOCATION,data["path"] ), encoding="utf-8") as f:
                # print( data["key"])
                # print(json.load(f))
                data["data"] =json.load(f)[data["key"]]
    with io.open(os.path.join(config.MDMS_LOCATION,"master.json"), mode="w", encoding="utf-8") as f:
        json.dump(attributeMasterData, f, indent=2,  ensure_ascii=False, cls=DateTimeEncoder)  
                

    with io.open(config.TENANT_JSON, encoding="utf-8") as f:
        cb_module_data = json.load(f)
        for found_index, module in enumerate(cb_module_data["tenants"]):
            if module["code"].find(".")==-1 : 
              continue
            cbname = module["code"].split(".")[1]
            if cbname=="testing" :
                continue
            # if cbname !="ambala":
            #     continue

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
                    billPeriodMatchWithCalc =False
                    if not billingRow["active"] :
                        continue
                    for calcAttr in CalculationAttribute :
                        if calcAttr["name"] == billingRow["connectionType"] :
                            billPeriodMatchWithCalc=True
                            if not calcAttr["active"] : 
                                cb_dict= createDict(cbName =cbname,billApplicable=True,calcAttrDefined="Not Active" ,billingRow=billingRow  )
                                cbMapping.append(cb_dict)
                                continue
                            isSlabDefined =False
                            for wcBillSlab in WCBillingSlab : 
                                if wcBillSlab["connectionType"]==billingRow["connectionType"]  :
                                    isSlabDefined =True
                                    cb_dict =createDict(cbName =cbname,billApplicable=True,calcAttrDefined="Active" ,billingRow=billingRow  )
                                    addKeyToDict( cb_dict,"calcJsonParamActive",getDictValue (calcAttr ,"active"))
                                    calcAttrBilling=getDictValue (calcAttr ,"attribute" )
                                    filterAttr=getDictValue (calcAttr,"filterAttribute",[] )
                                    if "filterAttribute"  not in calcAttr :
                                        addKeyToDict( cb_dict,"validationFilterAttrNotDefined",NOT_DEFINED)

                                    if calcAttrBilling !=  getDictValue (wcBillSlab ,"calculationAttribute" ) :
                                        addKeyToDict( cb_dict,"validationBillingSlabCalculionMismatch",getDictValue (wcBillSlab ,"calculationAttribute" ))
                                    
                                    filterDisplayList =""
                                    for findex, f in enumerate(filterAttr):
                                        filterDisplayList = filterDisplayList +"{0}. {1} \n".format(findex+1, CANNONICAL_NAME[f] )
                                    if len(filterDisplayList)> 0 : 
                                        filterDisplayList=filterDisplayList[:-2]
                                    addKeyToDict( cb_dict,"filterAttribute",filterDisplayList)
                                    addKeyToDict( cb_dict,"attribute",getDictValue (calcAttr ,"attribute" ))
                                    invalidKey =set(filterAttr) -set(filter_keys)
                                    if len(invalidKey) > 0 :
                                        addKeyToDict( cb_dict,"validationInvalidFilterValue",list(invalidKey))
 
                                    
                                    values_not_defined=[]
                                    for filterkey in filterAttr :
                                        fkey =filterkey
                                        if filterkey =="majorUsageType" :
                                            fkey="buildingType"
                                        if fkey not in wcBillSlab.keys() :
                                            values_not_defined.append(fkey)
                                    if len(values_not_defined) > 0 :
                                        addKeyToDict( cb_dict,"validationFilterValueNotDefined",list(values_not_defined))
                                    
                                    for ele in wcBillSlab : 
                                        fkey =ele
                                        if ele == "buildingType" and  "majorUsageType" in filterAttr:
                                            ele="majorUsageType"
                                        value = getDictValue (wcBillSlab ,fkey )
                                        if ele in attributeMasterData :
                                            listData =attributeMasterData[ele]["data"]
                                            for l in listData : 
                                                if l["code"]==value : 
                                                    value=l["name"]
                                        addKeyToDict(cb_dict,ele,value)
                                    slabs =getDictValue (wcBillSlab ,"slabs",[] ) 
                                    if len(slabs)>0 : 
                                        for slab in slabs :  
                                            slab_data = copy.deepcopy(cb_dict)
                                            for s in slab : 
                                                addKeyToDict(slab_data,s,getDictValue (slab ,s ))
                                            if "type" in slab_data : 
                                                del slab_data["type"]
                                            type="Flat"
                                            if calcAttrBilling in lst :
                                                type="Rate"
                                                
                                            addKeyToDict(slab_data,"type",type)
                                            cbMapping.append(slab_data)
                                    else : 
                                        cbMapping.append(cb_dict)
                            if  not isSlabDefined :
                                cb_dict= createDict(cbName =cbname,billApplicable=True,calcAttrDefined="Not Active" ,billingRow=billingRow  )
                                cb_dict["Billing Slab Defined"]="No"
                                cbMapping.append(cb_dict)


                    if not billPeriodMatchWithCalc : 
                        cb_dict= createDict(cbName =cbname,billApplicable=True,calcAttrDefined="No",billingRow=billingRow  )
                        cbMapping.append(cb_dict)
                        

                    


            else : 
                cbMapping.append(createDict(cbName=  cbname  ))
    with io.open(os.path.join(config.MDMS_LOCATION,"billing_mapping.json"), mode="w", encoding="utf-8") as f:
        json.dump(cbMapping, f, indent=2,  ensure_ascii=False, cls=DateTimeEncoder)  
    df = pd.read_json (json.dumps(cbMapping))
    df.to_excel(os.path.join(config.MDMS_LOCATION,"Consolidate Water Bill Parameter.xlsx"), index = None,
        columns=["CB Name","Bill Applicable","Billing Cycle","Connection Type","Data Filter Param",
        "Billing Slab Id",
        "Location Of Property" ,"Water Usage ","Water Sub Usage", "Owner Type Of Property", 
         "Connection Owned By","Category Of Connection Holder","Source Of Water","Connection Authorization","Category Of Connection Holder",
         "Unit Of Measurement",
          "Calculation Type",
         "Slab From","Slab To","Meter Charges","Per Unit Charge",
          "Minimum Bill Charge","Maximum Bill Charge","Maintance Charge","Motor Charge"
         ]
    )

    with io.open(os.path.join(config.MDMS_LOCATION,"MasterData.json"), mode="w", encoding="utf-8") as f:
        json.dump(attributeMasterData, f, indent=2,  ensure_ascii=False, cls=DateTimeEncoder) 
    import xlsxwriter
    writer = ExcelWriter(os.path.join(config.MDMS_LOCATION,"Master Data For Bill.xlsx"))
    for key in attributeMasterData:
        master_data=attributeMasterData[key]["data"]

        if key =="buildingSubType" :
            master_data =[x for x in master_data if len(x["code"].split(".")) == 2 ]
        elif key =="buildingType" or  key =="majorUsageType" : 
            master_data =[x for x in master_data if len(x["code"].split(".")) == 1 ]
        data =[]
        for d in master_data : 
            data.append({"Code" :d["code"] ,"Name" :d["name"] })
             
        df = pd.read_json (json.dumps(data))
        df.to_excel(writer, CANNONICAL_NAME[key],index=False)
    writer.save()

    return


def createDict(cbName="", billApplicable=False,calcAttrDefined="No", billingRow=None) :
    cb_dict =OrderedDict()
    addKeyToDict(cb_dict,"cbname",cbName)
    addKeyToDict(cb_dict,"billingAppliable",("Applicable" if billApplicable else  "Not Applicable"))  

    if billApplicable : 
        addKeyToDict(cb_dict,"calcAttrDefined",calcAttrDefined)   
    if billingRow is not None : 
        addKeyToDict(cb_dict,"billingCycle",getDictValue (billingRow ,"billingCycle",None ) )   
        addKeyToDict(cb_dict,"connectionType",getDictValue (billingRow ,"connectionType",None ) )  
        addKeyToDict(cb_dict,"demandGenerationDateMillis",int (getDictValue (billingRow ,"demandGenerationDateMillis",0 ) /86400000 ) )  
        addKeyToDict(cb_dict,"billingCycle",int (getDictValue (billingRow ,"demandExpiryDate",0 ) /86400000 ) )  
        addKeyToDict(cb_dict,"demandEndDateMillis",int (getDictValue (billingRow ,"demandEndDateMillis",0 ) /86400000 ) )  
    return cb_dict
     

 
if __name__ == "__main__":
    main()
