import re
import threading
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

# A lock for thread-safe access to shared data
lock = threading.Lock()

def create_firefox_driver():
    """Initializes and returns a new Firefox WebDriver instance."""
    try:
        options = Options()
        options.add_argument("--headless")
        service = FirefoxService(GeckoDriverManager().install())
<<<<<<< HEAD
        driver = webdriver.Firefox(service=service)
=======
        driver = webdriver.Firefox(service=service, options=options)

        print("Firefox WebDriver initialized successfully!")
>>>>>>> parent of 5108ef1 (feat(main.py):added back dl func)
        return driver
    except Exception as e:
        print(f"Error initializing Firefox WebDriver: {e}")
        return None

def navigate_dn_thread(thread_id, shared_content, shared_not_found_links):
    """
    Function to be executed by each thread.
    It scrapes a single random distribution.
    """
    driver = create_firefox_driver()
    if not driver:
        print(f"Thread {thread_id}: Failed to create driver. Exiting.")
        return

    try:
        driver.get("https://distrowatch.com/")
        random_distribution_input = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//input[@value='Random Distribution']"))
        )
        random_distribution_input.click()
        current_url = driver.current_url
        driver.get(current_url)
<<<<<<< HEAD
        
        # Wait for the main page content to load
        wait = WebDriverWait(driver, 10)
        wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "Info")))

        distro, distro_rss, description = distro_meta_finder(driver)
        found_links = find_links(driver)

        print(f"Thread {thread_id}: Distro: {distro}")
        print(f"Thread {thread_id}: Distro RSS: {distro_rss}")
        print(f"Thread {thread_id}: Distro Desc: {description}")
        
        # Use the lock to safely update shared lists
        with lock:
            if not found_links:
                print(f"Thread {thread_id}: Could not find links for {distro}")
                shared_not_found_links.append(distro)
            else:
                print(f"Thread {thread_id}: Found links: {found_links}")
                shared_content.extend(found_links)
    
    except Exception as e:
        print(f"Thread {thread_id}: An error occurred: {e}")
    finally:
        if driver:
            driver.quit()
=======
        distro_info = distro_meta_finder(driver)
        links = find_links(driver)
>>>>>>> parent of 5108ef1 (feat(main.py):added back dl func)

def find_links(driver):
    """Finds 'ISO' links on the current page."""
    found_links = []
    try:
        html_content = driver.page_source
        soup = BeautifulSoup(html_content, "html.parser")
        all_links = soup.find_all("a", string="ISO")
        for link in all_links:
            href = link.get("href")
            if href:
                found_links.append(href)
    except Exception as e:
        print(f"Error finding links: {e}")
    return found_links

def distro_meta_finder(driver):
    """Finds distro metadata like name, RSS, and description."""
    distro, distro_rss, description = "Unknown", "Unknown", ""
    html_content = driver.page_source
    soup = BeautifulSoup(html_content, "html.parser")
    
    # Find RSS link
    pattern = re.compile(r"news/distro/(.*?)\.xml")
    find = soup.find("a", href=pattern)
    if find:
        distro_rss = find.get("href")
        match = re.search(pattern, distro_rss)
        if match:
            distro = match.group(1)

    # Find description
    element = soup.find(attrs={"class": "TablesTitle"})
    if element:
        for content_part in element.contents:
            if isinstance(content_part, NavigableString) and content_part.strip():
                description = content_part.strip()
                break
    return distro, distro_rss, description

def metadata_packerman(file_path, content_list):
    """Writes the content of a list to a file."""
    with open(file_path, 'w') as file:
        for item in content_list:
            file.write(item + '\n')

def navigate_dl_single(distroname):
    """Scrapes a single, named distribution."""
    driver = create_firefox_driver()
    if not driver:
        return
    try:
        driver.get("https://distrowatch.com/")
        input_field = driver.find_element(By.NAME, "distribution")
        input_field.send_keys(distroname + Keys.ENTER)
        wait = WebDriverWait(driver, 10)
        info_element = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "Info")))
        distro, distro_rss, description = distro_meta_finder(driver)
        found_links = find_links(driver)
        
        print("Distro: " + distro)
        print("Distro RSS: " + distro_rss)
        print("Distro Desc: " + description)
        
        if not found_links:
            print(f"Could not find links for {distro}")
        else:
            print("Found links")
            print(found_links)
        
        return found_links
    
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        driver.quit()


if __name__ == "__main__":
    found_links_master = []
    not_found_links_master = []
    
    print("Hi Welcome to Distrowatch ISO scrapper! Do you want to scrap distro names or links (dn, dl)")
    userInput = input()

    if userInput == "dn":
        print("Please input how many threads you want to run to find random distro links")
        try:
            num_threads = int(input())
        except ValueError:
            print("Invalid input. Using 1 thread.")
            num_threads = 1
        
        threads = []
        for i in range(num_threads):
            thread = threading.Thread(
                target=navigate_dn_thread, 
                args=(i, found_links_master, not_found_links_master)
            )
            threads.append(thread)
            thread.start()
        
        for thread in threads:
            thread.join() # Wait for all threads to finish

    elif userInput == "dl":
<<<<<<< HEAD
        print("What is the Name of the distro?")
        distroname = input()
        found_links_master = navigate_dl_single(distroname)

    # Save results to file
    if found_links_master:
        metadata_packerman("links_output.txt", found_links_master)
    if not_found_links_master:
        metadata_packerman("not_found_distros.txt", not_found_links_master)

    print("Scraping complete.")
=======
        pass
    metadata_packerman()
>>>>>>> parent of 5108ef1 (feat(main.py):added back dl func)
