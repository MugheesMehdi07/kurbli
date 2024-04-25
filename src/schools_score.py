import json
import urllib.parse
import urllib3
import logging
from utils import *

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def calculate_overall_rating(schools):
    rating_values = {
        'A+': 4.33, 'A': 4.0, 'A-': 3.67,
        'B+': 3.33, 'B': 3.0, 'B-': 2.67,
        'C+': 2.33, 'C': 2.0, 'C-': 1.67,
        'D+': 1.33, 'D': 1.0, 'D-': 0.67,
        'F': 0
    }

    total_score = 0
    count = 0

    for school in schools:
        try:
            rating = school['detail']['schoolRating'].strip()
            if rating in rating_values:
                total_score += rating_values[rating]
                count += 1
        except KeyError:
            continue  # Pass if school rating for some school not found

    if count == 0:
        return None  # No valid ratings found

    average_score = total_score / count
    # Convert average score back to rating
    closest_rating = min(rating_values, key=lambda x: abs(rating_values[x] - average_score))

    logger.info("Closest Rating: %s", closest_rating)
    return round(rating_values[closest_rating] * 2)  # Multiply by 2 to get a score between 1-10


def fetch_schools(geoIdV4):
    http = urllib3.PoolManager()

    params = {"geoIdV4": geoIdV4}
    headers = {"apikey": ATOM_API_KEY}
    encoded_params = urllib.parse.urlencode(params)

    url = f"{SCHOOL_PROFILE_URL}?{encoded_params}"

    try:
        response = http.request('GET', url, headers=headers)
        # Decode the JSON response
        schools = json.loads(response.data.decode('utf-8'))['schools']
        logger.info("Schools Response: %s", schools)

        school_score = calculate_overall_rating(schools)

        return school_score if school_score else DEFAULT_SCHOOL_SCORE

    except urllib3.exceptions.HTTPError as e:
        logger.error("HTTP error occurred: %s", e)  # Handle specific HTTP errors
    except Exception as e:
        logger.error("An error occurred: %s", e)  # Handle other possible errors

    return DEFAULT_SCHOOL_SCORE


def lambda_handler(event, context):
    response = {
        "statusCode": 200,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': '*'
        },
        "body": ""
    }

    try:
        logger.info("Received event: %s", event)
        geoIdV4 = event.get('queryStringParameters', {}).get('geo_id', '')
        if not geoIdV4:
            response["statusCode"] = 400
            response["body"] = json.dumps({"error": "geoIdV4 parameter is required"})
        else:
            school_score = fetch_schools(geoIdV4)
            response["body"] = json.dumps({"school_score": school_score})
    except Exception as e:
        logger.error("An error occurred: %s", e)
        response["statusCode"] = 500
        response["body"] = json.dumps({"error": "An error occurred while fetching school score"})


    return response


# Test the lambda_handler function
event = {
    "queryStringParameters": {
        "geo_id": "6828b00047035292dd47fe020e636bb3"
    }
}
context = {}
print(lambda_handler(event, context))

