import json

from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

from data.models import Property
from constants import ATOM_API_KEY, BASIC_PROFILE_URL
from investibility_calculation import calculate_investibility_score
from src.cap_score import calculate_cap_score
from src.crime_score import fetch_community_profile
from src.schools_score import fetch_schools
from src.sfr_score import nsfr_score, rsfr_score

app = Flask(__name__)
CORS(app)



@app.route('/api/get_geo_id', methods=['GET'])
def get_geo_id():
    data = json.loads(request.args.get('address'))
    attom_info = fetch_attom_basic_property_info(ATOM_API_KEY, data)
    return jsonify({"geo_id": geo_id})

@app.route('/api/cap_rate', methods=['GET'])
def cap_rate():
    try:
        data = json.loads(request.args.get('address'))
        cap_rate = calculate_cap_score(data)
        return jsonify({"cap_rate": cap_rate})
    except Exception as e:
        print(f"Failed to calculate cap rate: {e}")
        return jsonify({"cap_rate": "DefaultCapRate"})

@app.route('/api/crime_score', methods=['GET'])
def crime_score():
    try:
        geo_id = request.args.get('geo_id')
        crime_rate = fetch_community_profile(geo_id)
        return jsonify({"crime_rate": crime_rate})
    except Exception as e:
        print(f"Failed to fetch crime score: {e}")
        return jsonify({"crime_rate": "DefaultCrimeRate"})

@app.route('/api/school_score', methods=['GET'])
def school_score():
    try:
        geo_id = request.args.get('geo_id')
        school_rate = fetch_schools(geo_id)
        return jsonify({"school_rate": school_rate})
    except Exception as e:
        print(f"Failed to fetch school score: {e}")
        return jsonify({"school_rate": "DefaultSchoolRate"})

@app.route('/api/nsfr_scores', methods=['GET'])
def nsfr_scores():
    try:
        latitude = request.args.get('latitude')
        longitude = request.args.get('longitude')
        nsfr = nsfr_score(latitude, longitude)
        return jsonify({"nsfr": nsfr})
    except Exception as e:
        print(f"Failed to fetch nsfr scores: {e}")
        return jsonify({"nsfr": "DefaultNSFR"})

@app.route('/api/rsfr_scores', methods=['GET'])
def rsfr_scores():
    try:
        latitude = request.args.get('latitude')
        longitude = request.args.get('longitude')
        rsfr = rsfr_score(latitude, longitude)
        return jsonify({"rsfr": rsfr})
    except Exception as e:
        print(f"Failed to fetch rsfr scores: {e}")
        return jsonify({"rsfr": "DefaultRSFR"})

@app.route('/api/investibility_score', methods=['POST'])
def compute_investibility_score():
    try:
        property_data = request.get_json()
        property_obj = Property(**property_data)
        score = calculate_investibility_score(property_obj)
        return jsonify({"investibility_score": score})
    except Exception as e:
        print(f"Failed to compute investibility score: {e}")
        return jsonify({"investibility_score": "ErrorCalculatingScore"})

if __name__ == '__main__':
    app.run(debug=True)
