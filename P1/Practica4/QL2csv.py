import requests
import pandas as pd

def read_api(id, attr, limit, last):
    url = "http://localhost:8668/v2/entities/urn:ngsi-ld:Device:"+id+"/attrs/"+attr

    if limit != None:
        url = url +"?limit="+str(limit)
    
    if last != None:
        url = url +"?lastN="+str(last)

    payload = ""
    headers = {
    'Accept': 'application/json',
    'Fiware-Service': 'openiot',
    'Fiware-ServicePath': '/'
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    return response

response = read_api("cow001", "heartrate", limit = 3, last = None)
print(response.status_code)
print(response.json())

df = pd.DataFrame(response.json())
print(df)