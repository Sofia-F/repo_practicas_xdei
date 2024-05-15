import requests

def delete_subscriptions():
    url = 'http://localhost:1026/ngsi-ld/v1/subscriptions/'

    headers = {
        'NGSILD-Tenant': 'openiot'
    }
    subscriptions = requests.request("GET", url, headers=headers).json()

    for subscription in subscriptions:
        url = "http://localhost:1026/ngsi-ld/v1/subscriptions/"+subscription["id"]
        response = requests.request("DELETE", url, headers=headers)

    return response.status_code

if __name__ == "__main__":

    print("\nDeleting subscriptions...")
    status = delete_subscriptions()
    print(status)