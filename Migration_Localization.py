from common import *
from config import config
from common import superuser_login
import io
import os
import numpy

recv_host = "https://13.71.65.215.nip.io"
send_host = "https://demo.echhawani.gov.in"
recv_auth = "9804cdcf-d017-4cba-bf14-dd9c7185f6be"
send_auth = "4ffbd256-8e0d-43f2-a0f5-11be9640c98c"
tenantId = "pb"

def main():
    auth_token = superuser_login()["access_token"]
    modules = ["rainmaker-common","rainmaker-ws","rainmaker-pt","rainmaker-pdf","rainmaker-commonpay"]
    # modules = ["rainmaker-common"]
    locales = ["en_IN","hi_IN"]
    # locales = ["en_IN"]
    for module in modules:
        for locale in locales:
            data = search_localization(recv_auth,module,locale)["messages"]   
            with io.open(os.path.join(r"D:\Temp","localization.json"), mode="w", encoding="utf-8") as f:
                json.dump(data, f, indent=2,  ensure_ascii=False, cls=DateTimeEncoder)         
            upsert_localization(send_auth, data)
    print("Migration Completed")



def search_localization(auth_token, module_name, locale):
    url = urljoin(recv_host, '/localization/messages/v1/_search')
    request_body = {}
    request_body["RequestInfo"] = {"authToken": auth_token}
    params = {"tenantId": tenantId, "module": module_name, "locale": locale}
    return requests.post(url, params=params, json=request_body).json()



def upsert_localization(auth_token, data):
    body = {  
        "RequestInfo": {
            "authToken": "{{access_token}}"
        },          
        "tenantId": tenantId,
        "messages": data
    }

    body["RequestInfo"]["authToken"] = auth_token
    
    requests.post(url=send_host + '/localization/messages/v1/_upsert', json=body)



if __name__ == "__main__":
    main()
