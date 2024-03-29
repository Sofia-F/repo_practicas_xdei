import requests
import pprint
from datetime import datetime
from flask import render_template, request, redirect, url_for
import ngsiv2
from flask import Flask
import math
app = Flask(__name__)
import json

def get_weather_value(id, attr):
    url = "http://localhost:1026/v2/entities/"+ id + "/attrs/"+ attr +"/value"
    response = requests.request("GET", url)
    return response.status_code, response.json()

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/about/")
def about():
    return render_template("about.html")

@app.route('/employees/')
def employees():
 (status, employees) = ngsiv2.list_entities(type = 'Employee', options = 'keyValues')
#  print(status)
#  pprint.pprint(stores)
 if status == 200:
    return render_template('employees.html', employees = employees)
 
@app.route('/employees/<id>')
def employee(id):
 (status, employee) = ngsiv2.read_entity(id)
 print(employee)
 employee["image"]["value"] = employee["image"]["value"].ljust(math.ceil(len(employee["image"]["value"]) / 4) * 4, '=')
#  if status == 200:
#     (status, inventory_items) = ngsiv2.list_entities(type = 'InventoryItem',
#                                                     options = 'keyValues',
#                                                     attrs = None)
 return render_template('employee.html', employee = employee)

@app.route("/employee/create", methods=['GET', 'POST'])
def create_employee():
    if request.method == 'POST':
        print(request.form["id"])
        employee = {"id": request.form["id"],
                "type": "Product",
                "name": {"type": "Text", "value": request.form["name"]},
                "email": {"type": "Text", "value": request.form["email"]},      
                "dateOfContract": {"type": "Text", "value": request.form["dateOfContract"]},          
                "category": {"type": "Text", "value": request.form["category"]},
                "salary": {"type": "Integer", "value": int(request.form["salary"])},
                "skills": {"type": "Text", "value": request.form["skills"]},
                "username": {"type": "Text", "value": request.form["username"]},
                "password": {"type": "Text", "value": request.form["password"]},
                "refStore": {"type": "Relationship", "value": request.form["store"]}
                }
        status = ngsiv2.create_entity(employee)
        print(status)
        if status == 201:
            next = request.args.get('next', None)
            if next:
                return redirect(next)
            return redirect(url_for('employees'))
    else:
        return render_template('create_employee.html')

@app.route("/employee/update", methods=['GET', 'POST'])
def update_employee():
    if request.method == 'POST':
        print(request.form["id"])
        identifier = request.form["id"]
        attrs = {
                "name": {"type": "Text", "value": request.form["name"]},
                "email": {"type": "Text", "value": request.form["email"]},      
                "dateOfContract": {"type": "Text", "value": request.form["dateOfContract"]},          
                "category": {"type": "Text", "value": request.form["category"]},
                "salary": {"type": "Integer", "value": int(request.form["salary"])},
                "skills": {"type": "Text", "value": request.form["skills"]},
                "username": {"type": "Text", "value": request.form["username"]},
                "password": {"type": "Text", "value": request.form["password"]},
                "refStore": {"type": "Relationship", "value": request.form["store"]}
                }
        
        status = ngsiv2.update_attrs(identifier, attrs)
        print(status)
        if status == 204:
            next = request.args.get('next', None)
            if next:
                return redirect(next)
            return redirect(url_for('employees'))
    else:
        return render_template('update_employee.html')

@app.route("/employee/delete", methods=['GET', 'POST'])
def delete_employee():
    if request.method == 'POST':
        print(request.form["id"])
        identifier = str(request.form["id"])
        status = ngsiv2.delete_entity(identifier)
        #status = ngsiv2.delete_context_provider(identifier)
        print(status)
        if status == 204:
            next = request.args.get('next', None)
            if next:
                return redirect(next)
            return redirect(url_for('employees'))
    else:
        return render_template('delete_employee.html')

@app.route('/stores/')
def stores():
 (status, stores) = ngsiv2.list_entities(type = 'Store', options = 'keyValues')
#  print(status)
#  pprint.pprint(stores)
 if status == 200:
    return render_template('stores.html', stores = stores)
 
@app.route('/stores/<id>')
def store(id):
 status, response = get_weather_value(id, "relativeHumidity")
 status2, response2 = get_weather_value(id, "temperature")
 status2, response3 = get_weather_value(id, "tweets")

 (status, store) = ngsiv2.read_entity(id)
 store["image"]["value"] = store["image"]["value"].ljust(math.ceil(len(store["image"]["value"]) / 4) * 4, '=')
 store["relativeHumidity"] = {"type": "Number", "value": response}
 store["temperature"] = {"type": "Number", "value": response2}
 store["tweets"] = {"type": "Text", "value": response3}

 if status == 200:
    (status, inventory_items) = ngsiv2.list_entities(type = 'InventoryItem',
                                                    options = 'keyValues',
                                                    attrs = None)
    if status == 200:
        lon_deg = store['location']['value']['coordinates'][0]
        lat_deg = store['location']['value']['coordinates'][1]
        zoom = 15
        n = 1 << zoom
        lat_rad = math.radians(lat_deg)
        xtile = int((lon_deg + 180.0) / 360.0 * n)
        ytile = int((1.0 - math.asinh(math.tan(lat_rad)) / math.pi) / 2.0 * n)
        return render_template('store.html', store = store, inventory_items = inventory_items, zoom = zoom, xtile = xtile, ytile = ytile)

@app.route("/store/create", methods=['GET', 'POST'])
def create_store():
    if request.method == 'POST':
        print(request.form["id"])
        store = {"id": request.form["id"],
                "type": "Product",
                "name": {"type": "Text", "value": request.form["name"]},
                "address": {"type": "Text", "value": request.form["address"]},
                "location": {"type": "geo:json",
                             "value": {"type": "Point", "coordinates": [request.form["X_cord"],
                                                                        request.form["Y_cord"]]}},
                "image": {"type": "Text", "value": request.form["image"]},  
                "url": {"type": "Text", "value": request.form["url"]},
                "telephone": {"type": "Text", "value": request.form["telephone"]},
                "countryCode": {"type": "Text", "value": request.form["countryCode"]},
                "capacity": {"type": "Integer", "value": request.form["capacity"]},
                "description": {"type": "Integer", "value": request.form["description"]},
                "temperature": {"type": "Text", "value": request.form["temperature"]},    
                "relativeHumidity": {"type": "Integer", "value": request.form["relativeHumidity"]}
        }
        
        status = ngsiv2.create_entity(store)
        print(status)
        if status == 201:
            next = request.args.get('next', None)
            if next:
                return redirect(next)
            return redirect(url_for('stores'))
    else:
        return render_template('create_store.html')

@app.route("/store/update", methods=['GET', 'POST'])
def update_store():
    if request.method == 'POST':
        print(request.form["id"])
        identifier = request.form["id"]
        attrs = {
                "name": {"type": "Text", "value": request.form["name"]},
                "address": {"type": "Text", "value": request.form["address"]},
                "location": {"type": "geo:json",
                             "value": {"type": "Point", "coordinates": [request.form["X_cord"],
                                                                        request.form["Y_cord"]]}},
                "image": {"type": "Text", "value": request.form["image"]},  
                "url": {"type": "Text", "value": request.form["url"]},
                "telephone": {"type": "Text", "value": request.form["telephone"]},
                "countryCode": {"type": "Text", "value": request.form["countryCode"]},
                "capacity": {"type": "Integer", "value": request.form["capacity"]},
                "description": {"type": "Integer", "value": request.form["description"]},
                "temperature": {"type": "Text", "value": request.form["temperature"]},    
                "relativeHumidity": {"type": "Integer", "value": request.form["relativeHumidity"]}
        }
        status = ngsiv2.update_attrs(identifier, attrs)
        print(status)
        if status == 204:
            next = request.args.get('next', None)
            if next:
                return redirect(next)
            return redirect(url_for('stores'))
    else:
        return render_template('update_store.html')

@app.route("/store/delete", methods=['GET', 'POST'])
def delete_store():
    if request.method == 'POST':
        print(request.form["id"])
        identifier = str(request.form["id"])
        status = ngsiv2.delete_entity(identifier)
        #status = ngsiv2.delete_context_provider(identifier)
        print(status)
        if status == 204:
            next = request.args.get('next', None)
            if next:
                return redirect(next)
            return redirect(url_for('stores'))
    else:
        return render_template('delete_store.html')

@app.route('/products/')
def products():
 (status, products) = ngsiv2.list_entities(type = 'Product')
#  print(status)
 if status == 200:
    return render_template('products.html', products = products)

@app.route('/products/<id>')
def product(id):
 (status, product) = ngsiv2.read_entity(id)
 print(product)
 product["image"]["value"] = product["image"]["value"].ljust(math.ceil(len(product["image"]["value"]) / 4) * 4, '=')

 if status == 200:
    (status, inventory_items) = ngsiv2.list_entities(type = 'InventoryItem',
                                                    options = 'keyValues',
                                                    attrs = None)
    if status == 200:
        return render_template('product.html', product = product, inventory_items = inventory_items)

@app.route("/product/create", methods=['GET', 'POST'])
def create_product():
    if request.method == 'POST':
        print(request.form["id"])
        product = {"id": request.form["id"],
                "type": "Product",
                "name": {"type": "Text", "value": request.form["name"]},
                "image": {"type": "Text", "value": request.form["image"]},      
                "color": {"type": "Text", "value": request.form["color"]},          
                "size": {"type": "Text", "value": request.form["size"]},
                "price": {"type": "Integer", "value": int(request.form["price"])}}
        status = ngsiv2.create_entity(product)
        print(status)
        if status == 201:
            next = request.args.get('next', None)
            if next:
                return redirect(next)
            return redirect(url_for('products'))
    else:
        return render_template('create_product.html')

@app.route("/product/update", methods=['GET', 'POST'])
def update_product():
    if request.method == 'POST':
        print(request.form["id"])
        identifier = request.form["id"]
        attrs = {
                "name": {"type": "Text", "value": request.form["name"]},
                "image": {"type": "Text", "value": request.form["image"]},      
                "color": {"type": "Text", "value": request.form["color"]},          
                "size": {"type": "Text", "value": request.form["size"]},
                "price": {"type": "Integer", "value": int(request.form["price"])}}
        status = ngsiv2.update_attrs(identifier, attrs)
        print(status)
        if status == 204:
            next = request.args.get('next', None)
            if next:
                return redirect(next)
            return redirect(url_for('products'))
    else:
        return render_template('update_product.html')
    
@app.route("/product/delete", methods=['GET', 'POST'])
def delete_product():
    if request.method == 'POST':
        print(request.form["id"])
        identifier = str(request.form["id"])
        status = ngsiv2.delete_entity(identifier)
        #status = ngsiv2.delete_context_provider(identifier)
        print(status)
        if status == 204:
            next = request.args.get('next', None)
            if next:
                return redirect(next)
            return redirect(url_for('products'))
    else:
        return render_template('delete_product.html')

@app.route("/buy/<id>", methods=['GET', 'POST'])
def buy_product(id):
    if request.method == 'POST':
        attrs = {
                "shelfCount": {"type":"Integer", "value": {"$inc": -1}},
                "stockCount": {"type":"Integer", "value": {"$inc": -1}}
            }
        status = ngsiv2.update_attrs(id, attrs)
        print(status)
        if status == 204:
            next = request.args.get('next', None)
            if next:
                return redirect(next)
            return redirect(url_for('products'))
    else:
        status, inventory_item = ngsiv2.read_entity(id)
        status, product = ngsiv2.read_entity(str(inventory_item["refProduct"]["value"]))
        return render_template('buy_product.html', inventory_item = inventory_item,
                               product = product)
