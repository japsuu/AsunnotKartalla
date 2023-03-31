import re

from flask import Flask, request

from Services import mapService, dataService, customDataProcessor

app = Flask(__name__)


# Returns the (rather disgusting) index page.
@app.route('/', methods=['GET'])
def get_index():
    # Raw HTML bby!
    return '''
        Access the map <a href="./kartta">here</a>.
        </br>
        Access the latest data API <a href="./api-latest">here</a>.
        </br>
        Access the single-page data API <a href="./api-single?page=1&maxEntries=10">here</a>.
        '''


# Returns the CACHED data. Does not guarantee the data to actually be the latest available.
@app.route('/api-latest', methods=['GET'])
def get_api_latest():
    return dataService.format_data(dataService.get_data_cache())


# Returns a single page of results with the defined parameters.
@app.route('/api-single', methods=['GET'])
def get_api_single():
    page = request.args.get('page')
    max_entries = request.args.get('maxEntries')

    try:
        # Default page to 1.
        if page is None:
            page = 1
        else:
            page = int(page)
        if page < 1:
            return f'Invalid page number ({page}), should be larger than 1.'
        # Default max_entries to 20.
        if max_entries is None:
            max_entries = 20
        else:
            max_entries = int(max_entries)
        if max_entries < 1 or max_entries > 1000:
            return f'Invalid maxEntries ({max_entries}), should be in range [1, 1000].'
    except:
        return 'Invalid parameters supplied.'

    data = dataService.get_specific_page(str(page), str(max_entries))
    return dataService.format_data(data)


# Returns the HTML map with markers.
@app.route('/kartta', methods=['GET'])
def get_map():
    return mapService.get_latest_map()


# Returns raw data in stripped "ADDRESS | URL" -format for debugging.
@app.route('/api-stripped', methods=['GET'])
def get_raw():
    data = dataService.get_data_cache()
    results = []
    # Keep only the required data.
    for entry in data:
        address = entry['address']
        url = entry['url']
        results.append(f"{address} | {url} </br>")
    return str(results)


if __name__ == '__main__':

    print("Welcome! Would you like to:")
    print("1: Fetch the latest data if needed and cache it?")
    print("2: Force fetch the latest data and cache it?")
    print("3: Geocode all cached non-geocoded data?")
    print("4: Render all the geocoded data to the map?")
    print("5: Run customDataProcessor.py?")
    print("10: Just start the server?")

    user_input = str(input())

    start_server = user_input == '10'
    if user_input != '10':
        start_server = str(input("Would you like to start the server afterwards? (y/n)")) == 'y'

    if user_input == '1':
        dataService.get_data()

    if user_input == '2':
        dataService.scrape_and_cache_data()

    if user_input == '3':
        dataService.geocode_all_data(dataService.get_data_cache())

    if user_input == '4':
        mapService.re_render_map_from_cached_data()

    if user_input == '5':
        customDataProcessor.process()

    if start_server:
        app.run(port=8080, host='0.0.0.0', debug=False)
