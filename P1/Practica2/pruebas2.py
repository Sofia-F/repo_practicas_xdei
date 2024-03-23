import requests

url = "http://localhost:3000/health/weather"

payload = {}
files={}
headers = {}

response = requests.request("GET", url, headers=headers, data=payload, files=files)

print(response.text)