import requests 

def switch_on_lamp(id):
    url = "http://localhost:3001/iot/"+id
    payload = "urn:ngsi-ld:" + id + "@on"
    
    headers = {
        'Content-Type': 'text/plain'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    return response.status_code

def unlock_door(id):
    url = "http://localhost:3001/iot/"+id
    payload = "urn:ngsi-ld:" + id + "@open"
    
    headers = {
        'Content-Type': 'text/plain'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

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
            status = unlock_door(device["device_id"])
        
        if device["entity_type"] == "Lamp":
            status = switch_on_lamp(device["device_id"])


    return response.status_code

if __name__ == "__main__":

    devices = start_devices()
    print(devices)
