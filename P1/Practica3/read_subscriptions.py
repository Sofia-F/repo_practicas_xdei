import requests 

# Lee todas las suscripciones en formato de tabla.
# Borra todas las suscripciones existentes en Orion.
def read_subscriptions():
    url = "http://localhost:1026/v2/subscriptions/"

    response = requests.request("GET", url)
    subscriptions = response.json()

    return subscriptions

if __name__ == "__main__":
    
    subscriptions = read_subscriptions()