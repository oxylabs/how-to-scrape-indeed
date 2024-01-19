# How to Scrape Indeed

[![Oxylabs promo code](https://user-images.githubusercontent.com/129506779/250792357-8289e25e-9c36-4dc0-a5e2-2706db797bb5.png)](https://oxylabs.go2cloud.org/aff_c?offer_id=7&aff_id=877&url_id=112)

Here's the process of extracting job postings from [Indeed](https://www.indeed.com/) with the help of Oxylabs [Web Scraper API](https://oxylabs.io/products/scraper-api/web) (**1-week free trial**) and Python.

For the complete guide with in-depth explanations and visuals, check our [blog post](https://oxylabs.io/blog/how-to-scrape-indeed).

## Project setup

### Creating a virtual environment

```python
python -m venv indeed_env #Windows
python3 -m venv indeed_env #Macand Linux
```

### Activating the virtual environment

```python
.\indeed_env\Scripts\Activate#Windows
source indeed_env/bin/activate #Macand Linux
```

### Installing libraries

```python
$ pip install requests
```

## Overview of Web Scraper API

The following is an example that shows how Web Scraper API works.

```python
# scraper_api_demo.py
import requests
payload = {
    "source": "universal",
    "url": "https://www.indeed.com"
}
response = requests.post(
    url="https://realtime.oxylabs.io/v1/queries",
    json=payload,
    auth=(username,password),
)
print(response.json())
```

## Web Scraper API parameters

### Parsing the page title and retrieving results in JSON

```python
"title": {
    "_fns": [
                {
                    "_fn": "xpath_one",
                    "_args": ["//title/text()"]
                }
            ]
        }
},
```

If you send this as `parsing_instructions`, the output would be the following JSON.

```python
{ "title": "Job Search | Indeed", "parse_status_code": 12000 }
```

Note that the `parse_status_code` means a successful response.

The following code prints the title of the Indeed page.

```python
# indeed_title.py

import requests
payload = {
    "source": "universal",
    "url": "https://www.indeed.com",
    "parse": True,
    "parsing_instructions": {
        "title": {
            "\_fns": [
                        {
                            "\_fn": "xpath_one",
                            "\_args": [
                                "//title/text()"
                                ]
                        }
                    ]
                }
    },
}
response = requests.post(
    url="https://realtime.oxylabs.io/v1/queries",
    json=payload,
    auth=('username', 'password'),
)
print(response.json()['results'][0]['content'])
```

## Scraping Indeed job postings

### Selecting a job listing

```python
`.job_seen_beacon`
```

### Creating the placeholder for a job listing

```
"job_listings": {
    "_fns": [
        {
            "_fn": "css",
            "_args": [".job_seen_beacon"]
        }
    ],
    "_items": {
        "job_title": {
            "_fns": [
                {
                "_fn": "xpath_one",
                "_args": [".//h2[contains(@class,'jobTitle')]/a/span/text()"]
                }
            ]
        },
        "company_name": {
            "_fns": [
                {
                    "_fn": "xpath_one",
                    "_args": [".//span[@data-testid='company-name']/text()"]
                }
            ]
        },
```

### Adding other selectors

```json
{
  "source": "universal",
  "url": "https://www.indeed.com/jobs?q=work+from+home&l=San+Francisco%2C+CA",
  "parse": true,
  "parsing_instructions": {
    "job_listings": {
      "_fns": [
        {
          "_fn": "css",
          "_args": [".job_seen_beacon"]
        }
      ],
      "_items": {
        "job_title": {
          "_fns": [
            {
              "_fn": "xpath_one",
              "_args": [".//h2[contains(@class,'jobTitle')]/a/span/text()"]
            }
          ]
        },
        "company_name": {
          "_fns": [
            {
              "_fn": "xpath_one",
              "_args": [".//span[@data-testid='company-name']/text()"]
            }
          ]
        }
      }
    }
  }
}
```

For other data points, see the file [here](src/job_search_payload.json).

### Saving the payload as a separator JSON file

```python
# parse_jobs.py

import requests
import json
payload = {}
with open("job_search_payload.json") as f:
    payload = json.load(f)
response = requests.post(
    url="https://realtime.oxylabs.io/v1/queries",
    json=payload,
    auth=("username", "password"),
)
print(response.status_code)
with open("result.json", "w") as f:
    json.dump(response.json(), f, indent=4)
```

## Exporting to JSON and CSV

```python
# parse_jobs.py
with open("results.json", "w") as f:
    json.dump(data, f, indent=4)
df = pd.DataFrame(data["results"][0]["content"]["job_listings"])
df.to_csv("job_search_results.csv", index=False)
```

## Final word

Check our [documentation](https://developers.oxylabs.io/scraper-apis/web-scraper-api) for more API parameters and variables found in this tutorial.

If you have any questions, feel free to contact us at support@oxylabs.io.
