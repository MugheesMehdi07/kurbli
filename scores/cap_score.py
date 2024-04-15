import requests


def fetch_batchdata_property_lookup(api_token, data):
    url = "https://api.batchdata.com/api/v1/property/lookup/all-attributes"
    headers = {
        "Accept": "application/json",
        "Authorization": f"Bearer {api_token}",
        "Content-Type": "application/json"
    }

    # Construct the address data for the API call


    response = requests.post(url, json={"requests": [{"address": data}]}, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error fetching BatchData: {response.status_code}")
        return None

def calculate_cap_score(data):
    batchdata_api_token = "MDBUSyko3Q2cpXho7NboEIEzAaAKncCw9AIbTfbZ"

    response = fetch_batchdata_property_lookup(
        api_token=batchdata_api_token,
        data=data
    )

    print("BatchData Property Lookup:", response)
    # Extract the relevant data from the response
    property_info = response['results']['properties'][0]
    market_value = property_info['valuation']['estimatedValue']
    monthly_rental_estimate = 2000  # Placeholder since the actual rental estimate is not provided in the JSON

    # Step 1: Calculate the gross annual rent
    gross_annual_rent = monthly_rental_estimate * 12

    # Step 2: Calculate the annual expenses (assuming 5% of market value as expenses)
    annual_expenses = market_value * 0.05

    # Step 3: Calculate the net income of the property
    net_income = gross_annual_rent - annual_expenses

    # Step 4: Calculate the Cap Rate
    cap_rate = net_income / market_value

    return cap_rate