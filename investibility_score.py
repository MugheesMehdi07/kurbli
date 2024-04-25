import json

def calculate_investibility_score(property_data):
    score = 0
    cap_rate = property_data.get('cap_rate', 0)
    number_of_nxo_sfrs = property_data.get('number_of_nxo_sfrs', 0)
    number_of_rsfr = property_data.get('number_of_rsfr', 0)
    flood_factor_score = property_data.get('flood_factor_score', 10)  # assuming higher value if not specified
    neighborhood_crime_rating = property_data.get('neighborhood_crime_rating', 10)
    school_score = property_data.get('school_score', 0)

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
    property_data = event.get('queryStringParameters', {})

    if not property_data:
        return {
            "statusCode": 400,
            "body": json.dumps({"error": "Property data is required"})
        }

    result = calculate_investibility_score(property_data)
    return {
        "statusCode": 200,
        "body": json.dumps(result)
    }

# Test the lambda_handler function
event = {
    "queryStringParameters": {

            "cap_rate": 9,
            "number_of_nxo_sfrs": 15,
            "number_of_rsfr": 4,
            "flood_factor_score": 2,
            "neighborhood_crime_rating": 1,
            "school_score": 10
    }
}
context = {}
print(lambda_handler(event, context))
