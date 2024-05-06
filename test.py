import requests

# URL and parameter
url = 'https://api.sfranalytics.com/api/v1/property/best-buyers'
params = {'search_text': '4529 Winona Ct, Denver, CO 80212'}

# Headers
headers = {'X-API-TOKEN': 'bcf6b2c944ee488f17fc7744f5b929f913ca13e0f5fc49973a3b8cd2c7c890fb'}

# Send GET request
response = requests.get(url, headers=headers, params=params)

# Check if the request was successful
if response.status_code == 200:
    # Process the response
    data = response.json()
    print("Data retrieved successfully:", data)
else:
    print("Failed to retrieve data:", response.status_code)

