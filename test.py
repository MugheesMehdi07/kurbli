import json

import requests
import urllib3

from src.utils import BATCH_SEARCH_URL, BATCH_API_KEY

# URL and parameter
url = 'https://api.sfranalytics.com/api/v1/property/best-buyers'
params = {

            "searchCriteria": {

                "quickList": "not-owner-occupied",

                "general": {

                    "propertyTypeDetail": {

                        "inList": [

                            "Single Family",

                            "Single Family Residential"

                        ]

                    }

                },

                "compAddress": {

                    "street": "1600 jamaica st",
                    "city": "titusville",
                    "state": "FL",
                    "zip": "32780"

                }

            },

            "options": {

                "useDistance": 'true',

                "distanceMiles": 2,

                "skip": 0,

            }

        }

# Headers
def fetch_batchdata_property_lookup():
    http = urllib3.PoolManager()
    url = BATCH_SEARCH_URL
    headers = {
        "Accept": "application/json",
        "Authorization": f"Bearer {BATCH_API_KEY}",
        "Content-Type": "application/json"
    }
    try:
        # Send the POST request with JSON data
        response = http.request('POST', url, headers=headers, body=json.dumps(params))
        if response.status == 200:
            print(response.data)
            return json.loads(response.data.decode('utf-8'))
        else:
            # logger.error("Error fetching BatchData: %s", response.status)
            print(response)
            return None
    except Exception as e:
        # logger.error("Error occurred during BatchData fetch: %s", e)
        print(e)
        return None

result = fetch_batchdata_property_lookup()
print(len(result['results']['properties']))