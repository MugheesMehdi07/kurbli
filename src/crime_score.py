import json
import urllib.parse
import urllib3
import logging
from utils import *

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Define CORS headers
cors_headers = {
    'Content-Type': 'application/json',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': '*'
}

def normalize_crime_rate(neighborhood_crime_rating):
    """Normalize the crime rate to a value between 1-10 for scoring purposes using a linear formula."""
    try:
        crime_rate = float(neighborhood_crime_rating)
    except ValueError:
        return None

    # Calculate the score based on the crime rate
    score = 11 - (crime_rate // 100)

    # Clamp the score to be within 1 to 10
    return max(1, min(10, score))


def fetch_community_profile(geoIdV4):
    http = urllib3.PoolManager()

    params = {"geoIdV4": geoIdV4}
    headers = {"apikey": ATOM_API_KEY}
    encoded_params = urllib.parse.urlencode(params)

    url = f"{CRIME_PROFILE_URL}?{encoded_params}"

    try:
        response = http.request('GET', url, headers=headers)
        # Decode the JSON response
        response_data = json.loads(response.data.decode('utf-8'))

        # Navigate through the nested JSON to reach the crime section
        crime_data = response_data.get('community', {}).get('crime', {})

        # Extract the "crime_Index" which can be considered as the "Neighborhood Crime Rating"
        neighborhood_crime_rating = crime_data.get('crime_Index', 'No data available')

        logger.info("Neighborhood Crime Rating: %s", neighborhood_crime_rating)

        return normalize_crime_rate(neighborhood_crime_rating)

    except urllib3.exceptions.HTTPError as e:
        logger.error("HTTP error occurred: %s", e)  # Handle specific HTTP errors
    except Exception as e:
        logger.error("An error occurred: %s", e)  # Handle other possible errors


def lambda_handler(event, context):
    response = {
        "statusCode": 200,
        'headers': cors_headers,
        "body": ""
    }
    try:
        logger.info("Received event: %s", event)
        geoIdV4 = event.get('queryStringParameters', {}).get('geo_id', '')
        if not geoIdV4:
            response["statusCode"] = 400
            response["body"] = json.dumps({"error": "geoIdV4 parameter is required"})
        else:
            normalized_crime_rate = fetch_community_profile(geoIdV4)
            if normalized_crime_rate is not None:
                response["body"] = json.dumps({"crime_score": normalized_crime_rate})
            else:
                response["statusCode"] = 500
                response["body"] = json.dumps({"error": "Failed to fetch crime score"})

    except Exception as e:
        logger.error("An error occurred: %s", e)
        response["statusCode"] = 500
        response["body"] = json.dumps({"error": "An error occurred while processing the request"})

    return response


# # Test the lambda_handler function
event =  {
    "queryStringParameters": {
        "geo_id": "9fc63b98ee04811a9c931d3e99a91ac0"
    }
}
context = {}
print(lambda_handler(event, context))
