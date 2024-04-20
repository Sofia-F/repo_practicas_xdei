import requests 
import json

def switch_off_lamp(id):
    url = "http://localhost:1026/v2/entities/urn:ngsi-ld:"+ id + "/attrs?type=Lamp"

    payload = json.dumps({
    "off": {
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

def lock_door(id):
    url = "http://localhost:1026/v2/entities/urn:ngsi-ld:"+id+"/attrs?type=Door"

    payload = json.dumps({
    "lock": {
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

# Cierra las puertas y apaga las lámparas
def stop_devices():
    url = "http://localhost:4041/iot/devices"

    payload = ""
    headers = {
    'fiware-service': 'openiot',
    'fiware-servicepath': '/'
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    return(response.json())

if __name__ == "__main__":

    devices = stop_devices()

    print(devices)

