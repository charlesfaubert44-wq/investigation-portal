"""
Manager for coordinating all scrapers and storing results
"""

import logging
from datetime import datetime
import sqlite3
from .demo_scraper import DemoScraper
from .independent_scraper import IndependentScraper

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ScraperManager:
    """Manages all store scrapers and data storage"""
    
    def __init__(self, db_path='grocery_prices.db', use_demo=True):
        self.db_path = db_path
        self.use_demo = use_demo
        self.scrapers = {}
        self._init_scrapers()
        
    def _init_scrapers(self):
        """Initialize scrapers for each store"""
        if self.use_demo:
            # Use demo scrapers for testing
            self.scrapers = {
                'Independent Grocer': DemoScraper('Independent Grocer'),
                'Extra Foods': DemoScraper('Extra Foods'),
                'The Co-op': DemoScraper('The Co-op'),
                'Save-On-Foods': DemoScraper('Save-On-Foods')
            }
            logger.info("Initialized DEMO scrapers (generating sample data)")
        else:
            # Use real scrapers (not fully implemented)
            self.scrapers = {
                'Independent Grocer': IndependentScraper(),
                # Add other store scrapers here when implemented
            }
            logger.info("Initialized real scrapers")
    
    def get_db(self):
        """Get database connection"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn
    
    def get_or_create_item(self, db, name, category_name, unit):
        """Get item ID or create if doesn't exist"""
        # Get category ID
        category = db.execute(
            'SELECT id FROM categories WHERE name = ?', 
            (category_name,)
        ).fetchone()
        
        if not category:
            # Create category if it doesn't exist
            db.execute('INSERT INTO categories (name) VALUES (?)', (category_name,))
            db.commit()
            category = db.execute(
                'SELECT id FROM categories WHERE name = ?', 
                (category_name,)
            ).fetchone()
        
        category_id = category['id']
        
        # Check if item exists
        item = db.execute(
            'SELECT id FROM items WHERE name = ? AND category_id = ?',
            (name, category_id)
        ).fetchone()
        
        if item:
            return item['id']
        
        # Create new item
        db.execute(
            'INSERT INTO items (name, category_id, unit) VALUES (?, ?, ?)',
            (name, category_id, unit)
        )
        db.commit()
        
        item = db.execute(
            'SELECT id FROM items WHERE name = ? AND category_id = ?',
            (name, category_id)
        ).fetchone()
        
        return item['id']
    
    def get_store_id(self, db, store_name):
        """Get store ID by name"""
        store = db.execute(
            'SELECT id FROM stores WHERE name = ?',
            (store_name,)
        ).fetchone()
        
        return store['id'] if store else None
    
    def scrape_store(self, store_name, save_to_db=True):
        """
        Scrape a single store
        
        Args:
            store_name: Name of the store to scrape
            save_to_db: Whether to save results to database
            
        Returns:
            dict: Results with 'success', 'products_count', and 'products' list
        """
        if store_name not in self.scrapers:
            logger.error(f"No scraper found for {store_name}")
            return {'success': False, 'error': 'Store not found'}
        
        try:
            logger.info(f"Scraping {store_name}...")
            scraper = self.scrapers[store_name]
            products = scraper.scrape_products()
            
            if save_to_db and products:
                saved_count = self.save_products(store_name, products)
                logger.info(f"Scraped and saved {saved_count} products from {store_name}")
                return {
                    'success': True,
                    'products_count': len(products),
                    'saved_count': saved_count,
                    'products': products
                }
            
            return {
                'success': True,
                'products_count': len(products),
                'products': products
            }
            
        except Exception as e:
            logger.error(f"Error scraping {store_name}: {str(e)}")
            return {'success': False, 'error': str(e)}
    
    def scrape_all_stores(self, save_to_db=True):
        """
        Scrape all configured stores
        
        Returns:
            dict: Results for each store
        """
        logger.info("Starting scrape of all stores...")
        results = {}
        
        for store_name in self.scrapers.keys():
            results[store_name] = self.scrape_store(store_name, save_to_db)
        
        total_products = sum(r.get('products_count', 0) for r in results.values())
        logger.info(f"Scraping complete. Total products: {total_products}")
        
        return results
    
    def save_products(self, store_name, products):
        """
        Save scraped products to database
        
        Args:
            store_name: Name of the store
            products: List of product dicts
            
        Returns:
            int: Number of products saved
        """
        db = self.get_db()
        store_id = self.get_store_id(db, store_name)
        
        if not store_id:
            logger.error(f"Store not found in database: {store_name}")
            return 0
        
        today = datetime.now().strftime('%Y-%m-%d')
        saved_count = 0
        
        for product in products:
            try:
                # Get or create item
                item_id = self.get_or_create_item(
                    db,
                    product['name'],
                    product.get('category', 'General'),
                    product.get('unit', 'each')
                )
                
                # Check if price already exists for today
                existing = db.execute('''
                    SELECT id FROM prices 
                    WHERE item_id = ? AND store_id = ? AND date = ?
                ''', (item_id, store_id, today)).fetchone()
                
                notes = 'auto-fetched'
                if product.get('on_sale'):
                    notes += ' (on sale)'
                
                if existing:
                    # Update existing price
                    db.execute('''
                        UPDATE prices 
                        SET price = ?, notes = ?
                        WHERE id = ?
                    ''', (product['price'], notes, existing['id']))
                else:
                    # Insert new price
                    db.execute('''
                        INSERT INTO prices (item_id, store_id, price, date, notes)
                        VALUES (?, ?, ?, ?, ?)
                    ''', (item_id, store_id, product['price'], today, notes))
                
                saved_count += 1
                
            except Exception as e:
                logger.error(f"Error saving product {product.get('name')}: {str(e)}")
                continue
        
        db.commit()
        db.close()
        
        return saved_count
    
    def get_last_scrape_time(self, store_name=None):
        """Get the last time prices were auto-fetched"""
        db = self.get_db()
        
        if store_name:
            store_id = self.get_store_id(db, store_name)
            if not store_id:
                return None
            
            result = db.execute('''
                SELECT MAX(date) as last_date
                FROM prices
                WHERE store_id = ? AND notes LIKE '%auto-fetched%'
            ''', (store_id,)).fetchone()
        else:
            result = db.execute('''
                SELECT MAX(date) as last_date
                FROM prices
                WHERE notes LIKE '%auto-fetched%'
            ''').fetchone()
        
        db.close()
        return result['last_date'] if result else None
