from bs4 import BeautifulSoup
from selenium import webdriver
import csv


# Fetching the next page
def get_url(search_term):
    """Generate a URL from search term"""
    template = "https://www.amazon.com/s?k={}&crid=320Y6M8VL6LF8&sprefix=rtx+%2Caps%2C194&ref=nb_sb_ss_ts-doa" \
               "-p_3_4 "
    search_term = search_term.replace(" ", '+')

    # Add search term to url
    url = template.format(search_term)

    # Add page to placeholder
    url += '&page={}'

    return url


# Get all items from page
def extract_record(item):
    """Extracting data from record"""

    # Description and URL
    a_tag = item.h2.a
    description = a_tag.text.strip()
    url = 'https://www.amazon.com' + a_tag.get('href')

    try:
        # Price
        price_parent = item.find('span', 'a-price')
        price = price_parent.find('span', 'a-offscreen').text

    except AttributeError:
        return

    result = (description, price, url)

    return result


def main(search_term):
    """Run main program"""
    # Start up webdriver
    driver = webdriver.Chrome()

    records = []
    url = get_url(search_term)

    # Iterate over pages
    for page in range(1, 21):
        driver.get(url.format(page))

        # Soup Object and collection extraction
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        results = soup.find_all('div', {'data-component-type': 's-search-result'})

        # Return records in a list
        for item in results:
            record = (extract_record(item))
            if record and 'RTX 3080' and 'Graphics Card' in record[0]:
                records.append(record)

    driver.close()

    # Save data to csv file
    with open('results.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Description', 'Price', 'URL'])
        writer.writerows(records)


main('RTX 3080')
