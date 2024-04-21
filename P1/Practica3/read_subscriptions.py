import requests 
import pandas as pd

def read_subscriptions():

    url = "http://localhost:1026/v2/subscriptions/"

    payload = {}
    headers = {
    'fiware-service': 'openiot',
    'fiware-servicepath': '/'
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    return response

if __name__ == "__main__":
    
    print("\nReading subscriptions...")
    response = pd.DataFrame(read_subscriptions().json())
    print()
    print(response)
    print(read_subscriptions().json())