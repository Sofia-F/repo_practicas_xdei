import psycopg
import pandas as pd
from shapely.geometry import shape
import datetime

with psycopg.connect("dbname=mtopeniot user=crate") as conn:
    with conn.cursor() as cur:

        # Animals
        cur.execute("SELECT entity_id, time_index, heartrate, location, status \
        FROM mtopeniot.etdevice ORDER BY time_index")
        tuples = cur.fetchall()
        df = pd.DataFrame(data=tuples, columns=['entity_id', 'time_index','heartrate', 'location', 'status'])
        df['time_index'] = df['time_index'].apply(datetime.datetime.isoformat)
        df['location'] = df['location'].apply(shape)
        df.to_csv('animals.csv', index=False)

        # Tractor
        cur.execute("SELECT entity_id, time_index, location, status \
        FROM mtopeniot.ettractor ORDER BY time_index")
        tuples = cur.fetchall()
        df = pd.DataFrame(data=tuples, columns=["entity_id", "time_index", "location", "status"])
        df['time_index'] = df['time_index'].apply(datetime.datetime.isoformat)
        df['location'] = df['location'].apply(shape)
        df.to_csv('tractors.csv', index=False)
        
        # Filling Level Sensor
        cur.execute("SELECT entity_id, time_index, filling, location \
        FROM mtopeniot.etfillinglevelsensor ORDER BY time_index")
        tuples = cur.fetchall()
        df = pd.DataFrame(data=tuples, columns=["entity_id", "time_index", "filling", "location"])
        df['time_index'] = df['time_index'].apply(datetime.datetime.isoformat)
        df['location'] = df['location'].apply(shape)
        df.to_csv('fillingsensor.csv', index=False)

        # Soil Sensor
        cur.execute("SELECT entity_id, time_index, humidity \
        FROM mtopeniot.etsoilsensor ORDER BY time_index")
        tuples = cur.fetchall()
        df = pd.DataFrame(data=tuples, columns=["entity_id", "time_index", "humidity"])
        df['time_index'] = df['time_index'].apply(datetime.datetime.isoformat)
        df.to_csv('soilsensor.csv', index=False)
