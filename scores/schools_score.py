import requests

from constants import ATOM_API_KEY


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
        rating = school['detail']['schoolRating'].strip()
        if rating in rating_values:
            total_score += rating_values[rating]
            count += 1

    if count == 0:
        return None  # No valid ratings found

    average_score = total_score / count
    # Convert average score back to rating
    closest_rating = min(rating_values, key=lambda x: abs(rating_values[x] - average_score))

    return closest_rating


def fetch_schools(geoIdV4):
    url = "https://api.gateway.attomdata.com/v4/school/search"
    params = {"geoIdV4": geoIdV4, "radius": 5, "page": 1, "pageSize": 200}
    headers = {"apikey": ATOM_API_KEY}
    response = requests.get(url, headers=headers, params=params)

    print("Schools Response:", response.json())

    school_score = calculate_overall_rating(response.json())
    print("Schools Score:", school_score)

    return school_score