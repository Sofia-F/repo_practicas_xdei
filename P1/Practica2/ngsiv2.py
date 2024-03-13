import requests
import json

def create_entity(entity):
    url = "http://localhost:1026/v2/entities/"
    payload = json.dumps(entity)
    headers = {'Content-Type': 'application/json'}
    response = requests.request("POST", url, headers=headers, data=payload)
    return response.status_code

def delete_entity(id):
    url = "http://localhost:1026/v2/entities/" + id
    response = requests.request("DELETE", url)
    return response.status_code

def read_entity(id):
    url = "http://localhost:1026/v2/entities/" + id
    response = requests.request("GET", url)
    return (response.status_code, response.json())

def read_attr(id, attr):
    url = "http://localhost:1026/v2/entities/"+ id + "/attrs/" + attr + "/value"
    response = requests.request("GET", url)
    return (response.status_code, response.json())

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
    return response.status_code

# PUT - update_attr
def update_attr(id, attr, val):
    url = "http://localhost:1026/v2/entities/"+id+"/attrs/"+attr+"/value"
    payload = json.dumps(val)
    headers = {
    'Content-Type': 'text/plain'
    }
    response = requests.request("PUT", url, headers=headers, data=payload)
    print(response.text)
    return response.status_code

def list_entities(type = None, options = 'count', attrs = None):
    url = "http://localhost:1026/v2/entities/"
    if type != None:
        url = url + "?type="+str(type)
    if options != None:
        url = url + "&options=" + str(options)
    if attrs != None:
        url = url + "&attrs=" + ",".join(attrs)

    response = requests.request("GET", url)
    return response.status_code, response.json()

if __name__ == "__main__":

    # Inputs
    entity1 = {
        "id":"urn:ngsi-ld:Employee:001",
        "type":"Employee",
        "name":{"type":"Text", "value":"Jonh"},
        "email":{"type":"Text", "value":"jonh.manager@gmail.com"},
        "dateOfContract":{"type":"Date", "value":"2014-03-01T00:00:00Z"},
        "category":{"type":"Text", "value":"Manager"},
        "salary":{"type":"Float", "value":"3000"},
        "skills":{"type":"Text", "value":"WritingReports"},
        "username":{"type":"Text", "value":"Smith"},
        "password":{"type":"Text", "value":"jonh$smith"}
    }

    id = "urn:ngsi-ld:Employee:001"

#     id1 = "urn:ngsi-ld:Store:001"


#     attrs_Store1 = { "image": {"type": "Image",
#                            "value": "store1.jpg"},
#                     "url": {"type": "Text",
#                            "value": "https:store1.com"},
#                     "telephone": {"type": "Text",
#                            "value": "981065890"},
#                     "countryCode": {"type": "Text",
#                            "value": "49"},
#                     "capacity": {"type": "Number",
#                            "value": 500},
#                     "Description": {"type": "Text",
#                            "value": "Store number 1"},
#                     "temperature": {"type": "Numer",
#                            "value": 21.5},
#                     "relativeHumidity": {"type": "Number",
#                            "value": 20}}
    
    
#     id5 = "urn:ngsi-ld:Product:001"
#     attrs_Product1 = {"image": {"type": "Image",
#                            "value":"product1.jpg"},
#                       "color": {"type": "Text",
#                            "value": "Red"}}


    # Create an entity
    status = create_entity(entity1)
    print(status)
    status, val = read_entity(id)
    print(status, " ", val)

#     # Read entities
#     status, val = list_entities(type = "Supplier", options="values", attrs=["id","name"])
#     print(status, " ", val)

#     # Update attributes
#     status = update_attrs(id5, attrs_Product1)
#     print(status)
#     status = update_attrs(id1, attrs_Store1)
#     print(status)

#     status, val = read_entity(id5)
#     print(status, " ", val)

#     status, val = read_entity(id1)
#     print(status, " ", val)
