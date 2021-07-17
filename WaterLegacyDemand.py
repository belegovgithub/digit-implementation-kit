import json
from typing import Optional, List
from urllib.parse import urljoin
from uuid import UUID
import io
import os
import requests
from datetime import date

from config import config
from uploader.parsers.utils import PropertyEncoder, convert_json, underscore_to_camel

class WaterDemand:
    oldConnectionNo: Optional[str]
    connectionNo: Optional[str]
    waterCharge: Optional[float]
    advance: Optional[float]
    penalty: Optional[float]
    
    def __init__(self, oldConnectionNo: Optional[str] = None, connectionNo: Optional[str] = None,
                 waterCharge: Optional[float] = None, advance: Optional[float] = None , penalty: Optional[float] = None) -> None:
        self.oldConnectionNo = oldConnectionNo
        self.connectionNo = connectionNo        
        self.waterCharge = waterCharge
        self.penalty = penalty       
        self.advance = advance       
        


class WaterDemands:
    waterDemands: Optional[List[WaterDemand]]       

    def __init__(self, waterDemands: Optional[List[WaterDemand]]  = None) -> None:
        self.waterDemands = waterDemands


    def get_demand_json(self):
        demand_encoder = PropertyEncoder().encode(self)
        # print(json.loads(water_encoder))
        return convert_json(json.loads(demand_encoder), underscore_to_camel)

    def upload_demand(self, auth_token, tenantId, legacyDemandArr, root, name):
        request_data = {
            "RequestInfo": {
                "authToken": auth_token
            },
            "tenantId": tenantId,
            "legacyDemands": 
                self.get_demand_json()            
        }
        print(json.dumps(request_data, indent=2)) 
        with io.open(os.path.join(root, name, "legacy_create_req.json"), mode="w", encoding="utf-8") as f:
            json.dump(request_data, f, indent=2,  ensure_ascii=False) 
        return
        response = requests.post(
            urljoin(config.HOST, "/ws-calculator/waterCalculator/_generateLegacyDemand"),
            json=request_data)

        return response.status_code, response.json()       

        

