import json
import urllib.parse
import urllib3
import logging
from utils import *

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def lambda_handler(event, context):
    try:
        logger.info("Received event: %s", event)

        # Initialize response object
        response = {
            "statusCode": 200,
            'headers': {
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': '*'
            },
            "body": ""
        }

        # Parse the incoming JSON from event
        data = event.get('queryStringParameters', {}).get('address', '')
        data = urllib.parse.unquote(data)

        logger.info("Received address: %s", data)

        headers = {"apikey": ATOM_API_KEY}

        params = {
            "address": data
        }

        logger.info("Request parameters: %s", params)

        # Create a PoolManager instance
        http = urllib3.PoolManager()
        encoded_params = urllib.parse.urlencode(params)
        url = f"{BASIC_PROFILE_URL}?{encoded_params}"

        logger.info("Request URL: %s", url)

        # Perform HTTP GET request with params in the URL
        http_response = http.request(
            'GET',
            url,
            headers=headers
        )

        # Decode the JSON response
        response_data = json.loads(http_response.data.decode('utf-8'))

        logger.info("Response data: %s", response_data)

        # Extract required information from response
        geo_id = response_data['property'][0]['location']['geoIdV4']['CO']
        longitude = response_data['property'][0]['location']['longitude']
        latitude = response_data['property'][0]['location']['latitude']

        response["body"] = json.dumps({"geo_id": geo_id, "longitude": longitude, "latitude": latitude})

    except Exception as e:
        logger.error("Failed to fetch property info: %s", e)
        response["statusCode"] = 500
        response["body"] = json.dumps({"error": "Property not found"})

    return response


# Test the lambda_handler function
# event = {
#     "queryStringParameters": {
#         "address": "4529 Winona Ct, Denver, CO 80212"
#     }
# }
#
# context = {}
# print(lambda_handler(event, context))
