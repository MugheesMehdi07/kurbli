import requests

from constants import ATOM_API_KEY


def nsfr_score(latitude,longitude):
    url = "https://api.gateway.attomdata.com/propertyapi/v1.0.0/property/snapshot"
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "radius": "2",
        "propertytype": "sfr",
        "ownerOccupied": "false",
    }
    headers = {
        "apikey": ATOM_API_KEY
    }

    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        print("Failed to fetch property snapshot:", response.status_code, response.text)
        return None



def rsfr_score(latitude,longitude):
    url = "https://api.gateway.attomdata.com/propertyapi/v1.0.0/property/snapshot"
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "radius": "2",
        "propertytype": "sfr",
        #Rental
    }
    headers = {
        "apikey": ATOM_API_KEY
    }

    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        print("Failed to fetch property snapshot:", response.status_code, response.text)
        return None