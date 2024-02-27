import re
from datetime import datetime
from flask import render_template

from flask import Flask

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("home.html")

@app.route("/hello/")
@app.route("/hello/<name>")
def hello_there(name = None):
    return render_template(
        "hello_there.html",
        name=name,
        date=datetime.now()
    )

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

@app.route("/products/")
def products():
    return render_template("products.html")
