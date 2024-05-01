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

app = Flask(__name__)

@app.route("/")
def home():

    df = pd.DataFrame({
        'Fruit': ['Apples', 'Oranges', 'Bananas', 'Apples', 'Oranges', 'Bananas'],
        'Amount': [4, 1, 2, 2, 4, 5],
        'Prueba': [4, 1, 8, 3, 5, 7],
        'Latitud': [42.878213, 42.240599, 43.012787, 43.483151, 42.431423, 42.335508],
        'Longitud': [-8.544844, -8.720727, -7.555851, -8.227421, -8.644623, -7.863597],
        'City': ['SF', 'SF', 'SF', 'Montreal', 'Montreal', 'Montreal'],
        'Dates': ['2024-01-15', '2024-03-20', '2024-05-10', '2024-07-01', '2024-08-01', '2024-09-01'] 
    })

    df['Dates'] = pd.to_datetime(df['Dates'])
    geometry = [Point(xy) for xy in zip(df['Longitud'], df['Latitud'])]
    fruit_counts = df['Fruit'].value_counts(normalize=True).reset_index()
    fruit_counts.columns = ['Fruit', 'Percentage']
    gdf = gpd.GeoDataFrame(df, geometry=geometry, crs='EPSG:4326')
    heat_data = [[point.xy[1][0], point.xy[0][0]] for point in gdf.geometry]

    # Mapa
    m = folium.Map()
    features = []
    for _, row in gdf.iterrows():
        feature = {
        'type': 'Feature',
        'geometry': {
            'type': 'Point',
            'coordinates': [row['Longitud'], row['Latitud']]
            },
        'properties': {
            'time': row['Dates'].date().isoformat(),
            'popup': f"{row['Fruit']} - Amount: {row['Amount']}"
            }
        }
        features.append(feature)
        folium.CircleMarker([row['Latitud'], row['Longitud']], radius=5, fill = True).add_to(m)

    # Mapa posiciones
    m.fit_bounds(m.get_bounds())
    iframe = m.get_root()._repr_html_()

    # Mapa evolucion temporal
    m2 = folium.Map()
    TimestampedGeoJson(
        {'type': 'FeatureCollection', 'features': features},
        period='P1M', 
        add_last_point=True,  
        auto_play=False
    ).add_to(m2)
    iframe2 = m2.get_root()._repr_html_()

    # Mapa de calor
    m3 = folium.Map(zoom_start=6)
    HeatMap(heat_data).add_to(m3)
    iframe3 = m3.get_root()._repr_html_()

    # Series de tiempo 
    fig_time = px.line(df, x='Dates', y=['Amount', "Prueba"])
    graphJSON_time = json.dumps(fig_time, cls=plotly.utils.PlotlyJSONEncoder)

    # Humedad vs nivel de llenado
    fig_reg = px.scatter(df, x='Amount', y="Prueba",
                        title = "Relación amount/pruebas",
                        trendline='ols', trendline_color_override='darkblue')
    graphJSON_reg = json.dumps(fig_reg, cls=plotly.utils.PlotlyJSONEncoder)

    # Pie chart numero de frutas
    fig_chart = px.pie(fruit_counts, values='Percentage', names = "Fruit", title='Percentage of fruits')
    graphJSON_chart = json.dumps(fig_chart, cls=plotly.utils.PlotlyJSONEncoder)

    # Histograma de las pulsaciones
    fig_hist = px.histogram(df, x="Amount")
    graphJSON_hist = json.dumps(fig_hist, cls=plotly.utils.PlotlyJSONEncoder)

    # Diagrama de barras del numero de vacas cerdos y llenado
    fig_bar = px.bar(fruit_counts, x="Fruit", y="Percentage", title="Llenado por granja")
    graphJSON_bar = json.dumps(fig_bar, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template('home.html', graphJSON_time = graphJSON_time,
                                        graphJSON_reg = graphJSON_reg,
                                        graphJSON_chart = graphJSON_chart,
                                        graphJSON_hist = graphJSON_hist,
                                        graphJSON_bar = graphJSON_bar,
                                        iframe=iframe,
                                        iframe2=iframe2,
                                        iframe3=iframe3)
