import requests
import json

# Fuction to create a new entity.
def create_entity(entity):
    url = "http://localhost:1026/v2/entities/"

    payload = json.dumps(entity)
    headers = {'Content-Type': 'application/json'}
    response = requests.request("POST", url, headers=headers, data=payload)
    print(response.text)

# Function to delete an entity.
def delete_entity(id):
    url = "http://localhost:1026/v2/entities/" + id
    response = requests.request("DELETE", url)
    print(response.text)

# Function to read a new entity.
def read_entity(id):
    url = "http://localhost:1026/v2/entities/" + id
    response = requests.request("GET", url)
    print(response.text)

def read_attr(id, attr):
    url = "http://localhost:1026/v2/entities/"+ id + "/attrs/" + attr + "/value"
    response = requests.request("GET", url)
    print(response.text)

def delete_attr(id, attr):
    url = "http://localhost:1026/v2/entities/" + id + "/attrs/" + attr
    response = requests.request("DELETE", url)
    print(response.text)

def update_attrs(id, attrs_vals):
    url = "http://localhost:1026/v2/op/update"

    headers = {
    'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    print(response.text)

entity = {
      "id":"urn:ngsi-ld:Supplier:001", "type":"Supplier",
      "name":{"type":"Text", "value":"Alogon"}
}
id = "urn:ngsi-ld:Supplier:001"
attr = "name"

create_entity(entity)
read_entity(id)
read_attr(id, attr)
delete_attr(id, attr)
delete_entity(id)
