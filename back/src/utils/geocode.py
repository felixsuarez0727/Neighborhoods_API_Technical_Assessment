from dotenv import load_dotenv

import googlemaps
import requests
import json
import os
 
from utils.constants import API_URL, SP_REFERENCE, ST_START_NUMBER, ST_NAME, ST_STEP, LOCALITY
from utils import logger

load_dotenv()
API_KEY = os.environ.get("API_KEY")


try:
    logger.info_log( 'Loading Google Maps Client' )
    G_MAPS = googlemaps.Client( key=API_KEY )

except Exception as e:
    logger.error_log( f'Error Loading Google Maps Client: {e}' )
    exit()


def get_geocode(full_address):
    """ Returns the Geocoded Address using the Google Maps Client """
    
    try:
        return G_MAPS.geocode(full_address)
    except Exception as e:
        logger.error_log( f'Error Extracting the Address: {e}' )
        exit()


def get_coordinates(geocode):
    """ Obtain the coordinates from the provided Geocode """
    return geocode[0].get("geometry").get("location")


def calculate_distance(new_number:int):
    """ Calculate the distance between starting point and the ending point in steps """
    return int((new_number - ST_START_NUMBER) / ST_STEP)


def get_neighborhood(lat, lng) -> str:
    """ Obtain the neighborhood from the Portland Maps API """

    try:
        request = requests.get(f'{API_URL}/query?geometryType=esriGeometryPoint&returnGeometry=false&f=pjson&geometry={lng}%2C{lat}%0D%0A&inSR={SP_REFERENCE}')
        data = json.loads(request.text)
        neighborhood = data.get("features")[0].get("attributes").get("NAME").title()

    except Exception as e:
        logger.error_log( f'Error Getting the neighborhood: {e}' )
        exit()

    return neighborhood


def skip_street(st_number:int, neighborhood:str = None, result:list = []) -> dict:
    """ Recursive method, skip the street until find a new neighborhood """
    logger.info_log( f'Skipping street, actual number: {st_number}' )
    
    full_address = f"{st_number} {ST_NAME}, {LOCALITY}"
    geocode = get_geocode(full_address)

    coordinates = get_coordinates(geocode)
    lat = coordinates.get('lat')
    lng = coordinates.get('lng')

    new_neighborhood = get_neighborhood(lat, lng)

    if new_neighborhood == neighborhood or neighborhood == None : 
        result.append({"address":full_address, "neighborhood": new_neighborhood, "lat": lat, "lng": lng})
        return skip_street(st_number + ST_STEP, new_neighborhood)
    
    result.append({"address":full_address, "neighborhood": new_neighborhood, "lat": lat, "lng": lng})
    logger.info_log( f'Found new neighborhood, Old: {neighborhood}, New: {new_neighborhood}' )
    return result 
