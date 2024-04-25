import json
import urllib.parse
import urllib3

from utils import *


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

        print("Neighborhood Crime Rating:", neighborhood_crime_rating)

        return normalize_crime_rate(neighborhood_crime_rating)

    except urllib3.exceptions.HTTPError as e:
        print(f"HTTP error occurred: {e}")  # Handle specific HTTP errors
    except Exception as e:
        print(f"An error occurred: {e}")  # Handle other possible errors


def lambda_handler(event, context):
    geoIdV4 = event.get('queryStringParameters', {}).get('geo_id', '')
    if not geoIdV4:
        return {
            "statusCode": 400,
            "body": json.dumps({"error": "geoIdV4 parameter is required"})
        }

    normalized_crime_rate = fetch_community_profile(geoIdV4)
    return {
        "statusCode": 200,
        "body": json.dumps({"crime_score": normalized_crime_rate})
    }


# # Test the lambda_handler function
# # Test the lambda_handler function
# event =  {
#     "queryStringParameters": {
#         "geo_id": "9fc63b98ee04811a9c931d3e99a91ac0"
#     }
# }
# context = {}
# print(lambda_handler(event, context))


