import requests

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

if __name__ == "__main__":

    print("\nDeleting subscriptions...")
    status = delete_subscriptions()