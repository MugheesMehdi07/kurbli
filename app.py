from flask import Flask, request, jsonify
from flask_cors import CORS



app = Flask(__name__)
CORS(app)

@app.route('/calculate_score', methods=['POST'])
def calculate_score():
    data = request.get_json()
    address = data['address']
    print(address)
    # Logic to fetch and calculate the property model based on address
    property_model = {
        "property_id": "12345",
        "property_type": "SFR",
        "sale_value": 500000,
        "rent_estimate": 2000,
        "sale_date": "2021-01-01",
        "is_investor_owned": False,
        "investor_type": "Mom/Pop Investor",
        "new_investor": True,
        "investor_zip": "12345",
        "investor_city": "Investor City",
        "investor_state": "IS",
        "property_zip": address['zip'],
        "property_city": address['city'],
        "property_state": address['state'],
        "quality_of_investment": 0.8,
        "sold_recently": False
    }  # Placeholder for property model calculation logic

    return jsonify(property_model)

if __name__ == '__main__':
    app.run(debug=True)