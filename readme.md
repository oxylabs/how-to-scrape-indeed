# How to Scrape Indeed
  - [Introduction](#introduction)
  - [Why Scrape Indeed?](#why-scrape-indeed)
  - [The Tool: Oxylabs’ Web Scraper API](#the-tool-oxylabs-web-scraper-api)
  - [Project Setup](#project-setup)
  - [Overview of Web Scraper API](#overview-of-web-scraper-api)
  - [Scraper API Parameters](#scraper-api-parameters)
  - [Scraping Indeed Job Postings](#scraping-indeed-job-postings)
  - [Exporting to JSON and CSV](#exporting-to-json-and-csv)
  - [Conclusion](#conclusion)

## Introduction

In an era where data drives decisions, accessing up-to-date job market information is crucial. Indeed.com, a leading job portal, offersextensive insights into job openings, popular roles, and company hiring trends.However, manually collecting this job data can be tedious and time-consuming.This is where web scraping comes in as a game-changer, and Oxylabs' Web ScraperAPI makes this task seamless, efficient, and reliable.

## Why Scrape Indeed?

Scraping Indeed.com allows businesses, analysts, and jobseekers to stay ahead in the competitive job market. From tracking the mostpopular jobs to understanding industry demands, the insights gained from jobpostings and job details on Indeed are invaluable. Automated data collectionthrough scraping not only saves time but also provides a more comprehensiveview of the job landscape. Job scraping is a technique widely used by HRprofessionals

## The Tool: Oxylabs’ Web Scraper API

Oxylabs' Web Scraper API is designed to handle complex webscraping tasks with ease. It bypasses anti-bot measures, ensuring you get thejob data you need without interruption. Whether you're looking to scrape jobtitles, company names, or detailed job descriptions, Oxylabs simplifies theprocess.

This step-by-step tutorial will guide you through scraping job postings from Indeed.com, focusing on extracting key jobdetails like job titles, descriptions, and company names.

## Project Setup

#### Prerequisites

Before diving into the code to scrape indeed, ensure youhave Python 3.8 or newer installed on your machine. This guide is written forPython 3.8+, so having a compatible version is crucial.

#### Creating a Virtual Environment

A virtual environment is an isolated space where you caninstall libraries and dependencies without affecting your global Python setup.It's a good practice to create one for each project. Here's how to set it up ondifferent operating systems:
python -m venv indeed_env #Windows
python3 -m venv indeed_env #Macand Linux
Replace indeed_env with the name you'd like to give to yourvirtual environment.

#### Activating the Virtual Environment

Once the virtual environment is created, you'll need toactivate it:
.\indeed_env\Scripts\Activate#Windows
source indeed_env/bin/activate #Macand Linux
You should see the name of your virtual environment in theterminal, indicating that it's active.

#### Installing Required Libraries

We'll use the requests library for this project to make HTTPrequests. Install it by running the following command:
$ pip install requests
And there you have it! Your project environment is ready forIMDb data scraping using Oxylabs' IMDb Scraper API. In the following sections,look into the Indeed structure.

## Overview of Web Scraper API

Oxylabs' [WebScraper API](https://oxylabs.io/products/scraper-api/web) allows you to extract data from many complex websiteseasily.
The following is a minimal example that shows how ScraperAPI works.

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

As you can see, the payload is where you would inform theAPI what and how you want to scrape.
Save this code in a file scraper_api_demo.py and run it. Youwill see that the entire HTML of the page will be printed, along with someadditional information from Scraper API.
In the following section, let's examine various parameterswe can send in the payload.

## Scraper API Parameters

The most critical parameter is **source**. For IMDb, setthe source as universal, a general-purpose source that can handle all domains.
The parameter **url** is self-explanatory, a direct linkto the page you want to scrape.
The example code in the earlier section has only these twoparameters. The result is, however, the entire HTML of the page.
Instead, what we need is parsed data. This is where theparameter parse comes into the picture. When you send parse as True, you mustalso send one more parameter —**parsing_instructions**.

Combined, these twoparameters allow you to get parsed data in any structure you like.
The following barse minimum allows you to get a JSON to getthe page title:

```json
"title": {
    "\_fns": [
                {
                    "\_fn": "xpath_one",
                    "\_args": ["//title/text()"]
                }
            ]
        }
}
```

If you send this as `parsing_instructions`, the outputwould be the following JSON:

```json
{ "title": "Job Search | Indeed", "parse_status_code": 12000 }
```

Note that the `parse_status_code` means a successful response.

The key **\_fns** indicates a list of functions, which cancontain one or more functions indicated by the `\_fn` key, along withthe arguments.

In this example, the function is **xpath_one**, whichtakes an XPath and returns one matching element. On the other hand, thefunction **xpath** returns all matching elements.

On similar lines are **css_one** and **css** functionsthat use CSS selectors instead of XPath.

For a complete list of available functions, see the [Scrpaer API documentation](https://developers.oxylabs.io/scraper-apis/custom-parser/list-of-functions).
The following code prints the title of the Indeed page:

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

Run this file to get the title of Indeed.

In the next section, we will scrape jobs from a list.

## Scraping Indeed Job Postings

Before scraping a page, we need to examine the pagestructure.
Open the [Job search results](https://www.indeed.com/jobs?q=work+from+home&l=San+Francisco%2C+CA) in Chrome, right-click the joblisting, and select **Inspect**.
Move around your mouse until you can precisely select one joblist item and related data.

![](images/indeed_css_selector.png)

You can use the following CSS selector to select one job listing:

`.job_seen_beacon`

We can iterate over each matching item and get the specific jobdata points such as job title, company name, location, salalry range, dateposted, and job description.
First, create the placeholder for job listing as follows:

```
"job_listings": {
    "\_fns": [
        {
            "\_fn": "css",
            "\_args": [".job_seen_beacon"]
        }
    ],
```
    
Note the use of the function css. It means that it willreturn all matching elements.
Next, we can use reserved property **\_items** to indicatethat we want to iterate over a list, further processing each list itemseparately.
It will allow us to use concatenating to the path alreadydefined as follows:

```
"job_listings": {
    "\_fns": [
        {
            "\_fn": "css",
            "\_args": [".job_seen_beacon"]
        }
    ],
    "\_items": {
        "job_title": {
            "\_fns": [
                {
                "\_fn": "xpath_one",
                "\_args": [".//h2[contains(@class,'jobTitle')]/a/span/text()"]
                }
            ]
        },
        "company_name": {
            "\_fns": [
                {
                    "\_fn": "xpath_one",
                    "\_args": [".//span[@data-testid='company-name']/text()"]
                }
            ]
        },
```

Similarly, we can add other selectors. After adding otherdetails, here are the job_search_payload.json partial file contents:

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

For other data points, see the [file here](src/job_search_payload.json).

A good way to organize your code is to save the payload as aseparator JSON file. It will allow you to keep your Python file as short as follows:

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

![](images/indeed_code_exectution.png)

## Exporting to JSON and CSV

The output of Scraper API is a JSON. You can save theextracted job listing as JSON directly.
You can use a library such as Pandas to save the job data asCSV.
Remember that the parsed data are stored in the **content** inside **results**.
As we created the job listings in the key job_listings, wecan use the following snippet to save the extracted indeed data:

```python
# parse_jobs.py
with open("results.json", "w") as f:
    json.dump(data, f, indent=4)
df = pd.DataFrame(data["results"][0]["content"]["job_listings"])
df.to_csv("job_search_results.csv", index=False)
```

## Conclusion

Web Scraper API makes web scraping very easy. You can useany language you like, and all you need to do is send the correct payload.

You can even use GUI tools such as Postman or Insomnia toscrape data. All you need to do is send a post request to the API with thedesired payload. The detailed documentation on Web Scraper API is available [here](https://developers.oxylabs.io/scraper-apis/web-scraper-api). You can also [try Web Scraper API](https://oxylabs.io/products/scraper-api/web/imdb) for free.
