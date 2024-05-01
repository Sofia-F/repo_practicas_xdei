import requests
import pprint
from datetime import datetime
from flask import render_template
import ngsiv2
from flask import Flask, render_template, redirect, url_for, request
from read_subscriptions import read_subscriptions
import create_subscriptions
import math
app = Flask(__name__)
import json


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

@app.route("/subscriptions/create/", methods=['GET', 'POST'])
def create_subscription():

    if request.method == 'POST':
        
        print("hola")
        print()
        print(request.form["condition_attrs"])
        print(request.form["condition_attrs"].split(", "))
        print()

        Description = request.form["description"]

        Subject = {
            "entities": [{"idPattern": request.form["entity_id_pattern"]}],
            "condition": {"attrs": request.form["condition_attrs"].split(", ")}
        }

        Notification = {
            "http": {"url": request.form["notif_http_url"]},
            "attrs": request.form["condition_attrs"].split(", "),
            "metadata": request.form["notif_metadata"].split(", ")
        }

        Throttling = int(request.form["throttling"])
        
        print(Description)
        print(Subject)
        print(Notification)
        print(Throttling)

        status = create_subscriptions.create_subs(Description, Subject, Notification, Throttling)
        print(status)
        if status == 201:
            next = request.args.get('next', None)
            if next:
                return redirect(next)
            return redirect(url_for('subscriptions'))
    else:
        return render_template('create_subscription.html')   

@app.route("/subscriptions/update/<id>", methods=['GET', 'POST'])
def update_subscription(id):

    if request.method == 'POST':
       
        url = "http://localhost:1026/v2/subscriptions/"+id

        payload = {
           
         'description': request.form["description"], 
         'subject': {'entities': [{'idPattern': request.form["entity_id_pattern"]}], 
                     'condition': {'attrs': request.form["condition_attrs"].split(",")}},
         'notification': {'http': {'url': request.form["notif_http_url"]}, 
                                   'attrs': request.form["notif_attrs"].split(", "),
                                   'metadata': request.form["notif_metadata"].split(", ")},
         'throttling': int(request.form["throttling"])
        }

        print(payload)

        headers = {
            'Content-Type': 'application/json',
            'fiware-service': 'openiot',
            'fiware-servicepath': '/'
        }

        response = requests.request("PATCH", url, headers=headers, data=json.dumps(payload))
        status = response.status_code
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
    url = "http://localhost:1026/v2/subscriptions/"

    headers = {
        'fiware-service': 'openiot',
        'fiware-servicepath': '/'
    }

    subscriptions = requests.request("GET", url, headers=headers).json()

    for subscription in subscriptions:
        if subscription["id"] == id:
            url = "http://localhost:1026/v2/subscriptions/"+subscription["id"]
            response = requests.request("DELETE", url, headers=headers)

    if response.status_code == 204:
        next = request.args.get('next', None)
        if next:
            return redirect(next)
        return redirect(url_for('subscriptions'))

@app.route('/subscriptions/')
def subscriptions():
    subscriptions = read_subscriptions().json()
    return render_template("subscriptions.html", subscriptions = subscriptions)