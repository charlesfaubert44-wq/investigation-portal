"""
Base scraper class for grocery stores
"""

import requests
from bs4 import BeautifulSoup
from abc import ABC, abstractmethod
import logging
import time
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class BaseScraper(ABC):
    """Base class for all grocery store scrapers"""
    
    def __init__(self, store_name, base_url, user_agent=None):
        self.store_name = store_name
        self.base_url = base_url
        self.user_agent = user_agent or 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': self.user_agent,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        })
        
    def fetch_page(self, url, max_retries=3):
        """Fetch a page with retry logic"""
        for attempt in range(max_retries):
            try:
                response = self.session.get(url, timeout=30)
                response.raise_for_status()
                return response.text
            except requests.RequestException as e:
                logger.warning(f"Attempt {attempt + 1} failed for {url}: {str(e)}")
                if attempt < max_retries - 1:
                    time.sleep(2 ** attempt)  # Exponential backoff
                else:
                    logger.error(f"Failed to fetch {url} after {max_retries} attempts")
                    raise
        return None
    
    def parse_html(self, html):
        """Parse HTML content"""
        return BeautifulSoup(html, 'lxml')
    
    @abstractmethod
    def scrape_products(self, category=None):
        """
        Scrape products from the store
        
        Returns:
            list: List of dicts with format:
                {
                    'name': str,
                    'price': float,
                    'unit': str,
                    'category': str,
                    'url': str (optional),
                    'image_url': str (optional),
                    'on_sale': bool (optional)
                }
        """
        pass
    
    @abstractmethod
    def get_available_categories(self):
        """
        Get list of available product categories
        
        Returns:
            list: List of category names
        """
        pass
    
    def clean_price(self, price_text):
        """Clean and convert price text to float"""
        if not price_text:
            return None
        
        # Remove currency symbols and whitespace
        cleaned = price_text.replace('$', '').replace(',', '').strip()
        
        # Handle price ranges (take the first price)
        if '-' in cleaned:
            cleaned = cleaned.split('-')[0].strip()
        
        try:
            return float(cleaned)
        except ValueError:
            logger.warning(f"Could not parse price: {price_text}")
            return None
    
    def clean_product_name(self, name):
        """Clean product name"""
        if not name:
            return None
        return ' '.join(name.split()).strip()
