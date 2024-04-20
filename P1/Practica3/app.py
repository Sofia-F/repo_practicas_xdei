import requests
import pprint
from datetime import datetime
from flask import render_template
import ngsiv2
from flask import Flask, render_template, redirect, url_for, request
import math
app = Flask(__name__)


@app.route("/")
def home():
    return render_template("home.html")

@app.route("/about/")
def about():
    return render_template("about.html")

@app.route('/stores/')
def stores():
 (status, stores) = ngsiv2.list_entities(type = 'Store', options = 'keyValues')
#  print(status)
#  pprint.pprint(stores)
 if status == 200:
    return render_template('stores.html', stores = stores)
 
@app.route('/stores/<id>')
def store(id):
 (status, store) = ngsiv2.read_entity(id)
 print(status)
 if status == 200:
    (status, inventory_items) = ngsiv2.list_entities(type = 'InventoryItem',
                                                    options = 'keyValues',
                                                    attrs = None)
    print(inventory_items)
    if status == 200:
        lon_deg = store['location']['value']['coordinates'][0]
        lat_deg = store['location']['value']['coordinates'][1]
        zoom = 15
        n = 1 << zoom
        lat_rad = math.radians(lat_deg)
        xtile = int((lon_deg + 180.0) / 360.0 * n)
        ytile = int((1.0 - math.asinh(math.tan(lat_rad)) / math.pi) / 2.0 * n)
        return render_template('store.html', store = store, inventory_items = inventory_items, zoom = zoom, xtile = xtile, ytile = ytile)

@app.route('/products/')
def products():
 (status, products) = ngsiv2.list_entities(type = 'Product', options = 'keyValues')
#  print(status)
#  pprint.pprint(products)
 if status == 200:
    return render_template('products.html', products = products)

@app.route('/products/<id>')
def product(id):
 (status, product) = ngsiv2.read_entity(id)
 print(status)
 pprint.pprint(product)
 if status == 200:
    (status, inventory_items) = ngsiv2.list_entities(type = 'InventoryItem',
                                                    options = 'keyValues',
                                                    attrs = None)
    print(inventory_items)
    if status == 200:
        return render_template('product.html', product = product, inventory_items = inventory_items)


@app.route("/subscriptions/update/<id>", methods=['GET', 'POST'])
def update_subscription(id):
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
                "image": {"type": "Text", "value": ngsiv2.b64("images/employees/"+request.form["image"])}
                }
        
        status = ngsiv2.update_attrs(id, attrs)
        print(status)
        if status == 204:
            next = request.args.get('next', None)
            if next:
                return redirect(next)
            return redirect(url_for('subscriptions'))
    else:
        return render_template('update_subscription.html', id = id)

@app.route("/subscriptions/delete/<id>", methods=['GET', 'POST'])
def delete_subscription(id):
    if request.method == 'GET':

        status = ngsiv2.delete_entity(id)

        if status == 204:
            next = request.args.get('next', None)
            if next:
                return redirect(next)
            return redirect(url_for('subscriptions'))

@app.route('/subscriptions/')
def subscriptions():
    return render_template("subscriptions.html")