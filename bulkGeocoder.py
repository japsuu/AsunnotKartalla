from geopy import Photon

import config
from Services import dataService, ioService


def get_geocode_provider():
    return 'photon'


def address_to_coordinates(address_to_geocode):
    # Create a geocoder object.
    geocoder = Photon(user_agent=config.common_user_agent)
    raw_geocode = geocoder.geocode(address_to_geocode)
    if raw_geocode is None:
        return None
    else:
        return [raw_geocode.latitude, raw_geocode.longitude]


# Bulk geocode the available data, until the end of time.
data = dataService.get_data_cache()

entries_to_geocode = 0
for listing in data:
    if listing['geocode'] is None:
        entries_to_geocode += 1

print(f'starting to geocode all data ({entries_to_geocode} entries)...')
geocoded_entries = 0
for listing in data:
    if listing['geocode'] is None:
        coordinates = address_to_coordinates(listing['address'])
        listing['geocode'] = coordinates
        listing['geocodeprovider'] = get_geocode_provider()
        geocoded_entries += 1
        if geocoded_entries % 20 == 0:
            ioService.overwrite_listings_file(data)
            print(f'geocoded {geocoded_entries}/{entries_to_geocode} entries...')

print(f'geocoding done!')
