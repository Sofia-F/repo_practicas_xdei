import requests 
from prettytable import PrettyTable

def read_subscriptions():

    url = 'http://localhost:1026/ngsi-ld/v1/subscriptions/'

    payload = {}
    headers = {
    'NGSILD-Tenant': 'openiot'
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    return response

if __name__ == "__main__":
    
    print("\nReading subscriptions...")
    responses = read_subscriptions().json()
    print(responses)
