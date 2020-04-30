import requests
from bs4 import BeautifulSoup
import csv
import datetime


NOW = datetime.datetime.now()

URLS = ['https://www.citilink.ru/search/?available=1&status=55395790&country=Все&menu_id=26&text=Ryzen%205%202600&sorting=price_asc',\
        'https://www.citilink.ru/catalog/computers_and_notebooks/hdd/ssd_in/?available=1&status=55395790&sorting=price_asc&p=1&f=5631_580',]
HEADERS = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1 Safari/605.1.15', 'accept': '*/*'}

def get_html(url, params = None):
    r = requests.get(url, headers = HEADERS, params = params)
    return r

def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('div', class_='js--subcategory-product-item subcategory-product-item product_data__gtm-js product_data__pageevents-js ddl_product', limit = 1)
    result = []
    for item in items:
        result.append({
            'title': item.find('a', class_='link_gtm-js link_pageevents-js ddl_product_link').get_text(strip=True),
            'price': item.find('ins', class_='subcategory-product-item__price-num').get_text(strip=True)
        })
    return result[0]


def parce(url):
    html = get_html(url)
    if html.status_code == 200:
        return get_content(html.text)
    else:
        print('ЧТО-ТО ПОШЛО НЕ ТАК, ТЫ ПИДОР ЛЫСЫЙ АЗАЗАЗ')

def save_csv(object, path):
    with open(path, 'w', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(['title', 'price'])
        for obj in object:
            writer.writerow([obj['title'], obj['price']])

def main(URLS):
    results = []
    for url in URLS:
        results.append(parce(url))
    save_csv(results, 'citilink' + str(NOW.date()) + '.csv')


if __name__ == "__main__":
    main(URLS)    

