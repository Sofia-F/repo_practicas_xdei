import requests
import json

def create_subs(Description, Subject, Notification, Throttling = None):
    url = "http://localhost:1026/v2/subscriptions/"

    payload = {
        "description": Description,
        "subject": Subject,
        "notification": Notification
    }

    if Throttling is not None:
        payload["throttling"] = Throttling

    headers = {
        'Content-Type': 'application/json',
        'fiware-service': 'openiot',
        'fiware-servicepath': '/'
    }

    response = requests.request("POST", url, headers=headers, data=json.dumps(payload))

    return response.status_code

if __name__ == "__main__":

    Description = ["Notify QuantumLeap of all Motion Sensor count changes",
                   "Notify QuantumLeap of all Door state changes",
                   "Notify QuantumLeap of all Lamp luminosity and location every 5 seconds"]
    Subject = [
        {
            "entities": [{"idPattern": "Motion.*"}],
            "condition": {"attrs": ["count"]}
        },
        
        {
            "entities": [{"idPattern": "Door.*"}],
            "condition": {"attrs": ["state"]}
        },

        {
            "entities": [{"idPattern": "Lamp.*"}],
            "condition": {"attrs": ["luminosity", "location"]}
        },
    ]

    Notification = [
        {
            "http": {"url": "http://quantumleap:8668/v2/notify"},
            "attrs": ["count"],
            "metadata": ["dateCreated", "dateModified"]
        },

        {
            "http": {"url": "http://quantumleap:8668/v2/notify"},
            "attrs": ["state"],
            "metadata": ["dateCreated", "dateModified"]
        },

        {
            "http": {"url": "http://quantumleap:8668/v2/notify"},
            "attrs": ["luminosity", "location"],
            "metadata": ["dateCreated", "dateModified"]
        }
    ]

    Throttling = [None, None, 5]

    print("Creating subscriptions ...")
    for i in range(len(Description)):
        if Subject[i]["entities"][0]["idPattern"] == "Lamp.*":
            for id in ["001", "002", "003", "004"]:
                Subject[i]["entities"][0]["idPattern"] = "Lamp"+id
                status = create_subs(Description[i], Subject[i], Notification[i], Throttling[i])
        else:
            status = create_subs(Description[i], Subject[i], Notification[i], Throttling[i])
    print(status)