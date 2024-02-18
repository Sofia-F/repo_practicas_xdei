import requests
import json

# Fuction to create a new entity.
def create_entity(entity):
    url = "http://localhost:1026/v2/entities/"

    payload = json.dumps(entity)
    headers = {'Content-Type': 'application/json'}
    response = requests.request("POST", url, headers=headers, data=payload)
    return response.status_code

# Function to delete an entity.
def delete_entity(id):
    url = "http://localhost:1026/v2/entities/" + id
    response = requests.request("DELETE", url)
    return response.status_code

# Function to read a new entity.
def read_entity(id):
    url = "http://localhost:1026/v2/entities/" + id
    response = requests.request("GET", url)
    return (response.status_code, response.text)

def read_attr(id, attr):
    url = "http://localhost:1026/v2/entities/"+ id + "/attrs/" + attr + "/value"
    response = requests.request("GET", url)
    return (response.status_code, response.text)

def delete_attr(id, attr):
    url = "http://localhost:1026/v2/entities/" + id + "/attrs/" + attr
    response = requests.request("DELETE", url)
    return response.status_code

def update_attrs(id, attrs_vals):
    url = "http://localhost:1026/v2/op/update"

    headers = {
    'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    print(response.text)


if __name__ == "__main__":

    # Inputs
    entity = {
        "id":"urn:ngsi-ld:Supplier:001", "type":"Supplier",
        "name":{"type":"Text", "value":"Alogon"}
    }
    id = "urn:ngsi-ld:Supplier:001"
    attr = "name"

    # Create an entity
    status = create_entity(entity)
    print(status)

    # Read an entity
    status, val = read_entity(id)
    print(status, " ", val)

    # Read an attribute
    status, val = read_attr(id, attr)
    print(status, " ", val)

    # Delete an attribute
    status = delete_attr(id, attr)
    print(status)

    # Delete an entity
    status = delete_entity(id)
    print(status)
