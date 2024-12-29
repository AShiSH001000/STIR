from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from pymongo import MongoClient
from datetime import datetime
from datetime import time
import uuid
import requests
from config import TWITTER_USERNAME, TWITTER_PASSWORD, MONGODB_URI, CHROMEDRIVER_PATH
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager


def setup_driver():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    
    service = Service()
    return webdriver.Chrome(service=service, options=chrome_options)
def login_twitter(driver):
    driver.get('https://twitter.com/login')
    wait = WebDriverWait(driver, 200)
    
    # Login form
    username_input = wait.until(EC.presence_of_element_located((By.NAME, "text")))
    username_input.send_keys(TWITTER_USERNAME)
    driver.find_element(By.XPATH, "//span[text()='Next']").click()
    
    password_input = wait.until(EC.presence_of_element_located((By.NAME, "password")))
    password_input.send_keys(TWITTER_PASSWORD)
    driver.find_element(By.XPATH, "//span[text()='Log in']").click()


def get_trending_topics(driver):
    try:
        wait = WebDriverWait(driver, 15)
        trending_section = wait.until(EC.presence_of_element_located(
            (By.XPATH, "/html/body/div[1]/div/div/div[2]/main/div/div/div/div[2]/div/div[2]/div/div/div/div[4]/section")
        ))
        trends = trending_section.find_elements(By.XPATH, ".//span")[:5]
        return [trend.text for trend in trends if trend.text.strip()]
    except Exception as e:
        print(f"Error fetching trending topics: {e}")
        raise


def save_to_mongodb(trends, ip_address):
    try:
        client = MongoClient(MONGODB_URI)
        db = client.twitter_trends
        collection = db.trends

        # Prepare the record
        record = {
            "_id": str(uuid.uuid4()),
            "timestamp": datetime.now(),
            "ip_address": ip_address,
        }

        # Add trends to the record
        for i, trend in enumerate(trends, 1):
            record[f"nameoftrend{i}"] = trend

        # Insert into MongoDB
        collection.insert_one(record)
        print("Record successfully saved to MongoDB.")
        return record
    except Exception as e:
        print(f"Error saving to MongoDB: {e}")
        raise
def save_to_mongodb(trends, ip_address):
    print("Mock Save to MongoDB")
    print("Trends:", trends)
    print("IP Address:", ip_address)
    return {"trends": trends, "ip_address": ip_address}

def scrape_trends():
    driver = setup_driver()
    try:
        # Login to Twitter
        login_twitter(driver)

        # Get trending topics
        trends = get_trending_topics(driver)
        print("Fetched trends:", trends)

        # Fetch external IP address
        ip_address = requests.get("https://api.ipify.org").text

        # Return the data directly as a dictionary
        return {
            "trends": trends,
            "ip_address": ip_address,
            "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        }
    finally:
        driver.quit()


