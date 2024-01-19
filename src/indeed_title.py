import requests

payload = {
    "source": "universal",
    "url": "https://www.indeed.com",
    "parse": True,
    "parsing_instructions": {
        "title": {"_fns": [{"_fn": "xpath_one", "_args": ["//title/text()"]}]}
    },
}

response = requests.post(
    url="https://realtime.oxylabs.io/v1/queries",
    json=payload,
    auth=("john_snow", "APIuser!123"),
)

print(response.json()["results"][0]["content"])
