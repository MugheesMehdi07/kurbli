import requests

from scores.c import calculate_overall_rating


def format_data(address):
    return  {
        "street": address['street'],
        "city": address['city'],
        "state": address['state'],
        "zip": address['zip']
    }

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


def fetch_event_details(api_key, property_id):
    url = f"https://api.gateway.attomdata.com/propertyapi/v1.0.0/allevents/detail?id={property_id}"
    headers = {"apikey": api_key}
    response = requests.get(url, headers=headers)
    return response.json()

def fetch_property_details_and_avm(api_key, address1, address2):
    url = "https://api.gateway.attomdata.com/propertyapi/v1.0.0/attomavm/detail"
    params = {"address1": address1, "address2": address2}
    headers = {"apikey": api_key}  # Replace with your actual API key
    response = requests.get(url, headers=headers, params=params)
    print("Property Details and AVM Response:", response.json())
    return response.json()

def fetch_schools(api_key,geoIdV4):
    url = "https://api.gateway.attomdata.com/v4/school/search"
    params = {"geoIdV4": geoIdV4, "radius": 5, "page": 1, "pageSize": 200}
    headers = {"apikey": api_key}
    response = requests.get(url, headers=headers, params=params)

    print("Schools Response:", response.json())

    school_score = calculate_overall_rating(response.json())
    print("Schools Score:", school_score)

    return school_score

def fetch_community_profile(api_key,geoIdv4):
    url = "https://api.gateway.attomdata.com/v4/neighborhood/community"
    params = {"geoIdv4": geoIdv4}
    headers = {"apikey": api_key}
    response = requests.get(url, headers=headers, params=params).json()
    print("Community Profile Response:", response.json())
    # Navigate through the nested JSON to reach the crime section
    crime_data = response.get('community', {}).get('crime', {})

    # Extract the "crime_Index" which can be considered as the "Neighborhood Crime Rating"
    neighborhood_crime_rating = crime_data.get('crime_Index', 'No data available')

    print("Neighborhood Crime Rating:", neighborhood_crime_rating)
    return neighborhood_crime_rating

def fetch_data(address):

    data = format_data(address)

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

    # Placeholder values for Steps 2 and 3 as the required data isn't available in the provided response
    number_of_nxo_sfrs = 10  # Placeholder
    number_of_rsfr = 5  # Placeholder


    attom_api_key = "7ad05283fcb3cddf035d448890befee9"

    attom_basic_info = fetch_attom_basic_property_info(
        api_key=attom_api_key,
        data=data
    )

    print("ATTOM Basic Property Information:", attom_basic_info)

    attom_id = attom_basic_info['property'][0]['identifier']['attomId']
    market_value = attom_basic_info['property'][0]['sale']['saleAmountData']['saleAmt']
    property_geo_id = attom_basic_info['property'][0]['location']['geoIdV4']['N1']


    # event_details = fetch_event_details(attom_api_key,attom_id)
    # property_details_and_avm = fetch_property_details_and_avm(attom_api_key,"4529 WINONA CT", "DENVER, CO")
    school_score = fetch_schools(attom_api_key, property_geo_id)
    neighborhood_crime_rating = fetch_community_profile(attom_api_key, property_geo_id)



    # # Aggregating data into the property model
    property_model = {
        "Market Value of Property": market_value,
        "Monthly Rental Estimate": monthly_rental_estimate,
        "Gross Annual Rent": gross_annual_rent,
        "Annual Expenses": annual_expenses,
        "Net Income of the Property": net_income,
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



