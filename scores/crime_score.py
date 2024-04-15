import requests

from constants import ATOM_API_KEY


def fetch_community_profile(geoIdv4):
    url = "https://api.gateway.attomdata.com/v4/neighborhood/community"

    params = {"geoIdv4": geoIdv4}
    headers = {"apikey": ATOM_API_KEY}
    response = requests.get(url, headers=headers, params=params).json()


    print("Community Profile Response:", response.json())
    # Navigate through the nested JSON to reach the crime section
    crime_data = response.get('community', {}).get('crime', {})

    # Extract the "crime_Index" which can be considered as the "Neighborhood Crime Rating"
    neighborhood_crime_rating = crime_data.get('crime_Index', 'No data available')

    print("Neighborhood Crime Rating:", neighborhood_crime_rating)

    return neighborhood_crime_rating