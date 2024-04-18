import requests

from constants import ATOM_API_KEY, BASIC_PROFILE_URL
from scores.cap_score import calculate_cap_score
from scores.crime_score import fetch_community_profile
from scores.schools_score import calculate_overall_rating, fetch_schools
from scores.sfr_score import nsfr_score, rsfr_score


def format_data(address):
    return  {
        "street": address['street'],
        "city": address['city'],
        "state": address['state'],
        "zip": address['zip']
    }




def fetch_attom_basic_property_info(api_key, data):
    headers = {
        "apikey": api_key
    }

    # Construct address1 and address2 from the address dictionary
    address1 = data['street']
    address2 = f"{data['city']}, {data['state']} {data['zip']}"

    params = {
        "address1": address1,
        "address2": address2
    }

    response = requests.get(BASIC_PROFILE_URL, headers=headers, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error fetching ATTOM data: {response.status_code}")
        return None





# def fetch_data(address):
#     print(address)
#     address['street'] = address['address'].split(",")[0]
#     data = format_data(address)
#
#     latitude = address['latitude']
#     longitude = address['longitude']
#
#     attom_basic_info = fetch_attom_basic_property_info(
#         api_key=ATOM_API_KEY,
#         data=data
#     )
#
#     print("ATTOM Basic Property Information:", attom_basic_info)
#
#
#     property_geo_id = attom_basic_info['property'][0]['location']['geoIdV4']['N1']
#
#
#
#     cap_rate = calculate_cap_score(data)
#
#     number_of_nxo_sfrs = nsfr_score(latitude,longitude)
#     number_of_rsfr = rsfr_score(latitude,longitude)
#     school_score = fetch_schools(property_geo_id)
#     neighborhood_crime_rating = fetch_community_profile(property_geo_id)
#     flood_factor_score = 5 # place holder
#
#
#
#     # # Aggregating data into the property model
#     property_model = {
#
#         "Cap Rate": cap_rate,
#         "Number of NxO SFRs in 2 mile radius": number_of_nxo_sfrs,
#         "Number of rSFR in 2 mile radius": number_of_rsfr,
#         "Flood Factor Score": flood_factor_score,
#         "Neighborhood Crime Rating": neighborhood_crime_rating,
#         "Neighborhood School Rating": school_score
#     }
#
#
#
#     print(property_model)
#
#     return property_model


def fetch_data(address):

    print(address)
    address['street'] = address['address'].split(",")[0]
    data = format_data(address)

    latitude = address['latitude']
    longitude = address['longitude']

    attom_basic_info = fetch_attom_basic_property_info(
        api_key=ATOM_API_KEY,
        data=data
    )

    print("ATTOM Basic Property Information:", attom_basic_info)


    property_geo_id = attom_basic_info['property'][0]['location']['geoIdV4']['N1']
    # Placeholder values
    default_cap_rate = 1  # default placeholder for NxO SFRs
    default_nsfr = 1  # default placeholder for NxO SFRs
    default_rsfr = 1  # default placeholder for rSFR
    default_school_score = 1  # default placeholder for school score
    default_crime_rate = 1  # default placeholder for crime rating

    try:
        cap_rate_score = calculate_cap_score(data)
    except Exception as e:
        print(f"Error fetching NxO SFRs: {e}")
        cap_rate_score = default_cap_rate

    try:
        number_of_nxo_sfrs = nsfr_score(latitude, longitude)
    except Exception as e:
        print(f"Error fetching NxO SFRs: {e}")
        number_of_nxo_sfrs = default_nsfr

    try:
        number_of_rsfr = rsfr_score(latitude, longitude)
    except Exception as e:
        print(f"Error fetching rSFR: {e}")
        number_of_rsfr = default_rsfr

    try:
        school_score = fetch_schools(property_geo_id)
    except Exception as e:
        print(f"Error fetching school scores: {e}")
        school_score = default_school_score

    try:
        neighborhood_crime_rating = fetch_community_profile(property_geo_id)
    except Exception as e:
        print(f"Error fetching crime rating: {e}")
        neighborhood_crime_rating = default_crime_rate

    # Returning fetched data along with placeholder values if exceptions were caught
    return {
        "cap_rate" : cap_rate_score,
        "number_of_nxo_sfrs": number_of_nxo_sfrs,
        "number_of_rsfr": number_of_rsfr,
        "school_score": school_score,
        "neighborhood_crime_rating": neighborhood_crime_rating,
        "flood_factor_score" : 5 # place holder
    }

# address = {
#     "address": "4529 Winona Ct, Denver, CO 80212",
#     "city": "Denver",
#     "state": "CO",
#     "zip": "80212",
#     "latitude": 39.77893,
#     "longitude": -105.047698
# }
#
# fetch_data(address)



