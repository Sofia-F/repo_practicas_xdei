from flask import Flask, render_template
import pandas as pd
import json
import plotly
import plotly.express as px
import folium
import geopandas as gpd
from shapely.geometry import Point
from folium.plugins import TimestampedGeoJson
import statsmodels
from folium.plugins import HeatMap
import datetime

app = Flask(__name__)

@app.route("/")
def home():

    animals = pd.read_csv("animals.csv")
    

    return render_template('home.html', graphJSON_time = graphJSON_time,
                                        graphJSON_reg = graphJSON_reg,
                                        graphJSON_chart = graphJSON_chart,
                                        graphJSON_hist = graphJSON_hist,
                                        graphJSON_bar = graphJSON_bar)
