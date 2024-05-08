import psycopg
import pandas as pd
from shapely.geometry import shape
import datetime

with psycopg.connect("dbname=mtopeniot user=crate") as conn:
    with conn.cursor() as cur:
        cur.execute("SELECT entity_id, time_index, heartrate, location, status \
        FROM mtopeniot.etdevice ORDER BY time_index")
        tuples = cur.fetchall()
        df = pd.DataFrame(data=tuples, columns=['entity_id', 'time_index','heartrate', 'location', 'status'])
        df['time_index'] = df['time_index'].apply(datetime.datetime.isoformat)
        df['location'] = df['location'].apply(shape)
        df.to_csv('animals.csv', index=False)