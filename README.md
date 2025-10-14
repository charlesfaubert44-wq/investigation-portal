# 🛒 Yellowknife Grocery Price Tracker

A local web application for tracking daily grocery prices across different stores in Yellowknife, Northwest Territories. Monitor price trends, compare stores, and make informed shopping decisions.

## Features

- **📊 Daily Price Tracking**: Record prices for grocery items from multiple stores with dates
- **🏪 Multi-Store Support**: Pre-configured with major Yellowknife stores (Independent Grocer, Extra Foods, The Co-op, Save-On-Foods)
- **📈 Price Trends**: View historical price trends for individual items over time
- **💰 Price Comparison**: Compare latest prices across all stores to find the best deals
- **🗂️ Category Organization**: Organize items by categories (Produce, Dairy, Meat, etc.)
- **📱 Responsive Design**: Works on desktop, tablet, and mobile devices
- **💾 Local Database**: All data stored locally in SQLite - no internet required

## Quick Start

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

### Installation

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the application:**
   ```bash
   python app.py
   ```

3. **Open your browser and navigate to:**
   ```
   http://127.0.0.1:5000
   ```

That's it! The application will automatically create the database and populate it with default stores and categories.

## Usage

### Adding Items

1. Go to the **Manage Items** tab
2. Fill in the item name, select a category, and specify the unit (e.g., each, kg, L)
3. Click "Add Item"

### Recording Prices

1. Go to the **Add Price** tab
2. Select an item and store from the dropdowns
3. Enter the price and date (defaults to today)
4. Optionally add notes (e.g., "on sale", "bulk purchase")
5. Click "Add Price"

### Viewing Price History

- **Recent Prices**: View all price entries for the last 7, 14, 30, 60, or 90 days
- **Price Trends**: Select an item to see its price history with statistics (lowest, highest, average)
- **Store Comparison**: See the latest prices for all items across all stores, with best prices highlighted

### Managing Stores

1. Go to the **Manage Items** tab
2. Scroll to "Add New Store" section
3. Enter store name and location
4. Click "Add Store"

## Database Structure

The application uses SQLite with four main tables:

- **stores**: Store information (name, location)
- **categories**: Item categories
- **items**: Grocery items with category and unit
- **prices**: Price entries with item, store, price, date, and notes

## Data Export

The SQLite database file (`grocery_prices.db`) can be:
- Backed up by copying the file
- Queried using any SQLite browser/tool
- Exported to CSV or other formats using SQLite commands

## Customization

### Adding Default Stores

Edit the `init_db()` function in `app.py` to add your preferred stores:

```python
stores = [
    ('Your Store Name', 'Yellowknife, NT'),
    # Add more stores...
]
```

### Adding Default Categories

Edit the categories list in the `init_db()` function:

```python
categories = ['Produce', 'Dairy', 'Your Category', ...]
```

## Technology Stack

- **Backend**: Python Flask
- **Database**: SQLite
- **Frontend**: Vanilla JavaScript, HTML5, CSS3
- **Design**: Modern, responsive UI with CSS Grid and Flexbox

## Tips for Best Results

1. **Record prices regularly**: Try to record prices during your shopping trips
2. **Use notes**: Add notes for sales, bulk purchases, or quality differences
3. **Track common items**: Focus on items you buy frequently
4. **Compare trends**: Use the trends view to identify price patterns and optimal buying times
5. **Check store comparison**: Before shopping, check which store has the best prices for your needed items

## Troubleshooting

**Application won't start:**
- Ensure Python 3.8+ is installed: `python --version`
- Install dependencies: `pip install -r requirements.txt`

**Database errors:**
- Delete `grocery_prices.db` and restart the app to recreate the database

**Port already in use:**
- Change the port in `app.py`: `app.run(debug=True, port=5001)`

## License

This project is open source and available for personal use.

## Contributing

Feel free to fork this project and customize it for your needs!

## Author

Created for the Yellowknife community to help track and compare grocery prices.

---

**Happy Price Tracking! 🛒💰**
