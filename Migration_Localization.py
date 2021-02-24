from common import *
from config import config
from common import superuser_login
import io
import os
import numpy

recv_host = "https://13.71.65.215.nip.io"
#send_host = "https://demo.echhawani.gov.in"
send_host = "https://echhawani.gov.in"
recv_auth = "f5e4ba53-3d15-46f4-8bd5-09d74b34406a"
#send_auth = "8b5bcc37-bdc5-47bd-a47f-0a879b4333b8"
send_auth = "247a0a8c-d58e-4610-b4cb-3a8b9a28cc0d"
tenantId = "pb"

def main():
    auth_token = superuser_login()["access_token"]
    modules = ["rainmaker-common","rainmaker-ws","rainmaker-pt"]
    # modules = ["rainmaker-common"]
    locales = ["en_IN","hi_IN"]
    # locales = ["en_IN"]
    for module in modules:
        for locale in locales:
            data = search_localization(recv_auth,module,locale)["messages"]   
            # with io.open(os.path.join(r"D:\Temp","localization.json"), mode="w", encoding="utf-8") as f:
            #     json.dump(data, f, indent=2,  ensure_ascii=False, cls=DateTimeEncoder)         
            upsert_localization(send_auth, data)
            print(module, " ", locale)



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
