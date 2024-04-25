import json
import urllib3
import urllib.parse
import logging
from utils import *

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def normalize_cap_rate(cap_rate):
    """Normalize the cap rate to a value between 1-30 for scoring purposes."""
    normalized_cap_rate = (cap_rate * 100) / 3.33  # Normalize the cap rate to a value between 1-30
    return max(1, min(30, normalized_cap_rate))  # Clamp the score to be within 1 to 30


def fetch_batchdata_property_lookup(api_token, data):
    http = urllib3.PoolManager()
    url = BATCH_URL
    headers = {
        "Accept": "application/json",
        "Authorization": f"Bearer {api_token}",
        "Content-Type": "application/json"
    }
    try:
        # Send the POST request with JSON data
        response = http.request('POST', url, headers=headers, body=json.dumps({"requests": [{"address": data}]}))
        if response.status == 200:
            return json.loads(response.data.decode('utf-8'))
        else:
            logger.error("Error fetching BatchData: %s", response.status)
            return None
    except Exception as e:
        logger.error("Error occurred during BatchData fetch: %s", e)
        return None


def calculate_cap_score(data):
    batchdata_api_token = BATCH_API_KEY
    response = fetch_batchdata_property_lookup(
        api_token=batchdata_api_token,
        data=data
    )

    logger.info("BatchData Property Lookup: %s", response)

    if not response or 'results' not in response or not response['results']['properties']:
        return {"error": "No property data found"}

    property_info = response['results']['properties'][0]
    market_value = property_info['valuation']['estimatedValue']
    monthly_rental_estimate = 2000

    gross_annual_rent = monthly_rental_estimate * 12
    annual_expenses = market_value * 0.05
    net_income = gross_annual_rent - annual_expenses
    cap_rate = net_income / market_value

    logger.info("Cap Rate: %s", cap_rate)

    return normalize_cap_rate(cap_rate)


def lambda_handler(event, context):
    response = {
        "statusCode": 200,
        'headers': {
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': '*'
        },
        "body": ""
    }
    try:
        logger.info("Received event: %s", event)
        data = event.get('queryStringParameters', {}).get('address', '')
        data = urllib.parse.unquote(data)
        address = get_address(data)

        if not data:
            response["statusCode"] = 400
            response["body"] = json.dumps({"error": "Data parameter is required"})
        else:
            cap_score = calculate_cap_score(address)
            response["body"] = json.dumps({"cap_score": cap_score})

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
# context = {}
# print(lambda_handler(event, context))

