import requests
import pprint
from datetime import datetime
from flask import render_template
import ngsiv2
from flask import Flask

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
#  pprint.pprint(products)
 if status == 200:
    return render_template('stores.html', stores = stores)
 
@app.route('/stores/<id>')
def store(id):
 (status, store) = ngsiv2.read_entity(id)
 print(status)
 pprint.pprint(product)
 if status == 200:
    (status, inventory_items) = ngsiv2.list_entities(type = 'InventoryItem',
                                                    options = 'keyValues',
                                                    attrs = f'refStore=={id}')
    print(inventory_items)
    if status == 200:
        return render_template('store.html', store = store, inventory_items = inventory_items)

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
                                                    attrs = f'refProduct=={id}')
    print(inventory_items)
    if status == 200:
        return render_template('product.html', product = product, inventory_items = inventory_items)
