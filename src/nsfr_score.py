import json
import urllib3
from urllib.parse import urlencode
import logging
from utils import ATOM_API_KEY, SFR_PROFILE_URL

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
def normalize_score(score):
    """Normalize the score between 1 and 20."""
    if score is None:
        return None
    normalized_score = ((score - 1) / (20 - 1)) * (20 - 1) + 1
    return max(1, min(20, normalized_score))


def nsfr_score(latitude, longitude):
    http = urllib3.PoolManager()
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "radius": 2,
        "propertytype": "SFR",
        # "ownerOccupied": "false",  # Uncomment if used
    }
    headers = {
        "apikey": ATOM_API_KEY
    }
    encoded_params = urlencode(params)
    url = f"{SFR_PROFILE_URL}?{encoded_params}"

    try:
        response = http.request('GET', url, headers=headers)
        if response.status == 200:
            score = json.loads(response.data.decode('utf-8'))['status']['total']
            logger.info("N SFR Score: %s", score)

            return normalize_score(int(score))
        else:
            logger.error("Failed to fetch property snapshot: %s %s", response.status, response.data.decode('utf-8'))
            return None
    except Exception as e:
        logger.error("Failed to fetch property snapshot: %s", str(e))
        return None

def lambda_handler(event, context):
    response = {
        "statusCode": 200,
        "headers": cors_headers,
        "body": ""
    }
    try:
        logger.info("Received event: %s", event)
        query_params = event.get('queryStringParameters', {})
        latitude = query_params.get('latitude')
        longitude = query_params.get('longitude')
        if latitude is None or longitude is None:
            response["statusCode"] = 400
            response["body"] = json.dumps({"error": "Both latitude and longitude parameters are required"})
        else:
            score = nsfr_score(latitude, longitude)
            if score is not None:
                response["body"] = json.dumps({"n_sfr_score": score})
            else:
                response["statusCode"] = 500
                response["body"] = json.dumps({"error": "Failed to fetch N SFR score"})
    except Exception as e:
        logger.error("An error occurred: %s", e)
        response["statusCode"] = 500
        response["body"] = json.dumps({"error": "An error occurred while processing the request"})

    return response

# Test the lambda_handler function
# event = {
#     "queryStringParameters": {
#         "latitude": 34.0522,
#         "longitude": -118.2437
#     }
# }
# context = {}
# print(lambda_handler(event, context))
