import json
from typing import Optional, List
from urllib.parse import urljoin
from uuid import UUID
import io
import os
import requests
from config import config
from uploader.parsers.utils import PropertyEncoder, convert_json, underscore_to_camel


class PropertyAdditionalDetails:
    pass

    def __init__(self, ) -> None:
        pass


class Locality:
    code: Optional[str]

    def __init__(self, code: Optional[str] = None) -> None:
        self.code = code


class Address:
    city: Optional[str]
    location: Optional[str]
    locality: Optional[Locality]
    doorNo: Optional[str]
    buildingName: Optional[str]
    street: Optional[str]    
    pincode: Optional[int]

    def __init__(self, city: Optional[str] = None, location: Optional[str] = None, doorNo: Optional[str] = None, buildingName: Optional[str] = None,
                 street: Optional[str] = None, locality: Optional[Locality] = None, pincode: Optional[int] = None) -> None:
        self.city = city
        self.location = location
        self.doorNo = doorNo
        self.buildingName = buildingName
        self.street = street
        self.locality = locality
        self.pincode = pincode


class AdditionalDetails:
    isRainwaterHarvesting: Optional[bool]

    def __init__(self, isRainwaterHarvesting: Optional[bool] = False) -> None:
        self.isRainwaterHarvesting = isRainwaterHarvesting


class Document:
    document_uid: None
    document_type: None

    def __init__(self, document_uid: None = None, document_type: None = None) -> None:
        self.document_uid = document_uid
        self.document_type = document_type

class ConstructionDetail:
    builtUpArea:Optional[int]
    superBuiltUpArea: Optional[int]
    plinthArea: Optional[int]

    def __init__(self, builtUpArea: None = None, superBuiltUpArea: None = None, plinthArea: None = None) -> None:
        self.builtUpArea = builtUpArea
        self.superBuiltUpArea = superBuiltUpArea
        self.plinthArea = plinthArea

class Owner:
    name: Optional[str]
    mobileNumber: Optional[str]
    fatherOrHusbandName: Optional[str]
    emailId: Optional[str]
    correspondenceAddress: Optional[str]
    relationship: Optional[str]
    ownerType: Optional[str]
    gender: Optional[str]
    altContactNumber: Optional[str]
    sameAsPeropertyAddress : Optional[bool]
    status: Optional[str]

    def __init__(self, name: Optional[str] = None,
                 mobileNumber: Optional[str] = None, fatherOrHusbandName: Optional[str] = None,
                 emailId: Optional[str] = None, correspondenceAddress: Optional[str] = None,
                 relationship: Optional[str] = None, ownerType: Optional[str] = None,
                 gender: Optional[str] = None,
                 altContactNumber: Optional[str] = None,
                 sameAsPeropertyAddress : Optional[bool] = True,
                 status: Optional[str] = None
                 ) -> None:
        self.name = name
        self.mobileNumber = mobileNumber
        self.fatherOrHusbandName = fatherOrHusbandName
        self.emailId = emailId
        self.correspondenceAddress = correspondenceAddress
        self.relationship = relationship
        self.ownerType = ownerType
        self.gender = gender
        self.altContactNumber = altContactNumber
        self.sameAsPeropertyAddress = sameAsPeropertyAddress
        self.status = status

class Unit:
    usageCategory: Optional[str]
    occupancyType: Optional[str]
    constructionDetail : Optional[ConstructionDetail]
    arv: Optional[float]
    floorNo: Optional[int]

    def __init__(self, usageCategory: Optional[str] = None,
                 occupancyType: Optional[str] = None,
                 constructionDetail : Optional[ConstructionDetail] = None,
                 arv: Optional[float] = None, floorNo: Optional[int] = 0) -> None:
        self.usageCategory = usageCategory
        self.occupancyType = occupancyType
        self.constructionDetail = constructionDetail
        self.arv = arv
        self.floorNo = floorNo


class Institution:
    name: Optional[str]
    type: Optional[str]
    designation: Optional[str]

    def __init__(self, name: Optional[str] = None, type: Optional[str] = None,
                 designation: Optional[str] = None) -> None:
        self.name = name
        self.type = type
        self.designation = designation


class Property:
    tenantId: Optional[str]
    abasPropertyId: Optional[str]
    oldPropertyId: Optional[str]
    address: Optional[Address]
    propertyType: Optional[str]
    usageCategory: Optional[str]
    subUsageCategory: Optional[str]
    units: Optional[List[Unit]]    
    landArea: Optional[float]
    superBuiltUpArea: Optional[float]    
    noOfFloors: Optional[int]
    noOfFlats: Optional[int]
    ownershipCategory: Optional[str]
    owners: Optional[List[Owner]]
    financialYear: Optional[str]
    institution: Optional[Institution]
    documents: Optional[List[Document]]
    additional_details: Optional[AdditionalDetails]
    source: Optional[str]                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           
    channel: Optional[str]
    creationReason: Optional[str]

    def __init__(self, tenantId: Optional[str]= None,  oldPropertyId: Optional[str] = None, abasPropertyId: Optional[str] = None,
                 address: Optional[Address]  =None, subUsageCategory: Optional[str] = None, units: Optional[List[Unit]] = None,
                 usageCategory: Optional[str] = None,
                 landArea: Optional[int] = None, superBuiltUpArea: Optional[int] = None,
                 propertyType: Optional[str] = None, noOfFloors: Optional[int] = None, noOfFlats: Optional[int] = None,
                 ownershipCategory: Optional[str] = None,
                 owners: Optional[List[Owner]] = None, financialYear: Optional[str] = None,
                 institution: Optional[Institution] = None,
                 source: Optional[str] = None, channel: Optional[str] = None, creationReason: Optional[str] = None,
                 additionalDetails: Optional[AdditionalDetails] = None, documents: Optional[List[Document]] = None) -> None:
        self.tenantId = tenantId
        self.oldPropertyId = oldPropertyId
        self.abasPropertyId = abasPropertyId
        self.address = address
        self.subUsageCategory = subUsageCategory
        self.units = units
        self.usageCategory = usageCategory
        self.landArea = landArea
        self.superBuiltUpArea = superBuiltUpArea
        self.propertyType = propertyType
        self.noOfFloors = noOfFloors
        self.noOfFlats = noOfFlats
        self.ownershipCategory = ownershipCategory
        self.owners = owners
        self.financialYear = financialYear
        self.additional_details = additionalDetails
        self.institution = institution
        self.documents = documents
        self.source = source
        self.channel = channel

    def get_property_json(self):
        property_encoder = PropertyEncoder().encode(self)
        # print(property_encoder)
        return convert_json(json.loads(property_encoder), underscore_to_camel)

    def upload_property(self, access_token, tenantId, abasPropertyId, root, name):
        request_data = {
            "RequestInfo": {
                "authToken": access_token
            },
            "Property":  
                self.get_property_json()            
        }
        # print(json.dumps(request_data, indent=2))
        with io.open(os.path.join(root, name,"property_create_req.json"), mode="w", encoding="utf-8") as f:
            json.dump(request_data, f, indent=2,  ensure_ascii=False)
        response = requests.post(
            urljoin(config.HOST, "/property-services/property/_create"),
            json=request_data)

        return response.status_code, response.json()

    def search_abas_property(self,auth_token, tenantId, abasPropertyId):
        url = urljoin(config.HOST, '/property-services/property/_search')        
        request_body = {}
        request_body["RequestInfo"] = {"authToken": auth_token}
        params = {"tenantId": tenantId, "abasPropertyids": abasPropertyId}        
        obj = requests.post(url, params=params, json=request_body)
        res = obj.json()
        # print(json.dumps(res, indent=2))
        if(obj.status_code == 200):          
            return True, res
        else:

            return False, res

class RequestInfo:
    api_id: Optional[str]
    ver: Optional[str]
    ts: Optional[str]
    action: Optional[str]
    did: Optional[int]
    key: Optional[str]
    msg_id: Optional[str]
    auth_token: Optional[UUID]

    def __init__(self, api_id: Optional[str] = None, ver: Optional[str] = None, ts: Optional[str] = None,
                 action: Optional[str] = None, did: Optional[int] = None, key: Optional[str] = None,
                 msg_id: Optional[str] = None, auth_token: Optional[UUID] = None) -> None:
        self.api_id = api_id
        self.ver = ver
        self.ts = ts
        self.action = action
        self.did = did
        self.key = key
        self.msg_id = msg_id
        self.auth_token = auth_token


class PropertyCreateRequest:
    request_info: Optional[RequestInfo]
    properties: Optional[List[Property]]

    def __init__(self, request_info: Optional[RequestInfo] = None, properties: Optional[List[Property]] = None) -> None:
        self.request_info = request_info
        self.properties = properties
