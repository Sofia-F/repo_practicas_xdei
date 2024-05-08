import requests
import json

def create_subscription(Description, Entity_type, Watched_attrs, Notification_attrs):
    url = "http://localhost:1026/ngsi-ld/v1/subscriptions/"

    payload = json.dumps({
    "description": Description,
    "type": "Subscription",
    "entities": [
        {
        "type": Entity_type
        }
    ],
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
    },
    "@context": "http://context/ngsi-context.jsonld"
    })
    headers = {
    'Content-Type': 'application/ld+json',
    'NGSILD-Tenant': 'openiot'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    return response.status_code

if __name__ == "__main__":

    Description = ["Notify me of all feedstock changes",
                   "Notify me of all temperature and humidity changes",
                   "Notify me of all temperature and humidity changes",
                   "Notify me of all status and location changes",
                   "Notify me of all status and location changes"]
    
    Entity_type = ["FillingLevelSensor",
                   "TemperatureSensor",
                   "SoilSensor",
                   "Tractor",
                   "Device"]

    Watched_attrs = [["filling"],
                    ["temperature", "humidity"],
                    ["temperature", "humidity"],
                    ["status"],
                    ["location", "status", "heartRate"]
                    ]

    Notification_attrs = [["filling","location"],
                         ["temperature","humidity"],
                         ["temperature","humidity"],
                         ["status","location"],
                         ["location", "status", "heartRate"]]

    print("Creating subscriptions ...")
    for i in range(len(Description)):
        status = create_subscription(Description[i], Entity_type[i],
                                        Watched_attrs[i], Notification_attrs[i])
        print(status)