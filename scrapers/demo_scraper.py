"""
Demo scraper that generates sample data for testing
This demonstrates the data structure without actual web scraping
"""

from .base_scraper import BaseScraper
import random
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class DemoScraper(BaseScraper):
    """
    Demo scraper that generates realistic sample grocery data
    Use this to test the system before implementing real scrapers
    """
    
    SAMPLE_PRODUCTS = {
        'Produce': [
            ('Bananas', 'lb', (0.69, 1.29)),
            ('Apples - Gala', 'lb', (1.49, 2.99)),
            ('Tomatoes', 'lb', (1.99, 3.49)),
            ('Lettuce - Romaine', 'each', (2.49, 3.99)),
            ('Potatoes - Russet', '10lb bag', (4.99, 7.99)),
            ('Carrots', '2lb bag', (2.99, 4.49)),
            ('Onions - Yellow', 'lb', (0.99, 1.99)),
            ('Broccoli', 'each', (2.49, 3.99)),
        ],
        'Dairy': [
            ('Milk - 2L', '2L', (4.99, 6.99)),
            ('Butter - 454g', '454g', (5.99, 7.99)),
            ('Cheese - Cheddar 400g', '400g', (6.99, 9.99)),
            ('Yogurt - Greek 750g', '750g', (4.99, 6.49)),
            ('Eggs - Large Dozen', 'dozen', (4.49, 6.99)),
            ('Sour Cream - 500ml', '500ml', (3.99, 5.49)),
        ],
        'Meat': [
            ('Chicken Breast', 'lb', (6.99, 11.99)),
            ('Ground Beef - Lean', 'lb', (5.99, 9.99)),
            ('Pork Chops', 'lb', (5.49, 8.99)),
            ('Bacon - 500g', '500g', (6.99, 9.99)),
            ('Salmon Fillet', 'lb', (12.99, 18.99)),
        ],
        'Bakery': [
            ('White Bread - 570g', '570g', (2.99, 4.49)),
            ('Whole Wheat Bread', '570g', (3.49, 4.99)),
            ('Bagels - 6 pack', '6pk', (3.99, 5.99)),
            ('Croissants - 4 pack', '4pk', (4.99, 6.99)),
        ],
        'Pantry': [
            ('Pasta - 900g', '900g', (1.99, 3.49)),
            ('Rice - 2kg', '2kg', (4.99, 7.99)),
            ('Olive Oil - 1L', '1L', (8.99, 14.99)),
            ('Canned Tomatoes - 796ml', '796ml', (1.99, 2.99)),
            ('Peanut Butter - 1kg', '1kg', (6.99, 9.99)),
        ],
        'Frozen': [
            ('Frozen Pizza', 'each', (5.99, 8.99)),
            ('Ice Cream - 1.5L', '1.5L', (4.99, 7.99)),
            ('Frozen Vegetables - 750g', '750g', (3.49, 5.49)),
        ],
        'Beverages': [
            ('Orange Juice - 1.75L', '1.75L', (4.99, 6.99)),
            ('Coffee - 900g', '900g', (11.99, 16.99)),
            ('Pop - 12 pack', '12pk', (5.99, 8.99)),
        ]
    }
    
    def __init__(self, store_name='Demo Store', user_agent=None):
        super().__init__(
            store_name=store_name,
            base_url='https://demo.store',
            user_agent=user_agent
        )
        
    def scrape_products(self, category=None):
        """Generate demo product data"""
        logger.info(f"Generating demo data for {self.store_name}")
        
        products = []
        categories_to_scrape = [category] if category else self.SAMPLE_PRODUCTS.keys()
        
        for cat in categories_to_scrape:
            if cat not in self.SAMPLE_PRODUCTS:
                continue
                
            for product_name, unit, price_range in self.SAMPLE_PRODUCTS[cat]:
                # Generate random price within range
                price = round(random.uniform(price_range[0], price_range[1]), 2)
                
                # 20% chance of being on sale
                on_sale = random.random() < 0.2
                if on_sale:
                    price = round(price * 0.85, 2)  # 15% discount
                
                products.append({
                    'name': product_name,
                    'price': price,
                    'unit': unit,
                    'category': cat,
                    'on_sale': on_sale,
                    'source': 'auto-fetched'
                })
        
        logger.info(f"Generated {len(products)} demo products")
        return products
    
    def get_available_categories(self):
        """Return available categories"""
        return list(self.SAMPLE_PRODUCTS.keys())
