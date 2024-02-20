import requests
import json

# POST - create_entity - Fuction to create a new entity.
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

# DELETE - delete_attr(id, attr)
def delete_attr(id, attr):
    url = "http://localhost:1026/v2/entities/" + id + "/attrs/" + attr
    response = requests.request("DELETE", url)
    return response.status_code

def update_attrs(id, attrs_vals):
    url = "http://localhost:1026/v2/entities/"+ id + "/attrs/" 
    payload = json.dumps(attrs_vals)
    headers = {'Content-Type': 'application/json'}
    response = requests.request("PATCH", url, headers=headers, data=payload)
    return (response.status_code, response.text)

# PUT - update_attr
def update_attr(id, attr, val):
    url = "http://localhost:1026/v2/entities/"+id+"/attrs/"+attr+"/value"

    payload = val
    headers = {'Content-Type': 'text/plain'}
    response = requests.request("PUT", url, headers=headers, data=payload)
    print(response.status_code, response.text)

# GET - list_entities
# def list_entities(type):
#     url = "http://localhost:1026/v2/entities/?type="+type
#     response = requests.request("GET", url)

#     return (response.status_code, response.text)


def list_entities(type = None,options = 'count', attrs = None):
    url = "http://localhost:1026/v2/entities/"

    response = requests.request("GET", url)
    print(response.status_code, response.text)


if __name__ == "__main__":

    # Inputs
    entity = {
        "id":"urn:ngsi-ld:Supplier:001", "type":"Supplier",
        "name":{"type":"Text", "value":"Alfonso"}
    }

    entity2 = {
        "id":"urn:ngsi-ld:Supplier:002", "type":"Supplier",
        "name":{"type":"Text", "value":"Sofia"}
    }

    attrs_vals = {"name": {
                        "type": "Integer",
                        "value": 89
                    }}

    id = "urn:ngsi-ld:Supplier:001"
    id2 = "urn:ngsi-ld:Supplier:002"
    attr = "name"

    # Create an entity
    status = create_entity(entity2)
    status = create_entity(entity)
    print(status)

    # Read an entity
    status, val = read_entity(id)
    print(status, " ", val)

    # Read entities
    status, val = list_entities(type = "Supplier")
    print(status, " ", val)

    # Update an attribute
    status, val = update_attr(id, attr, val = "Alogon")
    print(val)

    # Update attributes
    # status, val = update_attrs(id, attrs_vals)
    # print(status)

    # Read an attribute
    status, val = read_attr(id, attr)
    status, val = read_entity(id)
    print(status, " ", val)

    # Delete an attribute
    status = delete_attr(id, attr)
    print(status)

    # Delete an entity
    status = delete_entity(id2)
    status = delete_entity(id)
    print(status)
