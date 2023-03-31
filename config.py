
# Requests
common_user_agent = 'Vuokraovi API (Development) - contact: YOUR_EMAIL - GitHub: https://github.com/japsuu/AsunnotKartalla'
common_request_headers = {'user-agent': common_user_agent}

# API Access
geoservice_MML_API_KEY = 'API_KEY_HERE'
geoservice_MML_API_PASSWORD = 'API_PASS_HERE'

# Vuokraovi specific
vuokraovi_ROOT_URL = 'https://www.vuokraovi.com'
vuokraovi_LISTING_URL = vuokraovi_ROOT_URL + '/vuokra-asunto/'
vuokraovi_APARTMENT_ID_REGEX = r'/(\d+)\?'

# IO Service
ioService_LISTINGS_FILENAME = 'listings.json'
ioService_MAP_FILENAME = 'map.html'
ioService_LISTINGS_METADATA_FILENAME = 'runtime_data.ak'

# Data Service
dataService_MAX_DATA_AGE = 86400     # 86400s = 24h.

# Geo Service
# False = Maanmittauslaitos API, True = Nominatim API.
geoService_USE_NOMINATIM_OVER_MML = True    # Maanmittauslaitos requires an API key, while Nominatim mostly works without one. Nominatim isn't suitable for bulk geocoding, though :).
geoService_API_MML_URL_PREFIX = 'https://avoin-paikkatieto.maanmittauslaitos.fi/geocoding/v2/pelias/search?text='
geoService_API_MML_URL_SUFFIX = '&sources=interpolated-road-addresses&size=1&lang=fi'   # With EPSG coordinate system: geoService_API_MML_URL_SUFFIX = '&sources=addresses&crs=EPSG:3067&lang=fi'


# Scrape Service
scrapeService_NON_BREAK_SPACE_CHAR = u'\xa0'
