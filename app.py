from flask import Flask, render_template, request, jsonify, redirect, url_for
from datetime import datetime, timedelta
import sqlite3
import json
from pathlib import Path

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yellowknife-grocery-tracker-2025'

# Database setup
DATABASE = 'grocery_prices.db'

def get_db():
    """Get database connection"""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initialize the database with tables"""
    with app.app_context():
        db = get_db()
        db.execute('''
            CREATE TABLE IF NOT EXISTS stores (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                location TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        db.execute('''
            CREATE TABLE IF NOT EXISTS categories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        db.execute('''
            CREATE TABLE IF NOT EXISTS items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                category_id INTEGER,
                unit TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (category_id) REFERENCES categories (id)
            )
        ''')
        db.execute('''
            CREATE TABLE IF NOT EXISTS prices (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                item_id INTEGER NOT NULL,
                store_id INTEGER NOT NULL,
                price REAL NOT NULL,
                date DATE NOT NULL,
                notes TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (item_id) REFERENCES items (id),
                FOREIGN KEY (store_id) REFERENCES stores (id)
            )
        ''')
        
        # Add some default stores in Yellowknife
        stores = [
            ('Independent Grocer', 'Yellowknife, NT'),
            ('Extra Foods', 'Yellowknife, NT'),
            ('The Co-op', 'Yellowknife, NT'),
            ('Save-On-Foods', 'Yellowknife, NT')
        ]
        
        for store_name, location in stores:
            try:
                db.execute('INSERT INTO stores (name, location) VALUES (?, ?)', (store_name, location))
            except sqlite3.IntegrityError:
                pass  # Store already exists
        
        # Add default categories
        categories = ['Produce', 'Dairy', 'Meat', 'Bakery', 'Pantry', 'Frozen', 'Beverages', 'Snacks']
        for category in categories:
            try:
                db.execute('INSERT INTO categories (name) VALUES (?)', (category,))
            except sqlite3.IntegrityError:
                pass  # Category already exists
        
        db.commit()

@app.route('/')
def index():
    """Main dashboard"""
    return render_template('index.html')

@app.route('/api/stores', methods=['GET', 'POST'])
def stores():
    """Get all stores or add a new one"""
    db = get_db()
    
    if request.method == 'POST':
        data = request.json
        try:
            db.execute('INSERT INTO stores (name, location) VALUES (?, ?)', 
                      (data['name'], data.get('location', '')))
            db.commit()
            return jsonify({'success': True})
        except sqlite3.IntegrityError:
            return jsonify({'success': False, 'error': 'Store already exists'}), 400
    
    stores = db.execute('SELECT * FROM stores ORDER BY name').fetchall()
    return jsonify([dict(store) for store in stores])

@app.route('/api/categories', methods=['GET', 'POST'])
def categories():
    """Get all categories or add a new one"""
    db = get_db()
    
    if request.method == 'POST':
        data = request.json
        try:
            db.execute('INSERT INTO categories (name) VALUES (?)', (data['name'],))
            db.commit()
            return jsonify({'success': True})
        except sqlite3.IntegrityError:
            return jsonify({'success': False, 'error': 'Category already exists'}), 400
    
    categories = db.execute('SELECT * FROM categories ORDER BY name').fetchall()
    return jsonify([dict(category) for category in categories])

@app.route('/api/items', methods=['GET', 'POST'])
def items():
    """Get all items or add a new one"""
    db = get_db()
    
    if request.method == 'POST':
        data = request.json
        db.execute('INSERT INTO items (name, category_id, unit) VALUES (?, ?, ?)',
                  (data['name'], data['category_id'], data.get('unit', 'each')))
        db.commit()
        return jsonify({'success': True})
    
    items = db.execute('''
        SELECT items.*, categories.name as category_name 
        FROM items 
        LEFT JOIN categories ON items.category_id = categories.id 
        ORDER BY items.name
    ''').fetchall()
    return jsonify([dict(item) for item in items])

@app.route('/api/prices', methods=['GET', 'POST'])
def prices():
    """Get all prices or add a new price entry"""
    db = get_db()
    
    if request.method == 'POST':
        data = request.json
        db.execute('''
            INSERT INTO prices (item_id, store_id, price, date, notes) 
            VALUES (?, ?, ?, ?, ?)
        ''', (data['item_id'], data['store_id'], data['price'], 
              data.get('date', datetime.now().strftime('%Y-%m-%d')), 
              data.get('notes', '')))
        db.commit()
        return jsonify({'success': True})
    
    # Get query parameters for filtering
    days = request.args.get('days', 30, type=int)
    item_id = request.args.get('item_id', type=int)
    
    query = '''
        SELECT prices.*, items.name as item_name, items.unit,
               stores.name as store_name, categories.name as category_name
        FROM prices
        JOIN items ON prices.item_id = items.id
        JOIN stores ON prices.store_id = stores.id
        LEFT JOIN categories ON items.category_id = categories.id
        WHERE date >= date('now', '-' || ? || ' days')
    '''
    params = [days]
    
    if item_id:
        query += ' AND prices.item_id = ?'
        params.append(item_id)
    
    query += ' ORDER BY prices.date DESC, items.name'
    
    prices = db.execute(query, params).fetchall()
    return jsonify([dict(price) for price in prices])

@app.route('/api/price-trends/<int:item_id>')
def price_trends(item_id):
    """Get price trends for a specific item"""
    db = get_db()
    days = request.args.get('days', 90, type=int)
    
    trends = db.execute('''
        SELECT prices.date, prices.price, stores.name as store_name, prices.notes
        FROM prices
        JOIN stores ON prices.store_id = stores.id
        WHERE prices.item_id = ? AND date >= date('now', '-' || ? || ' days')
        ORDER BY prices.date DESC
    ''', (item_id, days)).fetchall()
    
    return jsonify([dict(trend) for trend in trends])

@app.route('/api/daily-summary')
def daily_summary():
    """Get summary of prices entered today"""
    db = get_db()
    today = datetime.now().strftime('%Y-%m-%d')
    
    summary = db.execute('''
        SELECT prices.*, items.name as item_name, items.unit,
               stores.name as store_name, categories.name as category_name
        FROM prices
        JOIN items ON prices.item_id = items.id
        JOIN stores ON prices.store_id = stores.id
        LEFT JOIN categories ON items.category_id = categories.id
        WHERE date = ?
        ORDER BY items.name
    ''', (today,)).fetchall()
    
    return jsonify([dict(row) for row in summary])

@app.route('/api/price-comparison')
def price_comparison():
    """Compare latest prices across stores"""
    db = get_db()
    
    # Get the latest price for each item at each store
    comparison = db.execute('''
        WITH LatestPrices AS (
            SELECT item_id, store_id, price, date,
                   ROW_NUMBER() OVER (PARTITION BY item_id, store_id ORDER BY date DESC) as rn
            FROM prices
        )
        SELECT items.name as item_name, items.unit,
               stores.name as store_name,
               LatestPrices.price, LatestPrices.date,
               categories.name as category_name
        FROM LatestPrices
        JOIN items ON LatestPrices.item_id = items.id
        JOIN stores ON LatestPrices.store_id = stores.id
        LEFT JOIN categories ON items.category_id = categories.id
        WHERE rn = 1
        ORDER BY items.name, stores.name
    ''').fetchall()
    
    return jsonify([dict(row) for row in comparison])

if __name__ == '__main__':
    # Initialize database
    init_db()
    
    # Run the app
    print("\n" + "="*50)
    print("Yellowknife Grocery Price Tracker")
    print("="*50)
    print("\nStarting server at http://127.0.0.1:5000")
    print("Press CTRL+C to quit\n")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
