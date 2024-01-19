"""parse_jobs.py"""
import json
import requests
import pandas as pd

payload = {}
with open("job_search_payload.json", encoding="utf-8") as f:
    payload = json.load(f)

response = requests.post(
    url="https://realtime.oxylabs.io/v1/queries",
    json=payload,
    auth=("username", "password"),
    timeout=180,
)

print(response.status_code)


with open("result.json", "w", encoding="utf-8") as f:
    json.dump(response.json(), f, indent=4)


# save results into a variable data
data = response.json()
# save the indeed data as a json file

with open("results.json", "w") as f:
    json.dump(data, f, indent=4)
df = pd.DataFrame(data["results"][0]["content"]["job_listings"])
df.to_csv("job_search_results.csv", index=False)
