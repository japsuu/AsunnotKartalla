# AsunnotKartalla

![Title img](/Screenshots/map_page_vaasa_info.png)

## Info

**This is an experiment, and nothing here is production ready (or well though out) in any way.**

*This project is messy, and created to let me teach myself about Python & webscraping. Don't judge me based on it ;)*

## Features

- A webscraper to scrape rental apartments from Vuokraovi.
- API for the scraped data.
  - Endpoint for latest scraped data
  - Endpoint for single query (Vuokraovi listings page number, max entries per page)
  - Endpoint for stripped data.
- Naive geocoder implementation to geocode scraped addresses.
- Python Folium Leaflet.js map to display the apartments.
- Implements data caching.
- (Semi)modular design, allowing custom scraper implementations (other than Vuokraovi).
- Controls to manually trigger:
  - Data scraping,
  - Geocode all cached data,
  - Render cached data to the map,
  - Running Data postprocessors.

## Gallery

<img src="/Screenshots/map_page_vaasa_info_selection.png" width="512">

<img src="/Screenshots/api_latest.png" width="512">

<img src="/Screenshots/api_singlepage_max3.png" width="512">

<img src="/Screenshots/geocoding_console.png" width="512">

<img src="/Screenshots/map_page.png" width="512">

---

## Contributing

Feel free to submit any PRs :)