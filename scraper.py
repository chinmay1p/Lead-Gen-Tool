from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import re
import requests
from bs4 import BeautifulSoup
from urllib.parse import quote_plus

def get_email(url):
    """Extract email from website"""
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers, timeout=5)
        soup = BeautifulSoup(response.text, 'html.parser')
        emails = set(re.findall(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+", soup.get_text()))
        return list(emails)[0] if emails else "Not found"
    except:
        return "Not found"

def scrape_maps(industry, city, min_companies=5, max_companies=25):
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument("user-agent=Mozilla/5.0")

    driver = webdriver.Chrome(options=options)
    search_url = f"https://www.yellowpages.com/search?search_terms={quote_plus(industry)}&geo_location_terms={quote_plus(city)}"

    driver.get(search_url)
    time.sleep(5)

    results = []
    cards = driver.find_elements(By.XPATH, '//div[@class="result"]')
    count = 0

    for card in cards:
        if count >= max_companies:
            break

        try:
            name = card.find_element(By.XPATH, './/a[@class="business-name"]').text
        except:
            name = "N/A"

        try:
            phone = card.find_element(By.XPATH, './/div[@class="phones phone primary"]').text
        except:
            phone = "N/A"

        try:
            address = card.find_element(By.XPATH, './/div[@class="info"]/div[@class="street-address"]').text
        except:
            address = "N/A"

        try:
            website_link = card.find_element(By.XPATH, './/a[contains(text(),"Website")]')
            website_url = website_link.get_attribute("href")
        except:
            website_url = ""

        email = get_email(website_url) if website_url else "Not found"

        results.append({
            "name": name,
            "phone": phone,
            "address": address,
            "website": website_url,
            "email": email
        })

        count += 1

    driver.quit()

    if len(results) < min_companies:
        return f"Only {len(results)} companies found. Try another input."

    return results