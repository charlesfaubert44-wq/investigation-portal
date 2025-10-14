import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Application configuration"""
    
    # Flask
    SECRET_KEY = os.getenv('SECRET_KEY', 'yellowknife-grocery-tracker-dev-key')
    FLASK_ENV = os.getenv('FLASK_ENV', 'development')
    
    # Database
    DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///grocery_prices.db')
    
    # Scraping
    SCRAPING_ENABLED = os.getenv('SCRAPING_ENABLED', 'true').lower() == 'true'
    SCRAPING_INTERVAL_HOURS = int(os.getenv('SCRAPING_INTERVAL_HOURS', '6'))
    USER_AGENT = os.getenv('USER_AGENT', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')
    
    # Server
    PORT = int(os.getenv('PORT', '5000'))
    HOST = os.getenv('HOST', '0.0.0.0')
    
    # Store URLs (to be updated with actual store websites)
    STORE_URLS = {
        'Independent Grocer': 'https://www.atlanticsuperstore.ca/',  # Loblaws family
        'Extra Foods': 'https://www.extrafoods.ca/',
        'The Co-op': 'https://www.coopathome.ca/',
        'Save-On-Foods': 'https://www.saveonfoods.com/'
    }
