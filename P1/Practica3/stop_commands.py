import requests 

def switch_off_lamp(id):
    url = f"http://localhost:3001/iot/"+id
    payload = "urn:ngsi-ld:" + id + "@off"
    
    headers = {
        'Content-Type': 'text/plain'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    return response.status_code

def lock_door(id):
    url = "http://localhost:3001/iot/"+id
    payload = "urn:ngsi-ld:" + id + "@lock"
    
    headers = {
        'Content-Type': 'text/plain'
    }

    headers = {
        'Content-Type': 'text/plain'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    return response.status_code

def stop_devices():
    url = "http://localhost:4041/iot/devices"

    payload = ""
    headers = {
    'fiware-service': 'openiot',
    'fiware-servicepath': '/'
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    for device in response.json()["devices"]:

        if device["entity_type"] == "Door":
            status = lock_door(device["device_id"])
        
        if device["entity_type"] == "Lamp":
            status = switch_off_lamp(device["device_id"])


    return response.status_code

if __name__ == "__main__":

    devices = stop_devices()

    print(devices)

