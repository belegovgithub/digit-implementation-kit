from common import *
from config import config
from common import superuser_login
import io
import os
import numpy

recv_host = "https://13.71.65.215.nip.io"
#send_host = "https://demo.echhawani.gov.in"
send_host = "https://echhawani.gov.in"
recv_auth = "ba459cd4-0666-4c28-8b8e-212ecbaa2dbe"
#send_auth = "af247018-87d2-4d61-808f-2ba31d951f2f"
send_auth = "97dfc6ee-11dd-4969-b06c-da348311d693"
tenantId = "pb"

def main():
    auth_token = superuser_login()["access_token"]
    modules = ["rainmaker-pt","rainmaker-common","rainmaker-ws","rainmaker-pdf"]
    # modules = ["rainmaker-common"]
    locales = ["en_IN","hi_IN"]
    #locales = ["en_IN"]
    for module in modules:
        for locale in locales:
            data = search_localization(recv_auth,module,locale)["messages"]   
            # with io.open(os.path.join(r"D:\Temp",locale+"localization.json"), mode="w", encoding="utf-8") as f:
            #     json.dump(data, f, indent=2,  ensure_ascii=False, cls=DateTimeEncoder)         
            localize_response = upsert_localization(send_auth, data)
            print(module, " ", locale)
            if(not (localize_response.status_code == 200 or localize_response.status_code == 201)):
                print(localize_response.json())
                print("Upsert Failed") 
                return



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

    # print(body)
    body["RequestInfo"]["authToken"] = auth_token    
    return requests.post(url=send_host + '/localization/messages/v1/_upsert', json=body)



if __name__ == "__main__":
    main()
