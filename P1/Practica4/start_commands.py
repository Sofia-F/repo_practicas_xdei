import requests 

def start_tractor(id):
    url = "http://localhost:3001/iot/"+id
    payload = "urn:ngsi-ld:" + id + "@start"
    
    headers = {
        'Content-Type': 'text/plain'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    return response.status_code

def add_hay(id):
    url = "http://localhost:3001/iot/"+id
    payload = "urn:ngsi-ld:" + id + "@add"
    
    headers = {
        'Content-Type': 'text/plain'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    return response.status_code

def remove_hay(id):
    url = "http://localhost:3001/iot/"+id
    payload = "urn:ngsi-ld:" + id + "@remove"
    
    headers = {
        'Content-Type': 'text/plain'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    return response.status_code

def raise_temperature(id):
    url = "http://localhost:3001/iot/"+id
    payload = "urn:ngsi-ld:" + id + "@raise"
    
    headers = {
        'Content-Type': 'text/plain'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    return response.status_code

def lower_temperature(id):
    url = "http://localhost:3001/iot/"+id
    payload = "urn:ngsi-ld:" + id + "@lower"
    
    headers = {
        'Content-Type': 'text/plain'
    }
    response = requests.request("POST", url, headers=headers, data=payload)

    return response.status_code

if __name__ == "__main__":

    url = "http://localhost:4041/iot/devices"

    payload = ""
    headers = {
    'fiware-service': 'openiot',
    'fiware-servicepath': '/'
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    devices = response.json()["devices"]

    for device in devices:

        if device["entity_type"] == "Tractor":
            status = start_tractor(device["device_id"])
            print("tractor: ", status)
        
        if device["entity_type"] == "FillingLevelSensor":
            if device["device_id"][-3:] in ["001", "002", "003"]:
                status = remove_hay(device["device_id"])
                print("filling: ", status)
            else: 
                status = add_hay(device["device_id"])
                print("filling", status)

        if device["entity_type"] == "TemperatureSensor":
            if device["device_id"][-3:] in ["001", "002", "003"]:
                status = raise_temperature(device["device_id"])
                print("temperature", status)
            else: 
                status = lower_temperature(device["device_id"])
                print("temperature", status)

