from selenium import webdriver
from bs4 import BeautifulSoup

# Set up Selenium webdriver
driver = webdriver.Chrome('question-scrapper/chromedriver')  # Replace with the path to your chromedriver executable

# Open the desired page
driver.get('https://leetcode.com/problemset/all/')  # Replace with the URL of the page you want to open

# Extract the page source using Selenium
page_source = driver.page_source

# Close the Selenium webdriver
driver.quit()

# Parse the page source with BeautifulSoup
soup = BeautifulSoup(page_source, 'html.parser')

# Now you can work with the parsed HTML using BeautifulSoup
# For example, let's print the page title
print("Page Title:", soup.title.text)
