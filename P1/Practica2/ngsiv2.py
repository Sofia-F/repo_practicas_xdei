import requests
import json
import base64
import math

def create_entity(entity):
    url = "http://localhost:1026/v2/entities/"
    payload = json.dumps(entity)
    print(payload)
    print(type(payload))
    headers = {'Content-Type': 'application/json'}
    response = requests.request("POST", url, headers=headers, data=payload)
    print(response)
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
    print(payload)
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

def b64(data):        
    with open(data, 'rb') as file:
        img = file.read()

    enc_data_wo_pad = base64.b64encode(img).decode('utf-8').rstrip('=')
    return enc_data_wo_pad

def register_weather_provider(id):
    url = "http://localhost:1026/v2/registrations"

    payload = json.dumps({
    "description": "Get Weather data for Store",
    "dataProvided": {
        "entities": [
        {
            "id": id,
            "type": "Store"
        }
        ],
        "attrs": [
        "temperature",
        "relativeHumidity"
        ]
    },
    "provider": {
        "http": {
        "url": "http://context-provider:3000/random/weatherConditions"
        },
        "legacyForwarding": False
    },
    "status": "active"
    })
    headers = {
    'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    return response.status_code, response.text

if __name__ == "__main__":

    # Inputs
    employees = [
    {
        "id": "urn:ngsi-ld:Employee:001",
        "type": "Employee",
        "name": { "type": "Text", "value": "Sofia" },
        "email": { "type": "Text", "value": "sofia.employee@gmail.com" },
        "dateOfContract": { "type": "Date", "value": "2019-07-15T00:00:00Z" },
        "category": { "type": "Text", "value": "Manager" },
        "salary": { "type": "Float", "value": 2800 },
        "skills": { "type": "Text", "value": "CustomerRelationships" },
        "username": { "type": "Text", "value": "SofiaM" },
        "password": { "type": "Text", "value": "sofiamanager" },
        "refStore": { "type": "Relationship", "value": "urn:ngsi-ld:Store:001"},
        "image": {"type": "Image", "value": b64("empleado.jpg")},
    },
    {
        "id": "urn:ngsi-ld:Employee:002",
        "type": "Employee",
        "name": { "type": "Text", "value": "Diego" },
        "email": { "type": "Text", "value": "diego.employee@gmail.com" },
        "dateOfContract": { "type": "Date", "value": "2020-02-20T00:00:00Z" },
        "category": { "type": "Text", "value": "Regular" },
        "salary": { "type": "Float", "value": 3200 },
        "skills": { "type": "Text", "value": "WritingReports" },
        "username": { "type": "Text", "value": "DiegoR" },
        "password": { "type": "Text", "value": "diegoregular" },
        "refStore": { "type": "Relationship", "value": "urn:ngsi-ld:Store:002"},
        "image": {"type": "Image", "value": b64("empleado.jpg")}
    },
    {
        "id": "urn:ngsi-ld:Employee:003",
        "type": "Employee",
        "name": { "type": "Text", "value": "Elena" },
        "email": { "type": "Text", "value": "elena.employee@gmail.com" },
        "dateOfContract": { "type": "Date", "value": "2018-11-10T00:00:00Z" },
        "category": { "type": "Text", "value": "Intern" },
        "salary": { "type": "Float", "value": 2500 },
        "skills": { "type": "Text", "value": "MachineryDriving" },
        "username": { "type": "Text", "value": "ElenaI" },
        "password": { "type": "Text", "value": "elenaintern" },
        "refStore": { "type": "Relationship", "value": "urn:ngsi-ld:Store:003"},
        "image": {"type": "Image", "value": b64("empleado.jpg")},
    }
    ]

    stores = [
    {
        "id": "urn:ngsi-ld:Store:001",
        "type": "Store",
        "name": {"type": "Text", "value": "Store 1"},
        "address": {"type": "Text", "value": "Calle de Alcala, Spain"},
        "image": {"type": "Image", "value": b64("store1.jpg")},
        "url": {"type": "Text", "value": "https://store1.com"},
        "telephone": {"type": "Text", "value": "913456789"},
        "countryCode": {"type": "Text", "value": "34"},
        "capacity": {"type": "Number", "value": 600},
        "address": {"type": "Text", "value": "Madrid"},
        "location": {"type": "geo:json", "value": {"type": "Point", "coordinates": [-3.7038, 40.4168]}},
        "description": {"type": "Text", "value": "Store number 1"}
    },
    {
        "id": "urn:ngsi-ld:Store:002",
        "type": "Store",
        "name": {"type": "Text", "value": "Store 2"},
        "address": {"type": "Text", "value": "Carrer de Balmes, Spain"},
        "image": {"type": "Image", "value": b64("store1.jpg")},
        "url": {"type": "Text", "value": "https://store2.com"},
        "telephone": {"type": "Text", "value": "917654321"},
        "countryCode": {"type": "Text", "value": "34"},
        "capacity": {"type": "Number", "value": 450},
        "address": {"type": "Text", "value": "Barcelona"},
        "location": {"type": "geo:json", "value": {"type": "Point", "coordinates": [2.1540, 41.3902]}},
        "description": {"type": "Text", "value": "Store number 2"},
    },
    {
        "id": "urn:ngsi-ld:Store:003",
        "type": "Store",
        "name": {"type": "Text", "value": "Store 3"},
        "address": {"type": "Text", "value": "Avenida de la Constitución, Spain"},
        "image": {"type": "Image", "value": b64("store1.jpg")},
        "url": {"type": "Text", "value": "https://store3.com"},
        "telephone": {"type": "Text", "value": "910987654"},
        "countryCode": {"type": "Text", "value": "34"},
        "capacity": {"type": "Number", "value": 700},
        "address": {"type": "Text", "value": "Valencia"},
        "location": {"type": "geo:json", "value": {"type": "Point", "coordinates": [-0.375, 39.4699]}},
        "description": {"type": "Text", "value": "Store number 3"}
    }
    ]

    products = [
    {
        "id": "urn:ngsi-ld:Product:001",
        "type": "Product",
        "name": {"type": "Text", "value": "Pizza"},
        "image": {"type": "Image", "value": b64('product1.jpg')},
        "color": {"type": "Text", "value": "Brown"},
        "size": {"type": "Text", "value": "Large"},
        "price": {"type": "Number", "value": 10.99}
    },
    {
        "id": "urn:ngsi-ld:Product:002",
        "type": "Product",
        "name": {"type": "Text", "value": "Burger"},
        "image": {"type": "Image", "value": b64('product1.jpg')},
        "color": {"type": "Text", "value": "Yellow"},
        "size": {"type": "Text", "value": "Medium"},
        "price": {"type": "Number", "value": 8.99}
    },
    {
        "id": "urn:ngsi-ld:Product:003",
        "type": "Product",
        "name": {"type": "Text", "value": "Sushi"},
        "image": {"type": "Image", "value": b64("product1.jpg")},
        "color": {"type": "Text", "value": "White"},
        "size": {"type": "Text", "value": "Small"},
        "price": {"type": "Number", "value": 12.99}
    },
    {
        "id": "urn:ngsi-ld:Product:004",
        "type": "Product",
        "name": {"type": "Text", "value": "Salad"},
        "image": {"type": "Image", "value": b64("product1.jpg")},
        "color": {"type": "Text", "value": "Green"},
        "size": {"type": "Text", "value": "Medium"},
        "price": {"type": "Number", "value": 7.99}
    },
    {
        "id": "urn:ngsi-ld:Product:005",
        "type": "Product",
        "name": {"type": "Text", "value": "Pasta"},
        "image": {"type": "Image", "value": b64("product1.jpg")},
        "color": {"type": "Text", "value": "Yellow"},
        "size": {"type": "Text", "value": "Large"},
        "price": {"type": "Number", "value": 9.99}
    },
    {
        "id": "urn:ngsi-ld:Product:006",
        "type": "Product",
        "name": {"type": "Text", "value": "Ice Cream"},
        "image": {"type": "Image", "value": b64("product1.jpg")},
        "color": {"type": "Text", "value": "Various"},
        "size": {"type": "Text", "value": "Small"},
        "price": {"type": "Number", "value": 5.99}
    },
    {
        "id": "urn:ngsi-ld:Product:007",
        "type": "Product",
        "name": {"type": "Text", "value": "Sushi Roll"},
        "image": {"type": "Image", "value": b64("product1.jpg")},
        "color": {"type": "Text", "value": "Various"},
        "size": {"type": "Text", "value": "Medium"},
        "price": {"type": "Number", "value": 11.99}
    }
    ]

    inventory_items = [
    {
        "id": "urn:ngsi-ld:InventoryItem:001",
        "type": "InventoryItem",
        "refProduct": {"type": "Relationship", "value": "urn:ngsi-ld:Product:001"},
        "refShelf": {"type": "Relationship", "value": "urn:ngsi-ld:Shelf:001"},
        "refStore": {"type": "Relationship", "value": "urn:ngsi-ld:Store:001"},
        "shelfCount": {"type": "Number", "value": 50},
        "stockCount": {"type": "Number", "value": 500}
    }
    ]

    shelfs = [
    {
        "id": "urn:ngsi-ld:Shelf:001",
        "type": "Shelf",
        "location": {"type": "geo:json", "value": {"type": "Point", "coordinates": [-0.375, 39.4699]}},
        "refStore": {"type": "Relationship", "value": "urn:ngsi-ld:Store:001"},
        "maxCapacity": {"type": "Number", "value": 50},
        "name": {"type": "Text", "value": "Corner Unit"}
    }
    ]

    print("Deleting Products entities...")
    for i in range(9):
        status = delete_entity("urn:ngsi-ld:Product:00"+str(i+1))
        print(status)

    print()
    print("Deleting Stores entities...")
    for i in range(4):
        print("urn:ngsi-ld:Store:00" + str(i+1))
        status = delete_entity("urn:ngsi-ld:Store:00" + str(i+1))
        print(status)

    print()
    print("Deleting Shelf entities...")
    for i in range(4):
        print("urn:ngsi-ld:Shelf:00" + str(i+1))
        status = delete_entity("urn:ngsi-ld:Shelf:00" + str(i+1))
        print(status)

    print()
    print("Deleting InventoryItem entities...")
    for i in range(4):
        print("urn:ngsi-ld:InventoryItem:00" + str(i+1))
        status = delete_entity("urn:ngsi-ld:InventoryItem:00" + str(i+1))
        print(status)

    print()
    print("Creating employees entities...")
    for employee in employees:
        print(employee)
        status = create_entity(employee)
        print(status)
        status, val = read_entity(str(employee["id"]))
        print(status, " ", val)

    print()
    print("Creating stores entities...")
    for store in stores:
        status = register_weather_provider(str(store["id"]))
        print(status)
        status = create_entity(store)
        print(status)
        status, val = read_entity(str(store["id"]))
        print(status, " ", val)
    
    print()
    print("Creating products entities...")
    for product in products:
        status = create_entity(product)
        print(status)
        status, val = read_entity(product["id"])
        print(status, " ", val)
    print()
    print("Completed")
