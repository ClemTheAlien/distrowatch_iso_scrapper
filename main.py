import re
from urllib.parse import urlparse

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

def navigate_dn():
    global driver
    if driver:
        driver.get("https://distrowatch.com/")
        random_distribution_input = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                        (By.XPATH, "//input[@value='Random Distribution']")
                    )
                )
        random_distribution_input.click()
        current_url=driver.current_url
        driver.get(current_url)
        distro_info = distro_meta_finder(driver)
        links = find_links(driver)

def find_links(driver):
    global found_links
    global distro
    html_content = None
    try:
        html_content = driver.page_source
        print("Successfully fetched HTML content for Links Finder")
        soup = BeautifulSoup(html_content, "html.parser")
        all_links = soup.find_all("a", string="ISO")
        for link in all_links:
            href = link.get("href")
            if href not in found_links:
                found_links.append(href)
            elif not all_links:
                ncontinue
    except requests.exceptions.RequestException as e:
        print(f"Error fetching the URL: {e}")
    return found_links


def distro_meta_finder(driver):
    global distro_rss
    global distro
    global description
    html_content = driver.page_source
    print("Successfully fetched HTML content for Metadata Finder")
    soup = BeautifulSoup(html_content, "html.parser")
    pattern = re.compile(r"news/distro/(.*?)\.xml")
    find = soup.find_all("a", href=pattern)
    if find:
        distro_rss = find[0].get("href")
        if distro_rss == "":
            distro_rss = "Unknown"  # TODO: Find better way of getting distro name as there isnt always an RSS feed
        else:
            match = re.search(pattern, distro_rss)
            if match:
                distro = match.group(1)
            else:
                distro = "Unknown"
    else:
        distro = "Unknown"
    element = soup.find(attrs={"class": "TablesTitle"})
    if element:
        for content in element.contents:
            if isinstance(content, NavigableString) and content.strip():
                description = content.strip()
                break
    else:
        description = ""
    return distro, distro_rss, description


def metadata_packerman():
    file_path = "links_output.txt"
    with open(file_path, 'w') as file:
        for e in content:
            file.write(e + '\n')   


if __name__ == "__main__":
    content = []
    i = 0
    driver = None
    distro = None
    distro_rss = None
    description= None 
    found_links = []
    not_found_links = []
    print(
        "Hi Welcome to Distrowatch ISO scrapper! Do you want to scrap distro names or links (dn, dl)"
    )
    driver = create_firefox_driver()
    userInput = input()
    if userInput == "dn":
        print("Please input how many times you want it to find a random distro link")
        userInput = input()
        while i < int(userInput):
            distro = ""
            distro_rss = ""
            description= "" 
            found_links = []
            not_found_links = ""
            navigate_dn()
            print("Distro: "+distro)
            print("Distro RSS: "+distro_rss)
            print("Distro Desc: "+description)
            print(i)
            if not found_links: 
                print ("Could not find links for")
                not_found_links = distro
                print(not_found_links)
            else:
                print ("Found links")
                print(found_links)
            for e in found_links:
                content.append(e)
            i+=1
    
    elif userInput == "dl":
        pass
    metadata_packerman()