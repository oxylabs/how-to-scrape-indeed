import requests

payload = {"source": "universal", "url": "https://www.imdb.com"}

response = requests.post(
    url="https://realtime.oxylabs.io/v1/queries",
    json=payload,
    auth=("username", "password"),
)

print(response.json())
