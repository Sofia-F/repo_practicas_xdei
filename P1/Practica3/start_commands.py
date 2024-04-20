import requests 
import json

def switch_on_lamp(id):
    url = "http://localhost:4041/v2/op/update"+ id + "/attrs?type=Lamp"

    payload = json.dumps({
    "on": {
        "type": "command",
        "value": ""
    }

    })
    headers = {
    'fiware-service': 'openiot',
    'fiware-servicepath': '/',
    'Content-Type': 'application/json'
    }

    response = requests.request("PATCH", url, headers=headers, data=payload)

    return response.status_code

def unlock_door(id):
    url = "http://localhost:1026/v2/entities/urn:ngsi-ld:"+id+"/attrs?type=Door"

    payload = json.dumps({
    "open": {
        "type": "command",
        "value": ""
    }
    })
    headers = {
    'fiware-service': 'openiot',
    'fiware-servicepath': '/',
    'Content-Type': 'application/json'
    }

    response = requests.request("PATCH", url, headers=headers, data=payload)

    return response.status_code

def start_devices():
    url = "http://localhost:4041/iot/devices"

    payload = ""
    headers = {
    'fiware-service': 'openiot',
    'fiware-servicepath': '/'
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    for device in response.json()["devices"]:
        if device["entity_type"] == "Door":
            print(device)
            status = unlock_door(device["entity_name"])
            print(print(device["entity_name"]), " status: ", status)
            
            print(device["entity_type"])
        
        if device["entity_type"] == "Lamp":
            print(device)
            status = switch_on_lamp(device["entity_name"])
            print(print(device["entity_name"]), " status: ", status)


    return response.status_code

if __name__ == "__main__":

    devices = start_devices()
    print(devices)
