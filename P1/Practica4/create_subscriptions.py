import requests
import json

def create_subscription(Description, Entity_type, Watched_attrs, Notification_attrs, Throttling):
    url = "http://localhost:1026/ngsi-ld/v1/subscriptions/"

    payload_dict = {
    "description": Description,
    "type": "Subscription",
    "entities":  Entity_type
    ,
    "watchedAttributes": Watched_attrs,
    "notification": {
        "attributes": Notification_attrs,
        "format": "normalized",
        "endpoint": {
            "uri": "http://quantumleap:8668/v2/notify",
            "accept": "application/json",
            "receiverInfo": [{
                "key": "fiware-service",
                "value": "openiot"
        }]
        }
    }
    }

    if Throttling > 0:
        payload_dict["throttling"] = int(Throttling)

    payload = json.dumps(payload_dict)
    headers = {
        'Content-Type': 'application/json',
        'NGSILD-Tenant': 'openiot',
        'fiware-servicepath': '/',
        'Link': '<http://context/ngsi-context.jsonld>; rel="http://www.w3.org/ns/json-ld#context"; type="application/ld+json"'
    }

    print(payload)
    response = requests.request("POST", url, headers=headers, data=payload)

    return response.status_code

if __name__ == "__main__":

    Description = ["Notify me of all feedstock changes",
                   "Notify me of all temperature and humidity changes",
                   "Notify me of all status and location changes",
                   "Notify me of animal locations"]
    
    Entity_type = [[{"type": "FillingLevelSensor"}],
                   [{"type": "SoilSensor"}, 
                    {"type": "TemperatureSensor"}],
                   [{"type": "Tractor"}],
                   [{"type": "Device"}]]

    Watched_attrs = [["filling"],
                    ["temperature", "humidity"],
                    ["status", "location"],
                    ["location", "status", "heartRate"]]

    Notification_attrs = [["filling","location"],
                         ["temperature", "humidity"],
                         ["status","location"],
                         ["location", "status", "heartRate"]]

    Throttling = [0,0,0,10]

    print("Creating subscriptions ...")
    for i in range(len(Description)):
        status = create_subscription(Description[i], Entity_type[i],
                                        Watched_attrs[i], Notification_attrs[i],
                                        Throttling[i])
        print(status)
