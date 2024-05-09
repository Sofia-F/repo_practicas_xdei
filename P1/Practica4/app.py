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

    # Serie de tiempo llenado
    fig_fill_time = px.line(filling, x='time_index', y="filling")
    graphJSON_fill_time = json.dumps(fig_fill_time, cls=plotly.utils.PlotlyJSONEncoder)

    # Status por animal de las granjas barchart
    perc = animals[["entity_id", "status"]].groupby(["entity_id", "status"]).value_counts(normalize=True)
    print(perc)
    fig_bar = px.bar(perc, x="entity_id", y="proportion", names = "status",  color="status")
    graphJSON_bar = json.dumps(fig_bar, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template('home.html', graphJSON_fill_time = graphJSON_fill_time,
                           graphJSON_bar = graphJSON_bar)
