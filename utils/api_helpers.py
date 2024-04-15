import requests

from constants import ATOM_API_KEY
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
    url = "https://api.gateway.attomdata.com/propertyapi/v1.0.0/property/basicprofile"
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

    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error fetching ATTOM data: {response.status_code}")
        return None





def fetch_data(address):

    data = format_data(address)

    latitude = address
    longitude = address



    attom_basic_info = fetch_attom_basic_property_info(
        api_key=ATOM_API_KEY,
        data=data
    )

    print("ATTOM Basic Property Information:", attom_basic_info)


    property_geo_id = attom_basic_info['property'][0]['location']['geoIdV4']['N1']



    cap_rate = calculate_cap_score(data)

    number_of_nxo_sfrs = nsfr_score(latitude,longitude)
    number_of_rsfr = rsfr_score(latitude,longitude)
    school_score = fetch_schools(property_geo_id)
    neighborhood_crime_rating = fetch_community_profile(property_geo_id)



    # # Aggregating data into the property model
    property_model = {

        "Cap Rate": cap_rate,
        "Number of NxO SFRs in 2 mile radius": number_of_nxo_sfrs,
        "Number of rSFR in 2 mile radius": number_of_rsfr,
        # "Flood Factor Score": flood_factor_score,
        "Neighborhood Crime Rating": neighborhood_crime_rating,
        "Neighborhood School Rating": school_score
    }


    #
    # print(property_model)

    return property_model



address = {
    "address": "4529 Winona Ct, Denver, CO 80212",
    "city": "Denver",
    "state": "CO",
    "zip": "80212",
    "latitude": 39.77893,
    "longitude": -105.047698
}

address['street'] =  address['address'].split(",")[0]
fetch_data(address)



