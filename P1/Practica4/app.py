from flask import Flask, render_template
import pandas as pd
import json
import plotly
import plotly.express as px
import folium
import geopandas as gpd
from shapely.geometry import Point
from folium.plugins import TimestampedGeoJson
import psycopg
import pandas as pd
from shapely.geometry import shape
import datetime
from folium.plugins import HeatMap
import datetime
import requests

app = Flask(__name__)

def read_api(id, types, limit, last, attrs):
    url = "http://localhost:8668/v2/"

    if id != None:
        url = url + "entities/urn:ngsi-ld:Device:" + id + "/"

    if types != None:
        url = url + "types/" + types + "/"

    url = url + "attrs/" + attrs

    if limit != None:
        url = url +"?limit="+str(limit)
    
    if last != None:
        url = url +"?lastN="+str(last)

    payload = ""
    headers = {
    'Accept': 'application/json',
    'Fiware-Service': 'openiot',
    'Fiware-ServicePath': '/'
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    return response

@app.route("/")
def home():

    # QL API
    ############################
    # Pulsaciones primera vaca #
    ############################
    response = read_api(id = "cow001", types = None, limit = None, last = None, attrs = "heartrate")
    heart_vaca = pd.DataFrame(response.json())
    heart_vaca["entityId"] = heart_vaca["entityId"].str.split(":").str[3]
    heart_vaca["entityId"] = heart_vaca["entityId"].str.replace("cow", "🐄")
    #print(heart_vaca)

    ############################
    # Pulsaciones primer cerdo #
    ############################
    response = read_api(id = "pig001", types = None, limit = None, last = None, attrs = "heartrate")
    heart_cerdo = pd.DataFrame(response.json())
    heart_cerdo["entityId"] = heart_cerdo["entityId"].str.split(":").str[3]
    heart_cerdo["entityId"] = heart_cerdo["entityId"].str.replace("pig", "🐖")
    #print(heart_cerdo)

    #########################################
    # Última localización de vacas y cerdos #
    #########################################
    response = read_api(id = None, types = "Device", limit = None, last = None, attrs = "location")
    locations = pd.DataFrame(response.json()["entities"])

    # Los resultados están agrupados, los desagrupamos
    locations_ungrup = locations.explode('index').explode('values')
    locations_ungrup["entityId"] = locations_ungrup["entityId"].str.split(":").str[3]
    locations_ungrup["entityId"] = locations_ungrup["entityId"].str.replace("cow", "🐄")
    locations_ungrup["entityId"] = locations_ungrup["entityId"].str.replace("pig", "🐖")

    # Creamos variables latitud y longitud para crear geodataframe
    locations_ungrup["longitude"] = locations_ungrup["values"].apply(lambda x: x.get('coordinates')[0])
    locations_ungrup["latitude"] = locations_ungrup["values"].apply(lambda x: x.get('coordinates')[1])
    gdf = gpd.GeoDataFrame(
        locations_ungrup, geometry=gpd.points_from_xy(locations_ungrup.longitude,
                                                    locations_ungrup.latitude),
                                                        crs="EPSG:4326"
    )
    # Nos quedamos con la última localización
    last_gdf = gpd.GeoDataFrame(gdf.groupby('entityId').last().reset_index(), geometry="geometry", crs = "epsg:4326")

    ###############################
    # Mapa evolución localización #
    ###############################

    # Lista de características GeoJSON
    features = []
    for idx, row in gdf.iterrows():
        line_feature = {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [row["geometry"].x, row["geometry"].y],
            },
            "properties": {
                "time": row["index"],
                "style": {
                    "color": "blue",
                    "weight": 5,
                },
            },
        }
        features.append(line_feature)
    
    # Evolución pulsaciones primer cerdo
    fig_P1 = px.line(heart_cerdo, x='index', y="values", line_shape="spline", markers=True,
                     title = "Evolución de las pulsaciones para el primer cerdo")
    graphJSON_P1 = json.dumps(fig_P1, cls=plotly.utils.PlotlyJSONEncoder)

    # Evolución pulsaciones primera vaca
    fig_C1 = px.line(heart_vaca, x='index', y="values", line_shape="spline", markers=True,
                     title = "Evolución de las pulsaciones para la primera vaca")
    graphJSON_C1 = json.dumps(fig_C1, cls=plotly.utils.PlotlyJSONEncoder)

    # Ultima localización vacas y cerdos
    m = folium.Map([52.486, 13.374], zoom_start=12)
    folium.GeoJson(
        last_gdf, name="Animals",
        marker=folium.Marker(),
        tooltip=folium.GeoJsonTooltip(fields=["entityId"]),
        popup=folium.GeoJsonPopup(fields=["entityId"]),
        zoom_on_click=True,
    ).add_to(m)
    iframe_last = m.get_root()._repr_html_()

    # Evolución temporal
    m2 = folium.Map([52.510, 13.354], zoom_start=14)
    TimestampedGeoJson(
        {
            "type": "FeatureCollection",
            "features": features,
        },
        period="PT1M",
        add_last_point=True,
    ).add_to(m2)
    iframe_time = m2.get_root()._repr_html_()

    # SQL
    with psycopg.connect("dbname=mtopeniot user=crate") as conn:
        with conn.cursor() as cur:

            # Animals
            cur.execute("SELECT entity_id, time_index, heartrate, location, status \
            FROM mtopeniot.etdevice ORDER BY time_index")
            tuples = cur.fetchall()
            animals = pd.DataFrame(data=tuples, columns=['entity_id', 'time_index','heartrate', 'location', 'status'])
            animals['time_index'] = animals['time_index'].apply(datetime.datetime.isoformat)
            animals["entity_id"] = animals["entity_id"].str.split(":").str[3]
            animals["entity_id"] = animals["entity_id"].str.replace("cow", "🐄")
            animals["entity_id"] = animals["entity_id"].str.replace("pig", "🐖")

            # Tractor
            cur.execute("SELECT entity_id, time_index, location, status \
            FROM mtopeniot.ettractor ORDER BY time_index")
            tuples = cur.fetchall()
            tractor = pd.DataFrame(data=tuples, columns=["entity_id", "time_index", "location", "status"])
            tractor['time_index'] = tractor['time_index'].apply(datetime.datetime.isoformat)
            tractor["entity_id"] = tractor["entity_id"].str.split(":").str[3]
            tractor["entity_id"] = tractor["entity_id"].str.replace("tractor", "🚜")
            
            # Filling Level Sensor
            cur.execute("SELECT entity_id, time_index, filling, location \
            FROM mtopeniot.etfillinglevelsensor ORDER BY time_index")
            tuples = cur.fetchall()
            filling = pd.DataFrame(data=tuples, columns=["entity_id", "time_index", "filling", "location"])
            filling ['time_index'] = filling ['time_index'].apply(datetime.datetime.isoformat)
            filling["entity_id"] = filling["entity_id"].str.split(":").str[3]
            filling["entity_id"] = filling["entity_id"].str.replace("filling", "🛖")

            # Soil Sensor
            cur.execute("SELECT entity_id, time_index, humidity \
            FROM mtopeniot.etsoilsensor ORDER BY time_index")
            tuples = cur.fetchall()
            soil = pd.DataFrame(data=tuples, columns=["entity_id", "time_index", "humidity"])
            soil['time_index'] = soil['time_index'].apply(datetime.datetime.isoformat)
            soil["entity_id"] = soil["entity_id"].str.split(":").str[3]
            soil["entity_id"] = soil["entity_id"].str.replace("humidity", "🌿💧")

            # Temperatura
            cur.execute("SELECT entity_id, time_index, temperature \
            FROM mtopeniot.ettemperaturesensor ORDER BY time_index")
            tuples = cur.fetchall()
            temperature = pd.DataFrame(data=tuples, columns=['entity_id', 'time_index',"temperature"])
            temperature['time_index'] = temperature['time_index'].apply(datetime.datetime.isoformat)
            temperature["entity_id"] = temperature["entity_id"].str.split(":").str[3]
            temperature["entity_id"] = temperature["entity_id"].str.replace("temperature", "🌡")


    ######################
    # GRÁFICAS ENUNCIADO #
    ######################

    # Evolución temporal del llenado según la granja (SQL)
    fig_area = px.area(filling, x='time_index', y="filling", facet_col="entity_id", color="entity_id", markers=True,
                       title = "Evolución temporal del llenado en las granjas")
    graphJSON_area = json.dumps(fig_area, cls=plotly.utils.PlotlyJSONEncoder)

    # Evolución humedad (SQL)
    fig_hum = px.line(soil, x='time_index', y="humidity", facet_col="entity_id", line_shape="spline", color = "entity_id",
                      title = "Evolución temporal de la humedad en las granjas")
    graphJSON_hum = json.dumps(fig_hum, cls=plotly.utils.PlotlyJSONEncoder)

    # Evolución temperatura (SQL)
    fig_temp = px.line(temperature, x='time_index', y="temperature", facet_col="entity_id", line_shape="spline", color = "entity_id",
                      title = "Evolución temporal de la temperatura en las granjas")
    graphJSON_temp = json.dumps(fig_temp, cls=plotly.utils.PlotlyJSONEncoder)

    # Evolución status primera vaca (SQL)
    primera_vaca = animals[animals['entity_id'] == "🐄001"]
    primer_firstC_status = px.scatter(primera_vaca, x='time_index', y="status",color="status",
                                      title = "Evolución status primera vaca")
    graphJSON_firstC_status = json.dumps(primer_firstC_status, cls=plotly.utils.PlotlyJSONEncoder)

    # Evolución status primer cerdo (SQL)
    primer_cerdo = animals[animals['entity_id'] == "🐖001"]
    primer_firstP_status = px.scatter(primer_cerdo, x='time_index', y="status", color="status",
                                      title = "Evolución status primer cerdo")
    graphJSON_firstP_status = json.dumps(primer_firstP_status, cls=plotly.utils.PlotlyJSONEncoder)

    ####################
    # GRÁFICAS PROPIAS #
    ####################

    # Barchart del status por animal de las granjas 
    count = animals[["entity_id", "status"]].groupby(["entity_id", "status"]).size().reset_index(name = "count")
    fig_bar = px.bar(count, x="entity_id", y = "count", color="status",
                     title="Conteo del status para cada animal de las granjas")
    graphJSON_bar = json.dumps(fig_bar, cls=plotly.utils.PlotlyJSONEncoder)

    # Boxplot pulsaciones por animal de las granjas
    fig_box = px.box(animals, x="entity_id", y="heartrate", points="all", color = "entity_id",
                     title="Boxplot pulsaciones para cada animal de las granjas")
    graphJSON_box = json.dumps(fig_box, cls=plotly.utils.PlotlyJSONEncoder)

    # Piechart del status de los tractores
    count2 = tractor[["entity_id", "status"]].groupby(["entity_id", "status"]).size().reset_index(name = "count")
    total_count2 = count2.groupby('entity_id')['count'].transform('sum')
    count2['percentage'] = (count['count'] / total_count2) * 100
    fig_pie = px.pie(count2, values="percentage", names="status", facet_col="entity_id",
                     title = "Porcentaje del status para cada tractor de las granjas")
    graphJSON_pie = json.dumps(fig_pie, cls=plotly.utils.PlotlyJSONEncoder)

    # Histograma de la humedad en cada granja
    fig_hist = px.histogram(soil, x="humidity", barmode="stack", facet_col="entity_id", color="entity_id",
                            title = "Histograma de la humedad para cada granja")
    graphJSON_hist = json.dumps(fig_hist, cls=plotly.utils.PlotlyJSONEncoder)

    # Mapa de calor del primer cerdo
    m3 = folium.Map([52.510, 13.354], zoom_start=14)
    pig001_heatMap = gdf.loc[gdf["entityId"] == "🐖001"]
    heat_data = [[row['geometry'].y, row['geometry'].x] for index, row in pig001_heatMap.iterrows()]
    HeatMap(heat_data).add_to(m3)
    iframe_heat = m3.get_root()._repr_html_()

    return render_template('home.html', 
                           # Enunciado
                           graphJSON_area = graphJSON_area,
                           graphJSON_hum = graphJSON_hum,
                           graphJSON_temp = graphJSON_temp,
                           graphJSON_firstC_status = graphJSON_firstC_status,
                           graphJSON_firstP_status = graphJSON_firstP_status,
                           iframe_last=iframe_last,
                           iframe_time = iframe_time,
                           graphJSON_P1 = graphJSON_P1,
                           graphJSON_C1 = graphJSON_C1,
                           # Propias
                           graphJSON_bar = graphJSON_bar,
                           graphJSON_box = graphJSON_box,
                           graphJSON_pie = graphJSON_pie,
                           graphJSON_hist = graphJSON_hist,
                           iframe_heat = iframe_heat
                        )