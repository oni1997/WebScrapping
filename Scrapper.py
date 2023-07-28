from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time
import requests
from bs4 import BeautifulSoup

def get_page_content(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.content
    else:
        raise Exception(f"Failed to retrieve the page. Status Code: {response.status_code}")

def parse_content(content):
    soup = BeautifulSoup(content, 'html.parser')
    products = []

    base_url = 'https://www.pnp.co.za'

    # Find the elements containing product details
    product_elements = soup.find_all('div', class_='productCarouselItem')

    for product_element in product_elements:
        name_element = product_element.find('div', class_='item-name')
        name = name_element.text.strip() if name_element else 'N/A'

        # Find the element containing the product price
        price_element = product_element.find('div', class_='currentPrice')
        price = price_element.text.strip() if price_element else 'N/A'

        # Find the element containing the product image URL
        img_element = product_element.find('img', class_='lazyloaded')
        image_url = img_element['src'] if img_element and 'src' in img_element.attrs else None

        # Convert the relative image URL to an absolute URL
        if image_url and not image_url.startswith('http'):
            image_url = base_url + image_url

        products.append({'name': name, 'price': price, 'image_url': image_url})

    return products

def main():
    base_url = 'https://www.pnp.co.za/'
    search_query = input("Enter the food item you are looking for: ")

    try:
        search_url = f"{base_url}pnpstorefront/pnp/en/search/?text={search_query}"
        print("Search URL:", search_url)

        # Use requests to get the page content
        content = get_page_content(search_url)

        data = parse_content(content)
        for product in data:
            print(f"Product: {product['name']}")
            print(f"Price: {product['price']}")
            print(f"Image URL: {product['image_url']}")
            print('-' * 40)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    main()
