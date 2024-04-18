import json

from flask import Flask, request, jsonify
from flask_cors import CORS

from data.models import Property
from investibility_calculation import calculate_investibility_score
from utils.api_helpers import fetch_data

app = Flask(__name__)
CORS(app)


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

