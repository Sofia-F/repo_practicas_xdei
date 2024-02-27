import re
from datetime import datetime
from flask import render_template
import ngsiv2
from flask import Flask

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("home.html")

@app.route("/api/data")
def get_data():
    return app.send_static_file("data.json")

# New functions
@app.route("/about/")
def about():
    return render_template("about.html")

@app.route("/stores/")
def stores():
    return render_template("stores.html")

@app.route('/products/')
def products():
 (status, products) = ngsiv2.list_entities(type = 'Product', options = 'keyValues')
 print(status)
 print(products)
 if status == 200:
    return render_template('products.html', products = products)

@app.route('/products/<id>')
def product(id):
 (status, product) = ngsiv2.read_entity(id)
 if status == 200:
    (status, inventory_items) = ngsiv2.list_entities(type = 'InventoryItem',
                                                    options = 'keyValues',
                                                    query = f'refProduct=={id}')
    print(inventory_items)
    if status == 200:
        return render_template('product.html', product = product, inventory_items = inventory_items)
