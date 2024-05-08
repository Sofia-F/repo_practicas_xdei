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
    estados_animales = animals.status.value_counts() / len(animals)

    animal_counts = animals['entity_id'].value_counts(normalize=True).reset_index()
    animal_counts.columns = ['entity_id', 'percentage']

    # Series de tiempo 
    fig_time = px.line(animals, x='time_index', y=['heartrate'])
    graphJSON_time = json.dumps(fig_time, cls=plotly.utils.PlotlyJSONEncoder)

    # Humedad vs nivel de llenado
    fig_reg = px.scatter(animals, x='heartrate', y="status",
                        title = "Relación heartrate/status",
                        trendline='ols', trendline_color_override='darkblue')
    graphJSON_reg = json.dumps(fig_reg, cls=plotly.utils.PlotlyJSONEncoder)

    # Pie chart numero de frutas
    fig_chart = px.pie(animal_counts, values='percentage', names = "entity_id", title='Percentage of status')
    graphJSON_chart = json.dumps(fig_chart, cls=plotly.utils.PlotlyJSONEncoder)

    # Histograma de las pulsaciones
    fig_hist = px.histogram(animals, x="heartrate")
    graphJSON_hist = json.dumps(fig_hist, cls=plotly.utils.PlotlyJSONEncoder)

    # Diagrama de barras del numero de vacas cerdos y llenado
    fig_bar = px.bar(animal_counts, x="entity_id", y="percentage", title="Llenado por granja")
    graphJSON_bar = json.dumps(fig_bar, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template('home.html', graphJSON_time = graphJSON_time,
                                        graphJSON_reg = graphJSON_reg,
                                        graphJSON_chart = graphJSON_chart,
                                        graphJSON_hist = graphJSON_hist,
                                        graphJSON_bar = graphJSON_bar)
