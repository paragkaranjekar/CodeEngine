import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time

s = Service('chromedriver.exe')
driver = webdriver.Chrome(service=s)

heading_class = ".mr-2.text-label-1"
body_class = ".px-5.pt-4"
difficulty_class = '//*[@id="qd-content"]/div[1]/div/div/div/div[2]/div/div/div[1]/div/div[2]/div[1]'
index = 1
QDATA_FOLDER = "Qdata"

links = []


def add_link_to_Qindex_file(text):
    with open('scrapper\link.txt', 'a') as f:
        f.write(text)


def add_text_to_index_file(text):
    with open('scrapper\heading.txt', 'a') as f:
        f.write(text+'\n')


def add_difficulty(text):
    with open('scrapper\difficulty.txt', 'a') as f:
        f.write(text+'\n')


def create_and_add_text_to_file(file_name, text):
    folder_path = os.path.join(QDATA_FOLDER, file_name)
    os.makedirs(folder_path, exist_ok=True)
    file_path = os.path.join(folder_path, file_name + ".txt")
    with open(file_path, "w", encoding="utf-8", errors="ignore") as new_file:
        new_file.write(text)


def get_array_of_links():
    with open('scrapper\Qindex.txt', 'r') as f:
        links = f.readlines()
        links = list(set(links))
    return links


def getPageData(url, index):
    try:
        driver.get(url)
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, body_class)))
        heading = driver.find_element(By.CSS_SELECTOR, heading_class)

        difficulty = driver.find_element(By.XPATH, difficulty_class)

        print(heading.text)
        if (heading.text):
            add_text_to_index_file(heading.text)
            add_difficulty(difficulty.text)
            add_link_to_Qindex_file(url)

        # body_element = driver.find_element(By.CLASS_NAME, body_class)
        # body_text = body_element.text
        # try:
        #     create_and_add_text_to_file(f"{str(index)}", body_text)
        # except UnicodeEncodeError:
        #     # Handle encoding issue by replacing the problematic character
        #     body_text = body_text.replace('\u2264', '<=')
        #     create_and_add_text_to_file(f"{str(index)}", body_text)

        return True
    except Exception as e:
        print(f"Error occurred while processing URL: {url}")
        print(e)
        return False


arr = get_array_of_links()

for link in arr:
    success = getPageData(link, index)
    if success:

        index += 1

driver.quit()
