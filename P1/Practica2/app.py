import requests
import pprint
from datetime import datetime
from flask import render_template, request, redirect, url_for
import ngsiv2
from flask import Flask
import math
import json
from flask import Flask, render_template
from flask_socketio import SocketIO

app = Flask(__name__)
socketio = SocketIO(app)

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
                "type": "Employee",
                "name": {"type": "Text", "value": request.form["name"]},
                "email": {"type": "Text", "value": request.form["email"]},      
                "dateOfContract": {"type": "Text", "value": request.form["dateOfContract"]},          
                "category": {"type": "Text", "value": request.form["category"]},
                "salary": {"type": "Integer", "value": int(request.form["salary"])},
                "skills": {"type": "Text", "value": request.form["skills"]},
                "username": {"type": "Text", "value": request.form["username"]},
                "password": {"type": "Text", "value": request.form["password"]},
                "image": {"type": "Text", "value": ngsiv2.b64(request.form["image"])},
                "refStore": {"type": "Relationship", "value": request.form["refStore"]}
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

@app.route("/employee/update/<id>", methods=['GET', 'POST'])
def update_employee(id):
    if request.method == 'POST':

        attrs = {
                "name": {"type": "Text", "value": request.form["name"]},
                "email": {"type": "Text", "value": request.form["email"]},      
                "dateOfContract": {"type": "Text", "value": request.form["dateOfContract"]},          
                "category": {"type": "Text", "value": request.form["category"]},
                "salary": {"type": "Integer", "value": int(request.form["salary"])},
                "skills": {"type": "Text", "value": request.form["skills"]},
                "username": {"type": "Text", "value": request.form["username"]},
                "password": {"type": "Text", "value": request.form["password"]},
                "refStore": {"type": "Relationship", "value": request.form["refStore"]},
                "image": {"type": "Text", "value": ngsiv2.b64(request.form["image"])}
                }
        
        status = ngsiv2.update_attrs(id, attrs)
        print(status)
        if status == 204:
            next = request.args.get('next', None)
            if next:
                return redirect(next)
            return redirect(url_for('employees'))
    else:
        return render_template('update_employee.html', id = id)

@app.route("/employee/delete/<id>", methods=['GET', 'POST'])
def delete_employee(id):
    if request.method == 'GET':

        status = ngsiv2.delete_entity(id)
        #status = ngsiv2.delete_context_provider(identifier)

        if status == 204:
            next = request.args.get('next', None)
            if next:
                return redirect(next)
            return redirect(url_for('employees'))

@app.route('/stores/')
def stores():
 (status, stores) = ngsiv2.list_entities(type = 'Store', options = 'keyValues')
 print(stores)
 for store in stores:
     print("Tienda")
     status, response = get_weather_value(store["id"], "relativeHumidity")
     status2, response2 = get_weather_value(store["id"], "temperature")
     store["temperature"] = {"type": "Text", "value": response}
     store["relativeHumidity"] = {"type": "Text", "value": response2}

 if status == 200:
    return render_template('stores.html', stores = stores)
 
@app.route('/stores/<id>')
def store(id):
 status2, response3 = get_weather_value(id, "tweets")

 (status, store) = ngsiv2.read_entity(id)
 store["image"]["value"] = store["image"]["value"].ljust(math.ceil(len(store["image"]["value"]) / 4) * 4, '=')
 store["tweets"] = {"type": "Text", "value": response3}

 if status == 200:
    (status, inventory_items) = ngsiv2.list_entities(type = 'InventoryItem',
                                                    options = 'keyValues',
                                                    attrs = None,
                                                    filter = "refStore=="+id)
    (status, shelf_items) = ngsiv2.list_entities(type = 'Shelf',
                                                 options = 'keyValues',
                                                 attrs = None)
    
    (status, product_items) = ngsiv2.list_entities(type = 'Product',
                                                 options = 'keyValues',
                                                 attrs = None)
    

    if status == 200:
        print(shelf_items[1])
        for inventory in inventory_items:
            for shelf in shelf_items:
                print(inventory["refShelf"], shelf["id"], inventory["refStore"], shelf["refStore"])
                print(inventory["refShelf"] == shelf["id"])
                print(inventory["refStore"] == shelf["refStore"])
                if inventory["refShelf"] == shelf["id"] and inventory["refStore"] == shelf["refStore"]:
                    print(shelf["maxCapacity"])
                    inventory["maxCapacity"] = shelf["maxCapacity"]

        for inventory in inventory_items:
            for product in product_items:
                print(inventory["refProduct"], product["id"])
                print(inventory["refProduct"] == product["id"])
                if inventory["refProduct"] == product["id"]:
                    inventory["prodName"] = product["name"]
                    inventory["prodPrice"] = product["price"]
                    inventory["prodSize"] = product["size"]
                    inventory["prodColor"] = product["color"]

        grouped_inventory = {}
        grouped_capacity = {}
        for item in inventory_items:
            store_id = item['refStore']
            shelf_id = item['refShelf']
            shelf_count = item['shelfCount']
            max_capacity = item["maxCapacity"]
            grouped_capacity[(store_id, shelf_id)] = max_capacity
            if (store_id, shelf_id) in grouped_inventory:
                grouped_inventory[(store_id, shelf_id)] += shelf_count
            else:
                grouped_inventory[(store_id, shelf_id)] = shelf_count
        print(grouped_capacity)
        print(grouped_inventory)
        lon_deg = store['location']['value']['coordinates'][1]
        lat_deg = store['location']['value']['coordinates'][0]
        zoom = 15
        n = 1 << zoom
        lat_rad = math.radians(lat_deg)
        xtile = int((lon_deg + 180.0) / 360.0 * n)
        ytile = int((1.0 - math.asinh(math.tan(lat_rad)) / math.pi) / 2.0 * n)
        return render_template('store.html', store = store, inventory_items = inventory_items,
                                zoom = zoom, xtile = xtile, ytile = ytile,
                                grouped_inventory = grouped_inventory,
                                grouped_capacity = grouped_capacity)

@app.route("/store/create", methods=['GET', 'POST'])
def create_store():
    if request.method == 'POST':
        print(request.form["id"])
        location = request.form["location"]
        X_cord, Y_cord = location.split(',') 
        store = {"id": request.form["id"],
                "type": "Store",
                "name": {"type": "Text", "value": request.form["name"]},
                "address": {"type": "Text", "value": request.form["address"]},
                "location": {"type": "geo:json",
                             "value": {"type": "Point", "coordinates": [float(X_cord),
                                                                        float(Y_cord)]}},
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

@app.route("/store/update/<id>", methods=['GET', 'POST'])
def update_store(id):
    if request.method == 'POST':
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
        status = ngsiv2.update_attrs(id, attrs)
        print(status)
        if status == 204:
            next = request.args.get('next', None)
            if next:
                return redirect(next)
            return redirect(url_for('stores'))
    else:
        return render_template('update_store.html', id = id)

@app.route("/store/delete/<id>", methods=['GET', 'POST'])
def delete_store(id):
    if request.method == 'GET':
        status = ngsiv2.delete_entity(id)
        print(status)
        if status == 204:
            next = request.args.get('next', None)
            if next:
                return redirect(next)
            return redirect(url_for('stores'))

@app.route("/store/<id>/shelf/<idShelf>/product/create", methods=['GET', 'POST'])
def create_shelfProd(id,idShelf):
    if request.method == 'POST':

        store = {
            "id": request.form["id"],
            "type": "InventoryItem",
            "refShelf": {"type": "Text", "value": idShelf},
            "refStore": {"type": "Text", "value": id},
            "refProduct": {"type": "Text", "value": request.form["refProduct"]},
            "shelfCount": {"type": "Number", "value": request.form["shelfCount"]},
            "stockCount": {"type": "Number", "value": request.form["stockCount"]}
        }
        
        status = ngsiv2.create_entity(store)
        print(status)
        if status == 201:
            next = request.args.get('next', None)
            if next:
                return redirect(next)
            return redirect(url_for('stores'))
    else:
        (status, inventory_items) = ngsiv2.list_entities(type = 'InventoryItem',
                                                        options = 'keyValues',
                                                        attrs = None,
                                                        filter = "refStore=="+id+";refShelf=="+idShelf)
        (status, products) = ngsiv2.list_entities(type = 'Product',
                                                        options = 'keyValues')
        product_list = []
        for product in products:
            product_list.append(product["id"])

        for inventory in inventory_items:
            print(inventory["refProduct"])
            if inventory["refProduct"] in product_list:
                product_list.remove(inventory["refProduct"])

        return render_template('create_shelfProd.html', 
                               id = id,
                               idShelf = idShelf,
                               product_list = product_list)
    
@app.route("/store/<id>/product/<idProduct>/shelf/create", methods=['GET', 'POST'])
def create_shelf(id, idProduct):
    if request.method == 'POST':

        store = {
            "id": request.form["id"],
            "type": "InventoryItem",
            "refShelf": {"type": "Text", "value": request.form["refShelf"]},
            "refStore": {"type": "Text", "value": id},
            "refProduct": {"type": "Text", "value": idProduct},
            "shelfCount": {"type": "Number", "value": request.form["shelfCount"]},
            "stockCount": {"type": "Number", "value": request.form["stockCount"]}
        }
        
        status = ngsiv2.create_entity(store)
        print(status)
        if status == 201:
            next = request.args.get('next', None)
            if next:
                return redirect(next)
            return redirect(url_for('stores'))
    else:
        (status, inventory_items) = ngsiv2.list_entities(type = 'InventoryItem',
                                                        options = 'keyValues',
                                                        attrs = None,
                                                        filter = "refStore=="+id+";refProduct=="+idProduct)
        (status, shelves) = ngsiv2.list_entities(type = 'Shelf',
                                                        options = 'keyValues')
        shelf_list = []
        for shelf in shelves:
            shelf_list.append(shelf["id"])

        for inventory in inventory_items:
            print(inventory["refShelf"])
            if inventory["refShelf"] in shelf_list:
                shelf_list.remove(inventory["refShelf"])

        return render_template('create_shelf.html', 
                               id = id,
                               idShelf = idProduct,
                               product_list = shelf_list)
    
@app.route("/store/<idStore>/shelf/delete/<id>", methods=['GET', 'POST'])
def delete_shelf(id, idStore):
    if request.method == 'GET':
        print(id)
        print(idStore)
        status = ngsiv2.delete_entity(id)
        print(status)
        if status == 204:
            next = request.args.get('next', None)
            if next:
                return redirect(next)
            return redirect(url_for('stores'))

@app.route("/store/<idStore>/shelf/update/<id>", methods=['GET', 'POST'])
def update_shelf(id, idStore):
    if request.method == 'POST':
        attrs = {
            "refShelf": {"type": "Text", "value": request.form["refShelf"]},
            "refStore": {"type": "Text", "value": request.form["refStore"]},
            "shelfCount": {"type": "Number", "value": request.form["shelfCount"]},
            "stockCount": {"type": "Number", "value": request.form["stockCount"]}
        }
        status = ngsiv2.update_attrs(id, attrs)
        print(status)
        if status == 204:
            next = request.args.get('next', None)
            if next:
                return redirect(next)
            return redirect(url_for('stores'))
    else:
        return render_template('update_shelf.html', id = id)
            
@app.route('/products/')
def products():
 (status, products) = ngsiv2.list_entities(type = 'Product')
#  print(status)
 product["image"]["value"] = product["image"]["value"].ljust(math.ceil(len(product["image"]["value"]) / 4) * 4, '=')
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
                                                    attrs = None,
                                                    filter = "refProduct=="+id)
    (status, shelf_items) = ngsiv2.list_entities(type = 'InventoryItem',
                                                    options = 'keyValues',
                                                    attrs = None,
                                                    filter = "refProduct=="+id)
                                                    
    grouped_inventory = {}
    for item in inventory_items:
        store_id = item['refStore']
        product_id = item['refProduct']
        stock_count = item['stockCount']
        if (store_id, product_id) in grouped_inventory:
            grouped_inventory[(store_id, product_id)] += stock_count
        else:
            grouped_inventory[(store_id, product_id)] = stock_count

    if status == 200:
        return render_template('product.html', product = product, inventory_items = inventory_items,
                               grouped_inventory = grouped_inventory)

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

@app.route("/product/update/<id>", methods=['GET', 'POST'])
def update_product(id):
    print(id)
    if request.method == 'POST':
        print(id)
        attrs = {
                "name": {"type": "Text", "value": request.form["name"]},
                "image": {"type": "Text", "value": request.form["image"]},      
                "color": {"type": "Text", "value": request.form["color"]},          
                "size": {"type": "Text", "value": request.form["size"]},
                "price": {"type": "Integer", "value": int(request.form["price"])}}
        status = ngsiv2.update_attrs(id, attrs)
        print(status)
        if status == 204:
            next = request.args.get('next', None)
            if next:
                return redirect(next)
            return redirect(url_for('products'))
    else:
        return render_template('update_product.html', id = id)
    
@app.route("/product/delete/<id>", methods=['GET', 'POST'])
def delete_product(id):
    if request.method == 'GET':
        status = ngsiv2.delete_entity(id)

        if status == 204:
            next = request.args.get('next', None)
            if next:
                return redirect(next)
            return redirect(url_for('products'))

@app.route("/buy/<id>", methods=['GET', 'POST'])
def buy_product(id):
    if request.method == 'GET':
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
            return redirect(url_for('stores'))

@app.route('/subscription/')
def subscription():
    print(request.method)
    if request.method == "POST":
        json_msg = request.form
        socketio.emit('my event', json_msg)
    return render_template('notificaciones.html')

@app.route('/map/')
def map():
    (status, stores) = ngsiv2.list_entities(type = 'Store', options = 'keyValues')
    return render_template('map.html', stores = stores)

if __name__ == '__main__':
    socketio.run(app)

