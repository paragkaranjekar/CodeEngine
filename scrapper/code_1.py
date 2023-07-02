from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from bs4 import BeautifulSoup

s = Service('chromedriver.exe')
driver = webdriver.Chrome(service=s)

# The base URL for the pages to scrape
page_URL = "https://www.codechef.com/practice"

# Function to get all the 'a' tags from a given URL


def get_a_tags(url):
    # Load the URL in the browser
    driver.get(url)
    # Wait for 7 seconds to ensure the page is fully loaded
    time.sleep(7)
    # Find all the 'a' elements on the page
    links = driver.find_elements(By.TAG_NAME, "a")
    ans = []
    # Iterate over each 'a' element
    for i in links:
        try:
            if "/problems/" in i.get_attribute("href"):
                ans.append(i.get_attribute("href"))
        except:
            pass
    # Remove duplicate links using set
    ans = list(set(ans))
    return ans


# List to store the final list of links
my_ans = []
my_ans += (get_a_tags(page_URL))

# Remove any duplicates that might have been introduced in the process
my_ans = list(set(my_ans))

# Open a file to write the results to
with open('codechef.txt', 'a') as f:
    for j in my_ans:
        f.write(j+'\n')

print(len(my_ans))
driver.quit()
