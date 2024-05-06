import json
import logging

import boto3
from botocore.exceptions import ClientError

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

# Initialize DynamoDB client
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('PropertyScores')

def calculate_investibility_score(property_data):
    score = 0
    cap_rate = int(property_data.get('cap_rate', 0))
    number_of_nxo_sfrs = int(property_data.get('number_of_nxo_sfrs', 0))
    number_of_rsfr = int(property_data.get('number_of_rsfr', 0))
    flood_factor_score = int(property_data.get('flood_factor_score', 10))  # assuming higher value if not specified
    neighborhood_crime_rating = int(property_data.get('neighborhood_crime_rating', 10))
    school_score = int(property_data.get('school_score', 0))

    # Step 1: Cap Rate Scoring
    if cap_rate >= 10:
        score += 30
    elif 8 <= cap_rate < 10:
        score += 8
    elif 5 <= cap_rate < 8:
        score += 5

    # Step 2: Number of NxO SFRs Scoring
    if number_of_nxo_sfrs > 20:
        score += 20
    elif 10 <= number_of_nxo_sfrs <= 20:
        score += 8
    elif 5 <= number_of_nxo_sfrs < 10:
        score += 5
    elif 1 < number_of_nxo_sfrs < 5:
        score += 2
    else:
        score += 1

    # Step 3: Number of rSFRs Scoring
    if number_of_rsfr > 20:
        score += 20
    elif 10 <= number_of_rsfr <= 20:
        score += 8
    elif 5 <= number_of_rsfr < 10:
        score += 5
    elif 1 < number_of_rsfr < 5:
        score += 2
    else:
        score += 1

    # Step 4: Flood Factor Scoring
    if 1 <= flood_factor_score <= 2:
        score += 10
    elif 3 <= flood_factor_score <= 6:
        score += 7
    elif 7 <= flood_factor_score <= 8:
        score += 3
    else:
        score += 1

    # Step 5: Crime Factor Scoring
    if 1 <= neighborhood_crime_rating <= 2:
        score += 10
    elif 3 <= neighborhood_crime_rating <= 6:
        score += 7
    elif 7 <= neighborhood_crime_rating <= 8:
        score += 3
    else:
        score += 1

    # Step 6: School Rating Scoring
    if school_score > 7:
        score += 10
    elif school_score > 5:
        score += 7
    elif school_score > 3:
        score += 3
    else:
        score += 1

    # Step 8: Determining the Ranking
    if score >= 99:
        ranking = "Diamond"
    elif 90 <= score <= 98:
        ranking = "Platinum"
    elif 85 <= score <= 89:
        ranking = "Gold"
    elif 75 <= score <= 84:
        ranking = "Silver"
    else:
        ranking = "Bronze"

    return {"score": score, "ranking": ranking}


def lambda_handler(event, context):
    response = {
        "statusCode": 200,
        "headers": cors_headers,
        "body": ""
    }
    try:
        logger.info("Received event: %s", event)
        property_data = event.get('queryStringParameters', {})
        email = property_data.get('email', None)
        address = property_data.get('address', None)

        if not property_data or not email or not address:
            response["statusCode"] = 400
            response["body"] = json.dumps({"error": "Property data, email, and address are required"})
        else:
            result= property_data
            result.update(calculate_investibility_score(property_data))

            # Save to DynamoDB
            try:
                table.put_item(Item=result)
                logger.info("Saved result to DynamoDB: %s", result)
            except ClientError as e:
                logger.error("Error saving to DynamoDB: %s", e)
                response["statusCode"] = 500
                response["body"] = json.dumps({"error": "Error saving to DB"})
                return response

            response["body"] = json.dumps(result)

    except Exception as e:
        logger.error("An error occurred: %s", e)
        response["statusCode"] = 500
        response["body"] = json.dumps({"error": "An error occurred while processing the request"})

    return response

# # Test the lambda_handler function
# event = {
#     "queryStringParameters": {
#         "property": {
#             "cap_rate": 9,
#             "number_of_nxo_sfrs": 15,
#             "number_of_rsfr": 4,
#             "flood_factor_score": 2,
#             "neighborhood_crime_rating": 1,
#             "school_score": 10,
#             "email": "john@gmail.com",
#             "address": "123 Main St, Denver, CO 80212"
#         },
#         }
#     }
#
# context = {}
# print(lambda_handler(event, context))
