import requests
import time
import config
from Scrapers import vuokraoviScraper


def do_scrape():
    data = []
    pages_count = 5
    max_entries_per_page = 5000
    fetch_interval_s = 60
    for page in range(1, pages_count + 1):
        print(f'scraping page {page} with {max_entries_per_page} max entries...')
        new_entries = vuokraoviScraper.scrape_website(page, max_entries_per_page)
        data.extend(new_entries)
        print(f'scraped {len(new_entries)} new entries (total {len(data)}). Sleeping for {fetch_interval_s}s...')
        if len(new_entries is not max_entries_per_page):
            time.sleep(fetch_interval_s)
    return data


def query_api_text(api_url, cookies) -> str:
    return requests.get(api_url, headers=config.common_request_headers, cookies=cookies).text


def query_api_text_minified(api_url, cookies) -> str:
    response = query_api_text(api_url, cookies)
    return minify_string(response)


def minify_string(to_minimize) -> str:
    return to_minimize.replace(config.scrapeService_NON_BREAK_SPACE_CHAR, '').replace('\n', ' ').replace('\r', '').replace('  ', '').replace(' ,', ',')
