# utils
BATCH_BASE_URL = 'https://api.batchdata.com'
ATOM_BASE_URL = 'https://api.gateway.attomdata.com'


#API KEYS
ATOM_API_KEY = '7ad05283fcb3cddf035d448890befee9'
BATCH_API_KEY = 'MDBUSyko3Q2cpXho7NboEIEzAaAKncCw9AIbTfbZ'

#URLS
CRIME_PROFILE_URL = f'{ATOM_BASE_URL}/v4/neighborhood/community'
SFR_PROFILE_URL = f'{ATOM_BASE_URL}/propertyapi/v1.0.0/property/snapshot'
SCHOOL_PROFILE_URL = f'{ATOM_BASE_URL}/v4/school/search'
BASIC_PROFILE_URL = f'{ATOM_BASE_URL}/propertyapi/v1.0.0/property/basicprofile'

BATCH_URL = f'{BATCH_BASE_URL}/api/v1/property/lookup/all-attributes'
BATCH_SEARCH_URL = f'{BATCH_BASE_URL}/api/v1/property/search'

#Default Scores
DEFAULT_CAP_RATE = 0.05
DEFAULT_CRIME_SCORE = 5
DEFAULT_SCHOOL_SCORE = 5




def get_address(address_str):


    # Split the address string by commas
    parts = address_str.split(', ')

    # Extract the street from the first part
    street = parts[0]

    # Extract the city from the second part
    city = parts[1]

    # Split the third part by space to separate the state and zip
    state_zip = parts[2].split(' ')

    # Extract the state
    state = state_zip[0]

    # Extract the zip code
    zip_code = state_zip[1]

    # Create a dictionary to hold the extracted values
    address_dict = {
        "street": street,
        "city": city,
        "state": state,
        "zip": zip_code
    }

    return address_dict
