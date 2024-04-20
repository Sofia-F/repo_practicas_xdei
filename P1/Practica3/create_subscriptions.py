# Crea una suscripcion en Orion

import requests
import json
import pandas as pd

def read_subscriptions():

    url = "http://localhost:1026/v2/subscriptions/"

    payload = {}
    headers = {
    'fiware-service': 'openiot',
    'fiware-servicepath': '/'
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    df = pd.DataFrame(response.json())

    if df.empty:
        return "No active subscriptions"
    else:
        return df[['id', 'description', 'status']]

def create_subscription(Description, Subject, Notification, Throttling = None):
    url = "http://localhost:1026/v2/subscriptions/"

    payload = json.dumps({
    "description": Description,
    "subject": Subject,
    "notification": Notification
    })

    if Throttling is not None:
        payload["throttling"] = Throttling

    headers = {
    'Content-Type': 'application/json',
    'fiware-service': 'openiot',
    'fiware-servicepath': '/'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    return response.status_code

def delete_subscriptions():
    url = "http://localhost:1026/v2/subscriptions/"

    headers = {
        'fiware-service': 'openiot',
        'fiware-servicepath': '/'
    }

    registrations = requests.request("GET", url, headers=headers).json()

    for registration in registrations:
        url = "http://localhost:1026/v2/subscriptions/"+registration["id"]
        response = requests.request("DELETE", url, headers=headers)

    return response.status_code

def delete_subscription(id):
    url = "http://localhost:1026/v2/subscriptions/"

    headers = {
        'fiware-service': 'openiot',
        'fiware-servicepath': '/'
    }

    registrations = requests.request("GET", url, headers=headers).json()

    for registration in registrations:
        if registration["id"] == id:
            url = "http://localhost:1026/v2/subscriptions/"+registration["id"]
            response = requests.request("DELETE", url, headers=headers)

            return response.status_code
        else:
            return "Failed to delete"

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

    print("Creating subscriptions ...")
    i = 2
    status = create_subscription(Description[i], Subject[i], Notification[i])
    print(status)

    print("\nReading subscriptions...")
    response = read_subscriptions()
    print(response)

    print("\nDeleting subscriptions...")
    status = delete_subscriptions()

    print("\nReading subscriptions...")
    response = read_subscriptions()
    print(response)


