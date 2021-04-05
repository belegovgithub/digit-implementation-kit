import json
from typing import Optional, List
from urllib.parse import urljoin
from uuid import UUID
import io
import os
import requests

from config import config
from uploader.parsers.utils import PropertyEncoder, convert_json, underscore_to_camel


class AdditionalDetail:
    initialMeterReading: Optional[int]

    def __init__(self, initialMeterReading: Optional[int] = None) -> None:
        self.initialMeterReading = initialMeterReading

class ProcessInstance:
    action: Optional[str]

    def __init__(self, action: Optional[str] = None) -> None:
        self.action = action

class Document:
    document_uid: None
    document_type: None

    def __init__(self, document_uid: None = None, document_type: None = None) -> None:
        self.document_uid = document_uid
        self.document_type = document_type

class ConstructionDetail:
    builtUpArea:None
    superBuiltUpArea: None
    plinthArea: None

    def __init__(self, builtUpArea: None = None, superBuiltUpArea: None = None, plinthArea: None = None) -> None:
        self.builtUpArea = builtUpArea
        self.superBuiltUpArea = superBuiltUpArea
        self.plinthArea = plinthArea

class ConnectionHolder:
    name: Optional[str]
    mobileNumber: Optional[str]
    fatherOrHusbandName: Optional[str]
    emailId: Optional[str]
    correspondenceAddress: Optional[str]
    relationship: Optional[str]
    ownerType: Optional[str]
    gender: Optional[str]
    sameAsPropertyAddress : Optional[bool]

    def __init__(self, name: Optional[str] = None,
                 mobileNumber: Optional[str] = None, fatherOrHusbandName: Optional[str] = None,
                 emailId: Optional[str] = None, correspondenceAddress: Optional[str] = None,
                 relationship: Optional[str] = None, ownerType: Optional[str] = None,
                 gender: Optional[str] = None,
                 sameAsPeropertyAddress : Optional[bool] = True,
                 ) -> None:
        self.name = name
        self.mobileNumber = mobileNumber
        self.fatherOrHusbandName = fatherOrHusbandName
        self.emailId = emailId
        self.correspondenceAddress = correspondenceAddress
        self.relationship = relationship
        self.ownerType = ownerType
        self.gender = gender
        self.sameAsPeropertyAddress = sameAsPeropertyAddress


class Property:
    propertyId: Optional[str]
    tenantId: Optional[str]

    def __init__(self, propertyId: Optional[str] = None, tenantId: Optional[str] = None) -> None:
        self.propertyId = propertyId,
        self.tenantId = tenantId

class WaterConnection:
    tenantId: Optional[str]
    propertyId: Optional[str]
    status: Optional[str]
    connectionNo: Optional[str]
    oldConnectionNo: Optional[str]
    proposedTaps: Optional[int]
    proposedPipeSize: Optional[float]
    propertyOwnership: Optional[str]
    connectionHolders: Optional[List[ConnectionHolder]]
    service: Optional[str]  
    water: Optional[str]  
    sewerage: Optional[str]  
    pipeSize : Optional[float]
    noOfTaps: Optional[int]
    motorInfo: Optional[str]
    applicationType: Optional[str]
    authorizedConnection: Optional[str]
    waterSource: Optional[str]
    sourceInfo: Optional[str]
    waterSubSource: Optional[str]
    connectionType : Optional[str]
    meterId: Optional[str]
    processInstance: Optional[ProcessInstance]
    documents: Optional[List[Document]]
    additionalDetails: Optional[AdditionalDetail]
    property: Optional[Property]
    source: Optional[str]
    channel: Optional[str]
    creationReason: Optional[str]
    applicationStatus: Optional[str]
    def __init__(self, tenantId: Optional[str] = None, propertyId: Optional[str] = None,
                 status: Optional[str]  =None, connectionNo: Optional[str] = None, oldConnectionNo: Optional[str] = None,
                 proposedTaps: Optional[int] = None, proposedPipeSize: Optional[float] = None, propertyOwnership: Optional[str]= None,
                 connectionHolders: Optional[List[ConnectionHolder]] = None, service: Optional[str] = None,
                 water: Optional[str] = None, sewerage: Optional[str] = None,
                 pipeSize : Optional[float] = None, noOfTaps: Optional[int] = None, motorInfo: Optional[str] = None,
                 applicationType: Optional[str] = None, authorizedConnection: Optional[str] = None,
                 waterSource: Optional[str] = None, sourceInfo: Optional[str] = None,
                 waterSubSource: Optional[str] = None, connectionType : Optional[str] = None, meterId : Optional[str] = None,
                 processInstance: Optional[ProcessInstance] = None, documents: Optional[List[Document]] = None,
                 additionalDetails: Optional[AdditionalDetail] =None, 
                 property: Optional[Property] = None, source: Optional[str] = None, channel: Optional[str] = None,
                 creationReason: Optional[str] = None, applicationStatus: Optional[str] = None ) -> None:
        self.tenantId = tenantId
        self.propertyId = propertyId
        self.status = status
        self.connectionNo = connectionNo
        self.oldConnectionNo = oldConnectionNo
        self.proposedTaps = proposedTaps
        self.proposedPipeSize = proposedPipeSize
        self.propertyOwnership = propertyOwnership
        self.connectionHolders = connectionHolders
        self.service = service
        self.water = water
        self.sewerage = sewerage
        self.pipeSize = pipeSize
        self.noOfTaps = noOfTaps
        self.motorInfo = motorInfo
        self.applicationType = applicationType
        self.authorizedConnection = authorizedConnection
        self.waterSource = waterSource
        self.sourceInfo = sourceInfo
        self.waterSubSource = waterSubSource
        self.connectionType = connectionType
        self.meterId = meterId
        self.processInstance = processInstance
        self.documents = documents
        self.additionalDetails = additionalDetails
        self.property = property
        self.source = source
        self.channel = channel
        self.creationReason = creationReason
        self.applicationStatus = applicationStatus

    def get_water_json(self):
        water_encoder = PropertyEncoder().encode(self)
        # print(json.loads(water_encoder))
        return convert_json(json.loads(water_encoder), underscore_to_camel)

    def upload_water(self, access_token, tenantId,  oldConnectionNo, root, name):       
        request_data = {
            "RequestInfo": {
                "authToken": access_token
            },
            "WaterConnection": 
                self.get_water_json()            
        }
        # print(json.dumps(request_data, indent=2)) 
        with io.open(os.path.join(root, name,"water_create_req.json"), mode="w", encoding="utf-8") as f:
            json.dump(request_data, f, indent=2,  ensure_ascii=False) 
        
        response = requests.post(
            urljoin(config.HOST, "/ws-services/wc/_create"),
            json=request_data)

        return response.status_code, response.json()        

    def search_water_connection(self,auth_token, tenantId, oldConnectionNo):
        url = urljoin(config.HOST, '/ws-services/wc/_search')        
        request_body = {}
        request_body["RequestInfo"] = {"authToken": auth_token}
        params = {"searchType":"CONNECTION","tenantId": tenantId, "oldConnectionNumber": oldConnectionNo}

        obj = requests.post(url, params=params, json=request_body)
        res = obj.json()
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
