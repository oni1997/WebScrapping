from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time

def get_page_content_with_selenium(url):
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run in headless mode without opening a browser window
    driver = webdriver.Chrome(options=chrome_options)
    
    try:
        driver.get(url)
        time.sleep(3)  # Give the page some time to load the content (adjust this if needed)
        return driver.page_source
    finally:
        driver.quit()

def get_page_content(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.content
    else:
        raise Exception(f"Failed to retrieve the page. Status Code: {response.status_code}")

def parse_content(content):
    soup = BeautifulSoup(content, 'html.parser')
    products = []

    # Find the elements containing product names and prices
    product_elements = soup.find_all('div', class_='product-item')

    for product_element in product_elements:
        name = product_element.find('a', class_='product-name').text.strip()
        price = product_element.find('span', class_='price').text.strip()
        products.append({'name': name, 'price': price})

    return products

def main():
    base_url = 'https://www.pnp.co.za/'
    search_query = input("Enter the food item you are looking for: ")

    try:
        search_url = f"{base_url}pnpstorefront/pnp/en/search/?text={search_query}"
        print("Search URL:", search_url)

        # Use Selenium to get the page content
        content = get_page_content_with_selenium(search_url)
        # Alternatively, you can use the following line to get the page content without Selenium
        # content = get_page_content(search_url)

        data = parse_content(content)
        print(data)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    main()
