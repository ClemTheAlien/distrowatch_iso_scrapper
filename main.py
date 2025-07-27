import time
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from undetected_geckodriver import Firefox
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException # Good to explicitly catch this
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


def search(distro): #TODO: Get this to work and not throw a 403 error
    try:
        if distro is not None:
            print("Getting link for " + distro)
            try:
                input_element = driver.find_element(
                    By.CSS_SELECTOR, "input[value='Type Distribution Name']"
                )
                input_element.send_keys(distro, Keys.ENTER)
                try:
                    results = parse()
                    print(results)
                except Exception as e:
                    print(f"An error occurred during script execution1: {e}")
            except Exception as e:
                print(f"An error occurred during script execution2: {e}")
    except Exception as e:
        print(f"An error occurred during script execution3: {e}")


def parse(): #TODO: Get this to work and not throw a 403 error
    keywords = ["release", "iso"]
    found_links = [] 

    try:
        print("Parsing: Waiting for links to be present...")
        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.TAG_NAME, "a"))
        )
        print("Links found on the page.")

        anchor_elements = driver.find_elements(By.TAG_NAME, "a")

        for link_element in anchor_elements:
            link_url = link_element.get_attribute("href")

            if link_url:
                link_string = str(link_url)

                for keyword in keywords:
                    if keyword.lower() in link_string.lower():
                        found_links.append(link_string)
                        break # Move to the next link once a keyword is found

    except TimeoutException:
        print(f"Parsing Timeout: No anchor elements found on page for {distro}.")
    except Exception as e:
        if distro:
             print(f"An error occurred during parsing for {distro}: {e}")
        else:
            print(f"An error occurred during parsing: {e}")
        raise 
    return found_links

if __name__ == "__main__":
    driver = None
    distro = None
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
            #driver.quit()
        else:
            print("Driver was not initialized, nothing to close.")
