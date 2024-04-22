import json

from flask import Flask, request, jsonify
from flask_cors import CORS

from data.models import Property
from investibility_calculation import calculate_investibility_score
import requests

from constants import ATOM_API_KEY, BASIC_PROFILE_URL
from scores.cap_score import calculate_cap_score
from scores.crime_score import fetch_community_profile
from scores.schools_score import fetch_schools
from scores.sfr_score import nsfr_score, rsfr_score
app = Flask(__name__)
CORS(app)

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








@app.route('/api/calculate_score', methods=['GET'])
def create_property():

    # Extract the address query parameter and decode it
    address_json = request.args.get('address', default='{}')

    # Check if the address is provided
    if not address_json:
        return jsonify({"error": "Address parameter is required"}), 400

    # Convert the JSON string back into a Python dictionary
    address = json.loads(address_json)

    try:
        # The fetch_data function retrieves all required fields directly using the address
        property_data = fetch_data(address)

        # Creating a new property instance



        new_property = Property(
            address=address,
            cap_rate=property_data['cap_rate'],
            number_of_nxo_sfrs=property_data['number_of_nxo_sfrs'],
            number_of_rsfr=property_data['number_of_rsfr'],
            neighborhood_crime_rating=property_data['neighborhood_crime_rating'],
            school_score=property_data['school_score'],
            flood_factor_score=property_data['flood_factor_score']
        )

        investibility_score = calculate_investibility_score(new_property)
        new_property.investibility_score = investibility_score


        # Return a dictionary version of the property for the API response
        return jsonify(new_property.to_dict()), 200
    except KeyError as e:
        # If any of the required data keys are missing
        return jsonify({"error": f"Missing property attribute: {str(e)}"}), 400
    except ValueError as e:
        # Handle value errors, such as invalid data formats
        return jsonify({"error": str(e)}), 400


if __name__ == '__main__':
    app.run(debug=True)

