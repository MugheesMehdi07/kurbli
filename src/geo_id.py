import json
import urllib.parse
import urllib3  # Use urllib.parse instead of urllib
from utils import *


def lambda_handler(event, context):
    try:
        # Parse the incoming JSON from event
        data = event.get('queryStringParameters', {}).get('address', '')
        data = urllib.parse.unquote(data)

        address = get_address(data)
        headers = {"apikey": ATOM_API_KEY}

        address1 = address['street']
        address2 = f"{address['city']}, {address['state']} {address['zip']}"

        params = {
            "address": data
        }

        # URL encode address parameters directly in the f-string
        geo_id = "9fc63b98ee04811a9c931d3e99a91ac0"
        print(f"params = {params}")
        # Create a PoolManager instance
        http = urllib3.PoolManager()
        encoded_params = urllib.parse.urlencode(params)
        url = f"{BASIC_PROFILE_URL}?{encoded_params}"
        # https://api.gateway.attomdata.com/propertyapi/v1.0.0/property/basicprofile?address=4529+Winona+Ct%2C+Denver%2C+CO+80212

        print(url)

        # Perform HTTP GET request with params in the URL
        response = http.request(
            'GET',
            url,
            headers=headers
        )
        # Decode the JSON response
        response_data = json.loads(response.data.decode('utf-8'))
        print(response_data)

        geo_id = response_data['property'][0]['location']['geoIdV4']['CO']
        longitude = response_data['property'][0]['location']['longitude']
        latitude = response_data['property'][0]['location']['latitude']

    except Exception as e:
        print(f"Failed to fetch property info: {e}")

    return json.dumps({"geo_id": geo_id, "longitude": longitude, "latitude": latitude})

# Test the lambda_handler function
event = {
    "queryStringParameters": {
        "address": "4529 Winona Ct, Denver, CO 80212"
    }
}

#geo id : 1291dc1937525d78f89cebb6a43a50de

context = {}
print(lambda_handler(event, context))
