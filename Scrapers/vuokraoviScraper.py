import config
from Services import scrapeService
import re
from bs4 import BeautifulSoup


def scrape_website(page, max_entries):
    cookies = {'LIST_PER_PAGE': str(max_entries)}
    scrape = scrapeService.query_api_text_minified(f'{config.vuokraovi_ROOT_URL}/vuokra-asunnot?page={str(page)}&pageType=list', cookies=cookies)

    # Create a soup parser.
    soup = BeautifulSoup(scrape, 'html.parser')

    # Find all elements with the "list-item-link" class (all listings).
    link_elements = soup.find_all(class_='list-item-link')

    # Extract required information.
    data = []
    for link_element in link_elements:
        url_element = link_element.get('href').strip()
        price_element = link_element.find(class_='price')
        # address_element = link_element.find(class_='address')
        address_element = link_element.find(class_='col-xs-5 col-sm-2 col-1')
        description_elements = link_element.find_all(class_='semi-bold')

        # Failsafe.
        if len(description_elements) < 2:
            continue
        else:
            title_element = description_elements[0]
            rooms_element = description_elements[1]

        # Process elements.
        title_value = title_element.text.strip()
        rooms_value = rooms_element.text.strip()
        price_value = price_element.text.strip()

        # Return if address missing.
        if address_element is None:
            continue
        else:
            # address_value = str(address_element['alt']).strip()
            address_value = address_element.text.strip()

        geocode = None
        geocodeprovider = None

        # Return if url missing.
        if url_element is None:
            continue
        else:
            match = re.search(config.vuokraovi_APARTMENT_ID_REGEX, url_element)
            if match:
                id_value = match.group(1)
                url_value = config.vuokraovi_LISTING_URL + id_value
            else:
                # Return if url doesn't contain the ID number. Should not happen, but just in case.
                continue

        listing = dict(id=id_value, title=title_value, rooms=rooms_value, price=price_value, address=address_value, geocode=geocode, geocode_provider=geocodeprovider,
                       url=url_value)
        data.append(listing)
    return data
