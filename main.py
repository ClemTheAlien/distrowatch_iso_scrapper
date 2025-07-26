from selenium import webdriver
from selenium.webdriver.common.by import By
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


if __name__ == "__main__":
    driver = None
    try:
        driver = create_firefox_driver()

        if driver:
            driver.get("https://distrowatch.com")
            try:
                input_element = driver.find_element(
                    By.CSS_SELECTOR, "input[value='Type Distribution Name']"
                )
                input_element.send_keys("NixOS"+ Keys.ENTER)
            except Exception as e:
                print(f"An error occurred during script execution: {e}")
    except Exception as e:
        print(f"An error occurred during script execution: {e}")
    finally:
        # Always close the browser when done
        if driver:
            print("Closing Firefox browser.")
            driver.quit()
        else:
            print("Driver was not initialized, nothing to close.")
