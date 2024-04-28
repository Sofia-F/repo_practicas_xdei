import requests 
from prettytable import PrettyTable

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
    responses = read_subscriptions().json()
    
    table = PrettyTable()
    table.field_names = ["description", "entities_id_pattern", "condition_attrs", "notif_http_url", "notif_attrs",
                         "notif_metadata", "throttling"]
    for response in responses:
        if "throttling" in response.keys():
            table.add_row([response["description"],
                        response["subject"]["entities"][0]["idPattern"],
                        response["subject"]["condition"]["attrs"],
                        response["notification"]["http"]["url"],
                        response["notification"]["attrs"],
                        response["notification"]["metadata"],
                        response["throttling"]])
        else:
            table.add_row([response["description"],
                    response["subject"]["entities"][0]["idPattern"],
                    response["subject"]["condition"]["attrs"],
                    response["notification"]["http"]["url"],
                    response["notification"]["attrs"],
                    response["notification"]["metadata"],
                    0])

    print(table)