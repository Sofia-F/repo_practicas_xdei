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

        df = pd.DataFrame(data=tuples, 
                          columns=['entity_id', "time_index",
                                    'heartrate', 'location', 'status'])
        for i in range(len(df)):
            dt_str = datetime.datetime.fromisoformat(df['time_index'].iloc[i])
            df['time_index'].iloc[i] = datetime.datetime.isoformat(dt_str)
            df['location'] = shape(df['location'].iloc[i])
            
        df.to_csv('animals.csv', index=False)