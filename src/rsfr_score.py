import json
import urllib3
from urllib.parse import urlencode

from utils import *  # Ensure this module provides ATOM_API_KEY

def rsfr_score(latitude, longitude):
    http = urllib3.PoolManager()

    params = {
        "latitude": latitude,
        "longitude": longitude,
        "radius": 2,
        "propertytype": "sfr",
        # "ownerOccupied": "false",  # Uncomment if this parameter is needed
    }
    headers = {
        "apikey": ATOM_API_KEY
    }
    encoded_params = urlencode(params)
    url_with_params = f"{SFR_PROFILE_URL}?{encoded_params}"

    try:
        response = http.request('GET', url_with_params, headers=headers)
        if response.status == 200:
            score = json.loads(response.data.decode('utf-8'))['status']['total']
            print("R SFR Score:", score)
            return score
        else:
            print("Failed to fetch property snapshot:", response.status, response.data.decode('utf-8'))
            return None
    except Exception as e:
        print("Failed to fetch property snapshot:", str(e))
        return None

def lambda_handler(event, context):
    query_params = event.get('queryStringParameters', {})
    latitude = query_params.get('latitude')
    longitude = query_params.get('longitude')
    if latitude is None or longitude is None:
        return {
            "statusCode": 400,
            "body": json.dumps({"error": "Both latitude and longitude parameters are required"})
        }

    score = rsfr_score(latitude, longitude)
    return {
        "statusCode": 200,
        "body": json.dumps({"r_sfr_score": score})
    }

# Test the lambda_handler function
event = {
    "queryStringParameters": {"longitude": "-105.047775", "latitude": "39.778926"}
}
context = {}
print(lambda_handler(event, context))
