import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager


def create_firefox_driver():
    try:
        # Set up the Firefox service using GeckoDriverManager
        service = FirefoxService(GeckoDriverManager().install())

        # Initialize the Firefox WebDriver
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
                input_element.send_keys(distro + Keys.ENTER)
                try:
                    parse(keywords)
                except Exception as e:
                    print(f"An error occurred during script execution: {e}")
            except Exception as e:
                print(f"An error occurred during script execution: {e}")
    except Exception as e:
        print(f"An error occurred during script execution: {e}")


def parse(keywords):
    response = requests.get(driver.current_url)
    response.raise_for_status()  # Raise an HTTPError for bad responses (4xx or 5xx)
    html_content = response.text
    soup = BeautifulSoup(html_content, "html.parser")
    links = soup.find_all("a")
    for keyword in keywords:
        for link in links:
            href = link.get("href")
            link_text = link.get_text(strip=True)
            if href:
                if (
                    keyword.lower() in href.lower()
                    or keyword.lower() in link_text.lower()
                ):
                    found_links.append({"text": link_text, "href": href})
                    print("  Found Link:")
                    print("    Text: {link_text}")
                    print("    URL: {href}\n")
            if not found_links:
                print(f"No links found containing the keyword '{keyword}'.")


if __name__ == "__main__":
    driver = None
    found_links = []
    keywords = []
    try:
        driver = create_firefox_driver()
        if driver:
            driver.get("https://distrowatch.com")
            search("NixOS")
    except Exception as e:
        print(f"An error occurred during script execution: {e}")
    finally:
        # Always close the browser when done
        if driver:
            print("Closing Firefox browser.")
            driver.quit()
        else:
            print("Driver was not initialized, nothing to close.")
