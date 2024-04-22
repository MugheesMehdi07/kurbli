import json

from flask import Flask, request, jsonify
from flask_cors import CORS
from data.models import Property
import requests
from constants import ATOM_API_KEY, BASIC_PROFILE_URL
from investibility_calculation import calculate_investibility_score
from scores.cap_score import calculate_cap_score
from scores.crime_score import fetch_community_profile
from scores.schools_score import fetch_schools
from scores.sfr_score import nsfr_score, rsfr_score

app = Flask(__name__)
CORS(app)

def fetch_attom_basic_property_info(api_key, data):
    headers = {"apikey": api_key}
    address1 = data['street']
    address2 = f"{data['city']}, {data['state']} {data['zip']}"
    params = {"address1": address1, "address2": address2}
    response = requests.get(BASIC_PROFILE_URL, headers=headers, params=params)
    return response.json() if response.status_code == 200 else None

@app.route('/api/get_geo_id', methods=['GET'])
def get_geo_id():
    data = json.loads(request.args.get('address'))
    attom_info = fetch_attom_basic_property_info(ATOM_API_KEY, data)
    geo_id = attom_info['property'][0]['location']['geoIdV4']['N1'] if attom_info else None
    return jsonify({"geo_id": geo_id})

@app.route('/api/cap_rate', methods=['GET'])
def cap_rate():
    data = json.loads(request.args.get('address'))
    cap_rate = calculate_cap_score(data)
    return jsonify({"cap_rate": cap_rate})

@app.route('/api/crime_score', methods=['GET'])
def crime_score():
    geo_id = request.args.get('geo_id')
    crime_rate = fetch_community_profile(geo_id)
    return jsonify({"crime_rate": crime_rate})

@app.route('/api/school_score', methods=['GET'])
def school_score():
    geo_id = request.args.get('geo_id')
    school_rate = fetch_schools(geo_id)
    return jsonify({"school_rate": school_rate})

@app.route('/api/nsfr_scores', methods=['GET'])
def nsfr_scores():
    latitude = request.args.get('latitude')
    longitude = request.args.get('longitude')
    nsfr = nsfr_score(latitude, longitude)
    return jsonify({"nsfr": nsfr})

@app.route('/api/rsfr_scores', methods=['GET'])
def rsfr_scores():
    latitude = request.args.get('latitude')
    longitude = request.args.get('longitude')
    rsfr = rsfr_score(latitude, longitude)
    return jsonify({"rsfr": rsfr})


@app.route('/api/investibility_score', methods=['POST'])
def investibility_score():
    property_data = request.get_json()
    property_obj = Property(**property_data)
    score = calculate_investibility_score(property_obj)
    return jsonify({"investibility_score": score})
@app.route('/api/investibility_score', methods=['POST'])
def compute_investibility_score():
    property_data = request.get_json()
    property_obj = Property(**property_data)
    score = calculate_investibility_score(property_obj)
    return jsonify({"investibility_score": score})

if __name__ == '__main__':
    app.run(debug=True)
