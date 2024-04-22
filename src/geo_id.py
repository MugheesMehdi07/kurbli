import json
import urllib.parse
import urllib3  # Use urllib.parse instead of urllib

ATOM_BASE_URL = 'https://api.gateway.attomdata.com'
BASIC_PROFILE_URL = f'{ATOM_BASE_URL}/propertyapi/v1.0.0/property/basicprofile'
ATOM_API_KEY = '7ad05283fcb3cddf035d448890befee9'


def lambda_handler(event, context):
    # Parse the incoming JSON from event
    data = json.loads(event.get('queryStringParameters', {}).get('address', '{}'))

    headers = {"apikey": ATOM_API_KEY}
    address1 = data['address']
    address2 = f"{data['city']}, {data['state']} {data['zip']}"

    params = {
        "address1": address1,
        "address2": address2
    }

    # URL encode address parameters directly in the f-string
    geo_id = "9fc63b98ee04811a9c931d3e99a91ac0"
    print(f"params = {params}")
    # Create a PoolManager instance
    http = urllib3.PoolManager()
    encoded_params = urllib.parse.urlencode(params)
    url = f"{BASIC_PROFILE_URL}?{encoded_params}"
    try:
        # Perform HTTP GET request with params in the URL
        response = http.request(
            'GET',
            url,
            headers=headers
        )
        # Decode the JSON response
        response_data = json.loads(response.read().decode('utf-8'))
        print(response_data)

        geo_id = response_data['property'][0]['location']['geoIdV4']['CO']
    except Exception as e:
        print(f"Failed to fetch property info: {e}")

    return json.dumps({"geo_id": geo_id})


# Test the lambda_handler function
event = {
    "queryStringParameters": {
        "address": json.dumps({
            "address": "123 Main St",
            "city": "Springfield",
            "state": "IL",
            "zip": "62701"
        })
    }
}

context = {}
lambda_handler(event, context)
