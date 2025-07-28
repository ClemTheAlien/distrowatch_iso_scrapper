import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager


def create_firefox_driver():
    try:
        options = Options()
        options.add_argument("--headless")
        service = FirefoxService(GeckoDriverManager().install())
        driver = webdriver.Firefox(service=service)

        print("Firefox WebDriver initialized successfully!")
        return driver
    except Exception as e:
        print(f"Error initializing Firefox WebDriver: {e}")
        return None


def search(distro):
    try:
        if distro is not None:
            print("Getting link for " + distro)
            try:
                input_element = driver.find_element(
                    By.CSS_SELECTOR, "input[value='Type Distribution Name']"
                )
                input_element.send_keys(distro, Keys.ENTER)
                try:
                    results = find_links()
                    parse(results)
                except Exception as e:
                    print(f"An error occurred during script execution1: {e}")
            except Exception as e:
                print(f"An error occurred during script execution2: {e}")
    except Exception as e:
        print(f"An error occurred during script execution3: {e}")


def find_links():  # TODO: make it stop scrapping only the front page by using current_link
    html_content = None
    keywords = ["iso", "ISO"]
    found_links = []
    # current_link = driver.current_url

    try:
        html_content = driver.page_source
        print("Successfully fetched HTML content.")
        soup = BeautifulSoup(html_content, "html.parser")
        all_links = soup.find_all("a",string="ISO")
        for link in all_links:
            href = link.get("href")
            found_links.append(link)
    except requests.exceptions.RequestException as e:
        print(f"Error fetching the URL: {e}")
    return found_links


def parse(results):  # TODO: Make it filter FTP from torrent servers etc
    print(results)


if __name__ == "__main__":
    driver = None
    distro = "Debian"
    try:
        driver = create_firefox_driver()
        if driver:
            driver.get("https://distrowatch.com/"+distro)
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
