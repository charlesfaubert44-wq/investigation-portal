# 🛒 Yellowknife Grocery Price Tracker - ONLINE VERSION

An automated web application that tracks grocery prices across Yellowknife stores with automatic price scraping, trend analysis, and multi-store comparison. Deploy online and access from anywhere!

## 🌟 Key Features

### 🤖 **Automatic Price Scraping**
- Scheduled automatic updates every 6 hours
- Fetches prices from multiple Yellowknife stores
- Smart item matching and categorization
- Demo mode with realistic sample data (production scrapers customizable)

### 📊 **Price Intelligence**
- **Live Price Comparison**: See best prices across all stores at a glance
- **Trend Analysis**: Historical price tracking with min/max/average statistics
- **Daily Updates**: View today's price changes
- **Source Tracking**: See which prices are auto-fetched vs manually entered

### 🏪 **Multi-Store Support**
Pre-configured with major Yellowknife stores:
- Independent Grocer
- Extra Foods
- The Co-op
- Save-On-Foods

### 🌐 **Online Deployment**
- Deploy to Railway, Render, or Heroku with one click
- PostgreSQL support for production
- Scheduled background tasks
- Environment-based configuration

### 📱 **Modern Interface**
- Responsive design (works on all devices)
- Real-time status indicators
- Manual trigger for immediate updates
- Beautiful, intuitive UI

## 🚀 Quick Start

### Local Development

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Create environment file:**
   ```bash
   cp .env.example .env
   # Edit .env with your settings
   ```

3. **Run the application:**
   ```bash
   python app.py
   ```

4. **Open your browser:**
   ```
   http://127.0.0.1:5000
   ```

The app will automatically:
- Create the database
- Populate default stores and categories
- Run an initial price scrape (demo mode)
- Schedule automatic updates every 6 hours

## 🌍 Deploy Online (Free!)

### Option 1: Railway (Recommended)

[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/new)

1. Push code to GitHub
2. Connect Railway to your repo
3. Set environment variables (see below)
4. Deploy! Your app will be live in minutes

[Detailed deployment guide →](deployment/DEPLOYMENT.md)

### Option 2: Render

1. Fork this repository
2. Create new Web Service on [Render](https://render.com)
3. Connect your repo
4. Deploy automatically

### Option 3: Heroku

```bash
cp deployment/Procfile .
heroku create yellowknife-grocery-tracker
heroku config:set SCRAPING_ENABLED=true
git push heroku main
```

## ⚙️ Configuration

### Environment Variables

Create a `.env` file or set these in your deployment platform:

```bash
# Flask
FLASK_ENV=production
SECRET_KEY=your-secret-key-change-this

# Scraping
SCRAPING_ENABLED=true
SCRAPING_INTERVAL_HOURS=6

# Database (optional - defaults to SQLite)
DATABASE_URL=postgresql://...

# Server
PORT=5000
HOST=0.0.0.0
```

### Scraping Modes

#### Demo Mode (Default)
- Generates realistic sample data
- No actual web scraping
- Perfect for testing and development
- Set in `app.py`: `ScraperManager(use_demo=True)`

#### Production Mode
- Real web scraping from store websites
- Requires implementation of store-specific scrapers
- Set in `app.py`: `ScraperManager(use_demo=False)`

## 🛠️ Implementing Real Scrapers

The app includes a framework for web scraping, but store-specific scrapers need customization:

### 1. Analyze Store Website

```bash
# Visit the store website and inspect the HTML
# Identify product listings and price elements
```

### 2. Edit Scraper File

Edit `scrapers/independent_scraper.py` (or create new scraper):

```python
def scrape_products(self, category=None):
    url = f"{self.base_url}/shop/products"
    html = self.fetch_page(url)
    soup = self.parse_html(html)
    
    products = []
    for element in soup.select('.product-item'):
        name = element.select_one('.product-name').text
        price = self.clean_price(element.select_one('.price').text)
        
        products.append({
            'name': self.clean_product_name(name),
            'price': price,
            'unit': 'each',
            'category': category or 'General'
        })
    
    return products
```

### 3. Update Configuration

```python
# In app.py
scraper_manager = ScraperManager(DATABASE, use_demo=False)
```

### 4. Legal Considerations

⚠️ **IMPORTANT**: Before scraping any website:

- ✅ Check the website's `robots.txt` file
- ✅ Review Terms of Service
- ✅ Respect rate limits (use delays between requests)
- ✅ Consider using official APIs if available
- ✅ Add appropriate `User-Agent` headers
- ❌ Don't overload servers with requests
- ❌ Don't scrape copyrighted content without permission

## 📖 API Endpoints

### Price Data
- `GET /api/prices?days=30` - Get recent prices
- `POST /api/prices` - Add manual price entry
- `GET /api/price-trends/{item_id}` - Get price history for item
- `GET /api/price-comparison` - Compare latest prices across stores

### Scraping
- `GET /api/scrape/status` - Get scraping status and last update time
- `POST /api/scrape` - Manually trigger price update (all stores)
- `POST /api/scrape/store/{store_name}` - Update specific store

### Data Management
- `GET /api/stores` - List all stores
- `GET /api/categories` - List categories
- `GET /api/items` - List all items

## 📊 Database Schema

```sql
stores          # Grocery stores
├── id, name, location, website_url, scraping_enabled

categories      # Product categories
├── id, name

items           # Grocery items
├── id, name, category_id, unit

prices          # Price history
├── id, item_id, store_id, price, date, notes, source
```

## 🎯 Usage Examples

### Manual Price Entry
1. Go to "Add Price Manually" tab
2. Select item and store
3. Enter price and date
4. Click "Add Price"

### Trigger Auto-Update
1. Go to "Auto-Scraping" tab
2. Click "Update Prices Now"
3. Wait for scraping to complete
4. View updated prices in "Price Comparison"

### View Price Trends
1. Go to "Price Trends" tab
2. Select an item from dropdown
3. View historical prices with statistics

### Compare Stores
1. Go to "Price Comparison" tab
2. See latest prices for all items
3. Green borders indicate best prices

## 🔧 Advanced Features

### Custom Scraping Schedule

Edit `config.py`:
```python
SCRAPING_INTERVAL_HOURS = 3  # Update every 3 hours
```

### Add New Store

1. Add to database via UI or:
```sql
INSERT INTO stores (name, location, website_url, scraping_enabled) 
VALUES ('New Store', 'Yellowknife, NT', 'https://...', 1);
```

2. Create scraper in `scrapers/new_store_scraper.py`

3. Register in `ScraperManager.__init__()`

### Export Data

```bash
# SQLite to CSV
sqlite3 grocery_prices.db
.mode csv
.output prices.csv
SELECT * FROM prices;
.quit
```

## 📈 Production Recommendations

### Database
- ✅ Use PostgreSQL instead of SQLite
- ✅ Regular backups
- ✅ Index frequently queried columns

### Monitoring
- ✅ Set up error logging
- ✅ Monitor scraping success rate
- ✅ Track API response times
- ✅ Use /api/scrape/status endpoint

### Performance
- ✅ Enable caching (Redis recommended)
- ✅ Use CDN for static files
- ✅ Compress responses (gzip)
- ✅ Rate limit API endpoints

### Security
- ✅ Use strong SECRET_KEY
- ✅ Enable HTTPS (automatic on deployment platforms)
- ✅ Validate all user inputs
- ✅ Use environment variables for secrets

## 🐛 Troubleshooting

### Scraping Not Working?
```python
# Check logs
heroku logs --tail  # or check platform logs

# Verify status
curl https://your-app.com/api/scrape/status

# Manual trigger
curl -X POST https://your-app.com/api/scrape
```

### No Prices Showing?
- Check if demo mode is enabled
- Trigger manual scrape
- Check database has items and stores
- View browser console for errors

### Deployment Issues?
- Verify all environment variables are set
- Check build logs for dependency errors
- Ensure `gunicorn` is in requirements.txt
- Verify `Procfile` is in root directory

## 📝 File Structure

```
yellowknife-grocery-tracker/
├── app.py                      # Main Flask application
├── config.py                   # Configuration management
├── requirements.txt            # Python dependencies
├── .env.example               # Environment variables template
├── runtime.txt                # Python version for deployment
│
├── scrapers/                  # Web scraping framework
│   ├── __init__.py
│   ├── base_scraper.py       # Base scraper class
│   ├── scraper_manager.py    # Scraper coordination
│   ├── demo_scraper.py       # Demo data generator
│   └── independent_scraper.py # Store-specific scraper
│
├── templates/                 # HTML templates
│   └── index.html
│
├── static/                    # CSS and JavaScript
│   ├── css/style.css
│   └── js/app.js
│
└── deployment/                # Deployment configs
    ├── Procfile
    ├── railway.json
    ├── render.yaml
    └── DEPLOYMENT.md
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Implement your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is open source and available for personal use.

## 🙏 Credits

Created for the Yellowknife community to help track and compare grocery prices in Canada's North.

## 📞 Support

- **Issues**: Open a GitHub issue
- **Questions**: Check existing issues or create new one
- **Deployment Help**: See [DEPLOYMENT.md](deployment/DEPLOYMENT.md)

---

**Built with ❤️ for Yellowknife** 

🌟 **Star this repo if you find it useful!**
