import requests
from bs4 import BeautifulSoup
import json
import time
import re
import folium
from flask import Flask
from geopy import Nominatim

# Settings.
user_agent = 'Vuokraovi API (Development) - contact: japsu.honkasalo@gmail.com'
rootUrl = 'https://www.vuokraovi.com'
listingUrl = rootUrl + '/vuokra-asunto/'
nonBreakSpace = u'\xa0'
resultsFilename = 'results.json'
apartmentIdRegex = r'/(\d+)\?'
request_headers = {'user-agent': user_agent}


def clear_data_file():
    file_to_delete = open(resultsFilename, 'w')
    file_to_delete.close()


def write_to_file(data):
    with open(resultsFilename, 'w', encoding='utf-8') as results_file:
        json.dump(data, results_file, ensure_ascii=False, indent=4)


# Create the Flask app.
app = Flask(__name__)


def clean_page_element(element):
    if element is None:
        return 'null'
    else:
        return element.text.strip()


def scrape_website(page, max_entries):
    # Fetch the html response.
    cookies = {'LIST_PER_PAGE': str(max_entries)}
    response = requests.get(f'{rootUrl}/vuokra-asunnot?page={str(page)}&pageType=list', headers=request_headers, cookies=cookies)

    # Remove non-breaking spaces because we don't need those.
    scrape = response.text.replace(nonBreakSpace, '').replace('\n', ' ').replace('\r', '').replace('  ', '')

    # Create a soup parser.
    soup = BeautifulSoup(scrape, 'html.parser')

    # Create a geocoder object.
    geocoder = Nominatim(user_agent=user_agent)

    # Find all elements with the "list-item-link" class (all listings).
    link_elements = soup.find_all(class_='list-item-link')

    # Extract required information.
    data = []
    for link_element in link_elements:
        url_element = link_element.get('href').strip()
        price_element = link_element.find(class_='price')
        address_element = link_element.find(class_='address')
        description_elements = link_element.find_all(class_='semi-bold')

        # Failsafe.
        if len(description_elements) < 2:
            continue
        else:
            title_element = description_elements[0]
            rooms_element = description_elements[1]

        # Process elements.
        title_value = clean_page_element(title_element)
        rooms_value = clean_page_element(rooms_element)
        price_value = clean_page_element(price_element)

        # Return if address missing.
        if address_element is None:
            continue
        else:
            address_value = clean_page_element(address_element)

        # Handle geocoding
        geocode = [1.13, 2.14]
        # 1 raw_geocode = geocoder.geocode(address_value)
        # 1 if raw_geocode is None:
        # 1     continue
        # 1 else:
        # 1     geocode = [raw_geocode.latitude, raw_geocode.longitude]

        # Return if url missing.
        if url_element is None:
            continue
        else:
            match = re.search(apartmentIdRegex, url_element)
            if match:
                id_value = match.group(1)
                url_value = listingUrl + id_value
            else:
                # Return if url doesn't contain the ID number. Should not happen, but just in case.
                continue

        listing = dict(id=id_value, title=title_value, rooms=rooms_value, price=price_value, address=address_value, geocode=geocode, url=url_value)
        data.append(listing)
    return data


def fetch_data(page, max_entries):
    data = scrape_website(page, max_entries)
    # write_to_file(data)
    # TODO: Implement caching for the data.
    return data


def fetch_all_data(pages, max_entries_per_page, delay_per_page):
    data = []
    for page in range(1, pages + 1):
        data.extend(scrape_website(page, max_entries_per_page))
        time.sleep(delay_per_page)
        print(f'scraped {len(data)} entries.')
    # TODO: Implement caching for the data.
    return data


def format_data(data):
    return f'<pre>{json.dumps(data, ensure_ascii=False, indent=4)}</pre>'


@app.route('/', methods=['GET'])
def get_main():
    return '''
        Access the API <a href="./api?page=1&maxEntries=10">here</a>.
        </br>
        Access the map <a href="./kartta">here</a>.
        '''


@app.route('/kartta', methods=['GET'])
def get_map():
    data = fetch_data('1', '100')
    m = folium.Map(location=[63.10678616588225, 21.65669875986231], zoom_start=12)
    for listing in data:
        tooltip = listing['title']
        folium.Marker(
            listing['geocode'], popup=f'''
            <i>{listing['address']}</i>
            </br>
            <i>{listing['rooms']}</i>
            </br>
            <i>{listing['price']}</i>
            </br>
            <a href="{listing['url']}">Link</a>
            ''', tooltip=tooltip
        ).add_to(m)

    return m.get_root().render()

    # 1 m.save("index.html")
    # 1 with open('index.html', 'r') as file:
    # 1     data = file.read()
    # 1 return data


@app.route('/api', methods=['GET'])
def get_api():
    print('starting scrape')
    clear_data_file()
    data = fetch_all_data(5, 5000, 60)
    write_to_file(data)
    return 'done'

    # page = request.args.get('page')
    # max_entries = request.args.get('maxEntries')
#
    # try:
    #     # Default page to 1.
    #     if page is None:
    #         page = 1
    #     else:
    #         page = int(page)
    #     if page < 1:
    #         return f'Invalid page number ({page}), should be larger than 1.'
#
    #     # Default max_entries to 20.
    #     if max_entries is None:
    #         max_entries = 20
    #     else:
    #         max_entries = int(max_entries)
    #     if max_entries < 1 or max_entries > 1000:
    #         return f'Invalid max_entries ({max_entries}), should be in range [1, 1000].'
    # except:
    #     return 'Invalid parameters supplied.'
#
    # data = fetch_data(str(page), str(max_entries))
    # return format_data(data)


if __name__ == '__main__':
    app.run(port=8080, host='0.0.0.0', debug=False)
