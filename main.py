import requests
import os
from dotenv import load_dotenv
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.firefox import GeckoDriverManager


def create_firefox_driver():
    try:
        #load_dotenv()
        #github_token = os.getenv("GH_TOKEN")
        options = Options()
        options.add_argument("--headless")
        service = FirefoxService(GeckoDriverManager().install())
        driver = webdriver.Firefox(service=service, options = options)

        print("Firefox WebDriver initialized successfully!")
        return driver
    except Exception as e:
        print(f"Error initializing Firefox WebDriver: {e}")
        return None


def find_links():
    html_content = None
    # current_link = driver.current_url

    try:
        html_content = driver.page_source
        print("Successfully fetched HTML content.")
        soup = BeautifulSoup(html_content, "html.parser")
        all_links = soup.find_all("a", string="ISO")
        for link in all_links:
            href = link.get("href")
            if href not in found_links:
                found_links.append(href)
            else:
                continue
    except requests.exceptions.RequestException as e:
        print(f"Error fetching the URL: {e}")
    return found_links


def parse(results):  # TODO: Make it filter FTP from torrent servers etc
    print(results)


def cherry_picker():
    """TODO: add a function that goes into the links and tries to find a download button and copy the link"""
    """for certain links that dont already open a download prompt"""
    pass


if __name__ == "__main__":
    driver = None
    found_links = []
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
                parse(results)
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
                results = find_links()
                driver.quit()
                i = i + 1
        parse(results)
