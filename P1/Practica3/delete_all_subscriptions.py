import requests

# Borra todas las suscripciones existentes en Orion.
def delete_subscriptions():
    url = "http://localhost:1026/v2/subscriptions/"

    response = requests.request("GET", url)
    registrations = response.json()

    for registration in registrations:
        url = "http://localhost:1026/v2/registrations/"+registration["id"]
        response = requests.request("DELETE", url)

# Borra una suscripcion
def delete_subscription(id):
    url = "http://localhost:1026/v2/subscriptions/"

    response = requests.request("GET", url)
    registrations = response.json()

    for registration in registrations:
        print(registration["dataProvided"]["entities"][0]["id"])
        if registration["dataProvided"]["entities"][0]["id"] == id:
            url = "http://localhost:1026/v2/registrations/"+registration["id"]
            response = requests.request("DELETE", url)

    return response.status_code

if __name__ == "__main__":

    id = "id"
    delete_subscriptions()
    delete_subscription(id)