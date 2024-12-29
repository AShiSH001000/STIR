# config.py
from dotenv import load_dotenv
import os

load_dotenv()
from urllib.parse import quote_plus

MONGODB_USER = "Ashishmaur42047"
MONGODB_PASSWORD = "Asm@12345"
MONGODB_HOST = "atlas-sql-676afba96422574f1e60c013-touer.a.query.mongodb.net"
MONGODB_DATABASE = "twitter_trends"

MONGODB_URI = f"mongodb+srv://{quote_plus(MONGODB_USER)}:{quote_plus(MONGODB_PASSWORD)}@{MONGODB_HOST}/{MONGODB_DATABASE}?retryWrites=true&w=majority"

# MONGODB_URI = os.getenv('MONGODB_URI', 'mongodb://localhost:27017')
PROXYMESH_HOST = os.getenv('PROXYMESH_HOST')
PROXYMESH_PORT = os.getenv('PROXYMESH_PORT')
TWITTER_USERNAME = os.getenv('TWITTER_USERNAME')
TWITTER_PASSWORD = os.getenv('TWITTER_PASSWORD')
CHROMEDRIVER_PATH = "C:/webdriver/chromedriver-win64/chromedriver.exe"