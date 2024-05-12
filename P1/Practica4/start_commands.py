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

    tractors = ["tractor001", "tractor002", "tractor003", "tractor004"]
    fillings = ["filling001", "filling002", "filling003", "filling004"]
    temperatures = ["temperature001", "temperature002", "temperature003", "temperature004"]

    for tractor in tractors:
        status = start_tractor(tractor)
        print("tractor:", status)
    
    for filling in fillings:
        if filling[-3:] in ["001", "002", "003"]:
            status = remove_hay(filling)
            print("filling:", status)
        else: 
            status = add_hay(filling)
            print("filling:", status)

    for temperature in temperatures:
        if temperature[-3:] in ["001", "002", "003"]:
            status = raise_temperature(temperature)
            print("temperature:", status)
        else: 
            status = lower_temperature(temperature)
            print("temperature:", status)

