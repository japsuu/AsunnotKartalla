import json
import time

import config
from Scrapers import vuokraoviScraper
from Services import ioService, geoService, scrapeService


# WARN: The following method blocks the "UI Thread" and should NEVER be used in prod.
# Fetching data should be done on an async thread, and should NEVER block UI.
# However, this is just a test project anyway ;)
def get_data():
    # Return cached data if it's recent enough
    if is_data_old():
        # Execute full scrape.
        return scrape_and_cache_data()
    else:
        return get_data_cache()


def get_data_cache():
    return ioService.read_listings_file()


def scrape_and_cache_data():
    listings = scrapeService.do_scrape()
    geocode_all_data(listings)
    ioService.overwrite_listings_file(listings)
    ioService.overwrite_listings_metadata_file(__get_current_time_seconds())
    return listings


def get_specific_page(page, max_entries_per_page):
    return vuokraoviScraper.scrape_website(page, max_entries_per_page)


def geocode_all_data(data):
    entries_to_geocode = 0
    for listing in data:
        if listing['geocode'] is None:
            entries_to_geocode += 1

    print(f'starting to geocode all data ({entries_to_geocode} entries)...')
    geocoded_entries = 0
    for listing in data:
        if listing['geocode'] is None:
            coordinates = geoService.address_to_coordinates(listing['address'])
            listing['geocode'] = coordinates
            listing['geocodeprovider'] = geoService.get_geocode_provider()
            geocoded_entries += 1
            if geocoded_entries % 20 == 0:
                ioService.overwrite_listings_file(data)
                print(f'geocoded {geocoded_entries}/{entries_to_geocode} entries...')

    print(f'geocoding done!')


def is_data_old() -> bool:
    return __get_data_age_seconds() > config.dataService_MAX_DATA_AGE


def format_data(data) -> str:
    return f'<pre>{json.dumps(data, ensure_ascii=False, indent=4)}</pre>'


def __get_data_age_seconds() -> int:
    return __get_current_time_seconds() - int(ioService.read_listings_metadata_file())


def __get_current_time_seconds() -> int:
    return int(time.time())
