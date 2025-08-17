import re
from urllib.parse import urlparse, urljoin

import requests
from bs4 import BeautifulSoup, NavigableString
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.firefox import GeckoDriverManager


def create_firefox_driver():
    try:
        options = Options()
        options.add_argument("--headless")
        service = FirefoxService(GeckoDriverManager().install())
        driver = webdriver.Firefox(service=service, options=options)

        print("Firefox WebDriver initialized successfully!")
        return driver
    except Exception as e:
        print(f"Error initializing Firefox WebDriver: {e}")
        return None


def find_links():
    html_content = None
    try:
        html_content = driver.page_source
        print("Successfully fetched HTML content.")
        current_url = driver.current_url
        soup = BeautifulSoup(html_content, "html.parser")
        all_links = soup.find_all("a", string="ISO")
        for link in all_links:
            href = link.get("href")
            if href not in found_links:
                found_links.append(href)
            elif all_links == 0:
                not_found_links.append(current_url)
    except requests.exceptions.RequestException as e:
        print(f"Error fetching the URL: {e}")
    return found_links


def distro_meta_finder():
    html_content = driver.page_source
    print("Successfully fetched HTML content.")
    soup = BeautifulSoup(html_content, "html.parser")
    pattern = re.compile(r"news/distro/(.*?)\.xml")
    find = soup.find_all('a', href=pattern)
    if find:
        distro_rss = find[0].get('href')
        if distro_rss == None:
            distro_rss = "Unknown" #TODO: Find better way of getting distro name as there isnt always an RSS feed
        else:
            match = re.search(pattern, distro_rss)
            if match:
                distro = match.group(1)
            else:
                distro = "Unknown"
    else:
        distro = "Unknown"
    element= soup.find(attrs={"class": "TablesTitle"})
    if element:
        for content in element.contents:
            if isinstance(content, NavigableString) and content.strip():
                description = content.strip()
                print("Found the first piece of unwrapped text:")
                break
    else:
        description = ""
    return distro, distro_rss, description


def metadata_packerman(distro):
    pass
def parse(distro):  # TODO: Make it filter FTP from torrent servers etc
    ftp = []
    distro_website = []
    sourceforge = []
    for e in found_links:
        parsed_url = urlparse(e)
        hostname = parsed_url.hostname
        if parsed_url.scheme == "ftp":
            ftp.append(e)
            print("FTP: " + e)
        elif hostname and hostname.endswith("sourceforge.net"):
            sourceforge.append(e)
            print("SOURCEFORGE: " + e)
        elif hostname and hostname.endswith(distro):
            distro_website.append(e)
            print("(distro_website(S): " + e)
    print("Found links for:")
    print(ftp)
    print(distro_website)
    print(sourceforge)
    print("Did not find links for:")
    print(not_found_links)

if __name__ == "__main__":
    driver = None
    found_links = []
    not_found_links = []
    print(
        "Hi Welcome to Distrowatch ISO scrapper! Do you want to scrap distro names or links (dn, dl)"
    )
    userInput = input()
    if userInput == "dl":
        print("Which Distro?")
        distro = input()
        try:
            driver = create_firefox_driver()
            if driver:
                driver.get("https://distrowatch.com/" + distro)
                results = find_links()
                parse(results, distro)
        except Exception as e:
            print(f"An error occurred during script execution: {e}")
        finally:
            if driver:
                print("Closing Firefox browser.")
                driver.quit()
            else:
                print("Driver was not initialized, nothing to close.")
    elif userInput == "dn":
        print("Please input how many times you want it to find a random distro link")
        userInput = input()
        i = 0
        while i < int(userInput):
            driver = create_firefox_driver()
            if driver:
                driver.get("https://distrowatch.com/")
                random_distribution_input = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable(
                        (By.XPATH, "//input[@value='Random Distribution']")
                    )
                )
                random_distribution_input.click()
                driver.get(driver.current_url)
                found_links = find_links()
                distro_results = distro_meta_finder();
                print(distro_results)
                driver.quit()
                i = i + 1
            parse(distro_results)
