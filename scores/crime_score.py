import requests

from constants import ATOM_API_KEY, CRIME_PROFILE_URL


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


def fetch_community_profile(geoIdv4):

    params = {"geoIdv4": geoIdv4}
    headers = {"apikey": ATOM_API_KEY}
    response = requests.get(CRIME_PROFILE_URL, headers=headers, params=params).json()


    # Navigate through the nested JSON to reach the crime section
    crime_data = response.get('community', {}).get('crime', {})

    # Extract the "crime_Index" which can be considered as the "Neighborhood Crime Rating"
    neighborhood_crime_rating = crime_data.get('crime_Index', 'No data available')

    print("Neighborhood Crime Rating:", neighborhood_crime_rating)

    return normalize_crime_rate(neighborhood_crime_rating)