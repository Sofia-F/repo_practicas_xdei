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
    tractors = pd.read_csv("tractors.csv")
    soil = pd.read_csv("soilsensor.csv")
    filling = pd.read_csv("fillingsensor.csv")

    fig_fill_time = px.line(filling, x='time_index', y="filling")
    graphJSON_fill_time = json.dumps(fig_fill_time, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template('home.html', graphJSON_fill_time = graphJSON_fill_time)
