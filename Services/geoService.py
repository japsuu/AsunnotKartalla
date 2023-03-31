import requests
import config
import json
from geopy import Nominatim


def get_geocode_provider():
    return 'nominatim'


def address_to_coordinates(address_to_geocode):
    if config.geoService_USE_NOMINATIM_OVER_MML:
        # Create a geocoder object.
        geocoder = Nominatim(user_agent=config.common_user_agent)
        raw_geocode = geocoder.geocode(address_to_geocode)
        if raw_geocode is None:
            return None
        else:
            return [raw_geocode.latitude, raw_geocode.longitude]
    else:
        # NOTE: Potential PROD code. Uses the Finnish Maanmittauslaitos API
        # Construct the API query
        query = config.geoService_API_MML_URL_PREFIX + address_to_geocode + config.geoService_API_MML_URL_SUFFIX
        # Fetch the json response
        response = requests.get(query, auth=(config.geoservice_MML_API_KEY, config.geoservice_MML_API_PASSWORD), headers=config.common_request_headers)
        # TODO: Exception checking.
        # MML might not be able to parse all addresses, as it requires the address to be supplied in specific format.
        # This, however, is not a rabbithole I want to go down, as I'd need to parse user generated addresses to a specific format...
        data = json.loads(response.text)
        return data['features'][0]['geometry']['coordinates']
