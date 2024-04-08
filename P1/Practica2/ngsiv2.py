import requests
import json
import base64
import math

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
    return response.status_code

def list_entities(type = None, options = 'count', attrs = None, filter = None):
    url = "http://localhost:1026/v2/entities/"
    if type != None:
        url = url + "?type="+str(type)
    if  filter != None:
        url = url + "&q="+filter
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

def register_tweet_provider(id):
    url = "http://localhost:1026/v2/registrations"

    payload = json.dumps({
    "description": "Get Tweets for Store",
    "dataProvided": {
        "entities": [
        {
            "id": id,
            "type": "Store"
        }
        ],
        "attrs": [
        "tweets"
        ]
    },
    "provider": {
        "http": {
        "url": "http://context-provider:3000/catfacts/tweets"
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

def register_shelfSubscription(id):
    url = "http://localhost:1026/v2/subscriptions"

    payload = json.dumps({
    "description": "Notify me of all product price changes",
    "subject": { "entities": [{"idPattern": ".*", "type": "InventoryItem"}],
                 "condition": {"attrs": ["shelfCount"],
                             "expression": {"q": "shelfCount<10;refStore=="+id}}
    },
    "notification": {
    "http": { "url": "http://host.docker.internal:5000/alertas/" } }
    })

    headers = {
    'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    return response.status_code

def register_priceSubscription():
    url = "http://localhost:1026/v2/subscriptions"

    payload = json.dumps({
    "description": "Notify me of all product price changes",
    "subject": {"entities": [{"idPattern": ".*", "type": "Product"}],
                "condition": {"attrs": [ "price" ]}
    },
    "notification": {
        "http": {"url": "http://host.docker.internal:3000:3000/subscription/price-change"}
    }})

    headers = {
    'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    return response.status_code

def delete_context_provider(id):
    url = "http://localhost:1026/v2/registrations"

    response = requests.request("GET", url)
    registrations = response.json()

    for registration in registrations:
        print(registration["dataProvided"]["entities"][0]["id"])
        if registration["dataProvided"]["entities"][0]["id"] == id:
            url = "http://localhost:1026/v2/registrations/"+registration["id"]
            response = requests.request("DELETE", url)

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
        "image": {"type": "Image", "value": b64("images/employees/employee1.jpg")},
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
        "image": {"type": "Image", "value": b64("images/employees/employee2.jpg")}
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
        "image": {"type": "Image", "value": b64("images/employees/employee3.jpg")},
    }
    ]

    stores = [
    {
        "id": "urn:ngsi-ld:Store:001",
        "type": "Store",
        "name": {"type": "Text", "value": "Store 1"},
        "address": {"type": "Text", "value": "Unter den Linden, Germany"},
        "image": {"type": "Text", "value": b64("images/stores/store1.jpg")},
        "url": {"type": "Text", "value": "https://store1.com"},
        "telephone": {"type": "Text", "value": "913456789"},
        "countryCode": {"type": "Text", "value": "GE"},
        "capacity": {"type": "Number", "value": 600},
        "location": {"type": "geo:json", "value": {"type": "Point", "coordinates": [52.5133, 13.4233]}},
        "description": {"type": "Text", "value": "Store number 1"}
    },
    {
        "id": "urn:ngsi-ld:Store:002",
        "type": "Store",
        "name": {"type": "Text", "value": "Store 2"},
        "address": {"type": "Text", "value": "Marienplatz, Germany"},
        "image": {"type": "Text", "value": b64("images/stores/store2.jpg")},
        "url": {"type": "Text", "value": "https://store2.com"},
        "telephone": {"type": "Text", "value": "917654321"},
        "countryCode": {"type": "Text", "value": "GE"},
        "capacity": {"type": "Number", "value": 450},
        "location": {"type": "geo:json", "value": {"type": "Point", "coordinates": [52.5333, 13.4033]}},
        "description": {"type": "Text", "value": "Store number 2"},
    },
    {
        "id": "urn:ngsi-ld:Store:003",
        "type": "Store",
        "name": {"type": "Text", "value": "Store 3"},
        "address": {"type": "Text", "value": "Brandenburger Tor, Germany"},
        "image": {"type": "Text", "value": b64("images/stores/store3.jpg")},
        "url": {"type": "Text", "value": "https://store3.com"},
        "telephone": {"type": "Text", "value": "910987654"},
        "countryCode": {"type": "Text", "value": "GE"},
        "capacity": {"type": "Number", "value": 700},
        "location": {"type": "geo:json", "value": {"type": "Point", "coordinates": [52.5343, 13.4033]}},
        "description": {"type": "Text", "value": "Store number 3"}
    }
    ]

    products = [
    {
        "id": "urn:ngsi-ld:Product:001",
        "type": "Product",
        "name": {"type": "Text", "value": "Orange"},
        "image": {"type": "Image", "value": b64('images/products/product1.jpg')},
        "color": {"type": "Text", "value": "#FF8000"},
        "size": {"type": "Text", "value": "Medium"},
        "price": {"type": "Number", "value": 3.99}
    },
    {
        "id": "urn:ngsi-ld:Product:002",
        "type": "Product",
        "name": {"type": "Text", "value": "Banana"},
        "image": {"type": "Image", "value": b64('images/products/product2.jpg')},
        "color": {"type": "Text", "value": "#FFD300"},
        "size": {"type": "Text", "value": "Medium"},
        "price": {"type": "Number", "value": 3.99}
    },
    {
        "id": "urn:ngsi-ld:Product:003",
        "type": "Product",
        "name": {"type": "Text", "value": "Lettuce"},
        "image": {"type": "Image", "value": b64("images/products/product3.jpg")},
        "color": {"type": "Text", "value": "#008000"},
        "size": {"type": "Text", "value": "Medium"},
        "price": {"type": "Number", "value": 6.99}
    },
    {
        "id": "urn:ngsi-ld:Product:004",
        "type": "Product",
        "name": {"type": "Text", "value": "Tomato"},
        "image": {"type": "Image", "value": b64("images/products/product4.jpg")},
        "color": {"type": "Text", "value": "#FF0000"},
        "size": {"type": "Text", "value": "Small"},
        "price": {"type": "Number", "value": 4.99}
    },
    {
        "id": "urn:ngsi-ld:Product:005",
        "type": "Product",
        "name": {"type": "Text", "value": "Eggs"},
        "image": {"type": "Image", "value": b64("images/products/product5.jpg")},
        "color": {"type": "Text", "value": "#FFEFAE"},
        "size": {"type": "Text", "value": "Large"},
        "price": {"type": "Number", "value": 5.99}
    },
    {
        "id": "urn:ngsi-ld:Product:006",
        "type": "Product",
        "name": {"type": "Text", "value": "Fish"},
        "image": {"type": "Image", "value": b64("images/products/product6.jpg")},
        "color": {"type": "Text", "value": "#0000FF"},
        "size": {"type": "Text", "value": "Small"},
        "price": {"type": "Number", "value": 10.99}
    },
    {
        "id": "urn:ngsi-ld:Product:007",
        "type": "Product",
        "name": {"type": "Text", "value": "Meat"},
        "image": {"type": "Image", "value": b64("images/products/product7.jpg")},
        "color": {"type": "Text", "value": "#FF0000"},
        "size": {"type": "Text", "value": "Medium"},
        "price": {"type": "Number", "value": 11.99}
    }
    ]

    inventory_items = [
    {
        "id": "urn:ngsi-ld:InventoryItem:001",
        "type": "InventoryItem",
        "refProduct": {"type": "Relationship", "value": "urn:ngsi-ld:Product:001"},
        "refShelf": {"type": "Relationship", "value": "urn:ngsi-ld:Shelf:unit001"},
        "refStore": {"type": "Relationship", "value": "urn:ngsi-ld:Store:001"},
        "shelfCount": {"type": "Number", "value": 11},
        "stockCount": {"type": "Number", "value": 11}
    },
    {
        "id": "urn:ngsi-ld:InventoryItem:002",
        "type": "InventoryItem",
        "refProduct": {"type": "Relationship", "value": "urn:ngsi-ld:Product:001"},
        "refShelf": {"type": "Relationship", "value": "urn:ngsi-ld:Shelf:unit002"},
        "refStore": {"type": "Relationship", "value": "urn:ngsi-ld:Store:001"},
        "shelfCount": {"type": "Number", "value": 70},
        "stockCount": {"type": "Number", "value": 500}
    },
    {
        "id": "urn:ngsi-ld:InventoryItem:003",
        "type": "InventoryItem",
        "refProduct": {"type": "Relationship", "value": "urn:ngsi-ld:Product:004"},
        "refShelf": {"type": "Relationship", "value": "urn:ngsi-ld:Shelf:unit003"},
        "refStore": {"type": "Relationship", "value": "urn:ngsi-ld:Store:002"},
        "shelfCount": {"type": "Number", "value": 30},
        "stockCount": {"type": "Number", "value": 500}
    },
    {
        "id": "urn:ngsi-ld:InventoryItem:004",
        "type": "InventoryItem",
        "refProduct": {"type": "Relationship", "value": "urn:ngsi-ld:Product:004"},
        "refShelf": {"type": "Relationship", "value": "urn:ngsi-ld:Shelf:unit004"},
        "refStore": {"type": "Relationship", "value": "urn:ngsi-ld:Store:002"},
        "shelfCount": {"type": "Number", "value": 70},
        "stockCount": {"type": "Number", "value": 500}
    },
    {
        "id": "urn:ngsi-ld:InventoryItem:005",
        "type": "InventoryItem",
        "refProduct": {"type": "Relationship", "value": "urn:ngsi-ld:Product:001"},
        "refShelf": {"type": "Relationship", "value": "urn:ngsi-ld:Shelf:unit005"},
        "refStore": {"type": "Relationship", "value": "urn:ngsi-ld:Store:003"},
        "shelfCount": {"type": "Number", "value": 70},
        "stockCount": {"type": "Number", "value": 500}
    },
    {
        "id": "urn:ngsi-ld:InventoryItem:006",
        "type": "InventoryItem",
        "refProduct": {"type": "Relationship", "value": "urn:ngsi-ld:Product:003"},
        "refShelf": {"type": "Relationship", "value": "urn:ngsi-ld:Shelf:unit002"},
        "refStore": {"type": "Relationship", "value": "urn:ngsi-ld:Store:001"},
        "shelfCount": {"type": "Number", "value": 70},
        "stockCount": {"type": "Number", "value": 500}
    }
    ]

    shelfs = [
    {
        "id": "urn:ngsi-ld:Shelf:unit001",
        "type": "Shelf",
        "location": {"type": "geo:json", "value": {"type": "Point", "coordinates": [-0.375, 39.4699]}},
        "refStore": {"type": "Relationship", "value": "urn:ngsi-ld:Store:001"},
        "maxCapacity": {"type": "Number", "value": 100},
        "name": {"type": "Text", "value": "Corner Unit"}
    },
    {
        "id": "urn:ngsi-ld:Shelf:unit002",
        "type": "Shelf",
        "location": {"type": "geo:json", "value": {"type": "Point", "coordinates": [-0.374, 39.4399]}},
        "refStore": {"type": "Relationship", "value": "urn:ngsi-ld:Store:001"},
        "maxCapacity": {"type": "Number", "value": 200},
        "name": {"type": "Text", "value": "Corner Unit"}
    },
    {
        "id": "urn:ngsi-ld:Shelf:unit003",
        "type": "Shelf",
        "location": {"type": "geo:json", "value": {"type": "Point", "coordinates": [-0.375, 39.4699]}},
        "refStore": {"type": "Relationship", "value": "urn:ngsi-ld:Store:002"},
        "maxCapacity": {"type": "Number", "value": 100},
        "name": {"type": "Text", "value": "Corner Unit"}
    },
    {
        "id": "urn:ngsi-ld:Shelf:unit004",
        "type": "Shelf",
        "location": {"type": "geo:json", "value": {"type": "Point", "coordinates": [-0.375, 39.4699]}},
        "refStore": {"type": "Relationship", "value": "urn:ngsi-ld:Store:002"},
        "maxCapacity": {"type": "Number", "value": 100},
        "name": {"type": "Text", "value": "Corner Unit"}
    },
    {
        "id": "urn:ngsi-ld:Shelf:unit005",
        "type": "Shelf",
        "location": {"type": "geo:json", "value": {"type": "Point", "coordinates": [-0.375, 39.4699]}},
        "refStore": {"type": "Relationship", "value": "urn:ngsi-ld:Store:003"},
        "maxCapacity": {"type": "Number", "value": 100},
        "name": {"type": "Text", "value": "Corner Unit"}
    }
    ]

    print(list_entities(type = "Shelf"))
    print("Deleting Products entities...")
    for i in range(9):
        status = delete_entity("urn:ngsi-ld:Product:00"+str(i+1))

    print()
    print("Deleting Stores entities...")
    for i in range(4):
        status = delete_entity("urn:ngsi-ld:Store:00" + str(i+1))


    print()
    print("Deleting Shelf entities...")
    list_shelfs = ["001", "002", "003", "004", "005", "006", "007", "008", "009", "010"]
    for i in list_shelfs:
        status = delete_entity("urn:ngsi-ld:Shelf:unit" + i)
    
    print()
    print("Creating Shelf entities...")
    for shelf in shelfs:
        status = create_entity(shelf)
        status, val = read_entity(str(shelf["id"]))


    print()
    print("Deleting InventoryItem entities...")
    lista_ids = ["001","002","003","004","005","006","007","008","401"]
    for i in lista_ids:
        status = delete_entity("urn:ngsi-ld:InventoryItem:"+i)
        print(status)

    print()
    print("Creating InventoryItem entities...")
    lista_ids = ["001","002","003","004","005","006","007","008","401"]
    for inventory in inventory_items:
        status = create_entity(inventory)
        status, val = read_entity(str(inventory["id"]))

    print()
    print("Creating employees entities...")
    for employee in employees:
        status = create_entity(employee)
        status, val = read_entity(str(employee["id"]))

    print()
    print("Creating stores entities...")
    for store in stores:
        status = register_weather_provider(str(store["id"]))
        status = register_tweet_provider(str(store["id"]))
        status = create_entity(store)
        status, val = read_entity(str(store["id"]))
        register_shelfSubscription(str(store["id"]))
    
    print()
    print("Creating products entities...")
    print(status)
    for product in products:
        status = create_entity(product)
        status, val = read_entity(product["id"])
    status4 = register_priceSubscription()
    print(status4)
    print()
    print("Completed")
