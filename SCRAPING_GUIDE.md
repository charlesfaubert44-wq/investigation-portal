# Web Scraping Implementation Guide

## Overview

This guide explains how to implement real web scrapers for Yellowknife grocery stores. The app currently runs in **demo mode** with sample data. To fetch real prices, you'll need to implement store-specific scrapers.

## ⚠️ Legal & Ethical Considerations

### BEFORE YOU START

1. **Check robots.txt**: Visit `https://store-website.com/robots.txt`
   - Respect all `Disallow` directives
   - Follow `Crawl-delay` if specified

2. **Review Terms of Service**: Read the store's ToS
   - Many sites prohibit automated access
   - Violation could result in legal action or IP bans

3. **Look for APIs**: Check if the store provides an official API
   - Many chains have partner/developer programs
   - APIs are legal, supported, and more reliable

4. **Respect Rate Limits**:
   - Add delays between requests (2-5 seconds minimum)
   - Don't overload servers
   - Use off-peak hours for large scrapes

5. **Data Usage**:
   - Only scrape publicly available data
   - Don't scrape copyrighted content (images, descriptions)
   - Use data for personal/research purposes only

### Recommendation

**Best Practice**: Contact stores directly and ask if they:
- Have an official API
- Allow automated price checking
- Can provide price feeds for community projects

## Technical Implementation

### Architecture

```
ScraperManager
├── Coordinates all scrapers
├── Manages database storage
└── Handles scheduling

BaseScraper (Abstract)
├── HTTP request handling
├── HTML parsing utilities
├── Error handling & retries
└── Rate limiting

Store-Specific Scrapers (Implement these)
├── IndependentScraper
├── ExtraFoodsScraper
├── CoopScraper
└── SaveOnFoodsScraper
```

### Step 1: Analyze Store Website

#### Method 1: Browser Developer Tools

1. Open store website in Chrome/Firefox
2. Press F12 to open DevTools
3. Go to Network tab
4. Navigate to product listings
5. Look for API calls (XHR/Fetch requests)

**If you find API calls**:
```javascript
// Example: Store might load products via API
GET https://store.com/api/products?category=dairy
Response: JSON with product data
```

This is IDEAL - you can directly call their API!

#### Method 2: HTML Inspection

1. Right-click on a product → "Inspect Element"
2. Identify HTML structure for:
   - Product container (usually `<div class="product">`)
   - Product name (`<h3 class="product-name">`)
   - Price (`<span class="price">`)
   - Unit/size (`<span class="unit">`)

Example HTML structure:
```html
<div class="product-card" data-product-id="123">
    <h3 class="product-name">Milk 2L</h3>
    <div class="price-container">
        <span class="price">$4.99</span>
        <span class="unit">2L</span>
    </div>
    <span class="category">Dairy</span>
</div>
```

### Step 2: Implement Scraper

Edit `scrapers/independent_scraper.py`:

```python
from .base_scraper import BaseScraper
import logging

logger = logging.getLogger(__name__)

class IndependentScraper(BaseScraper):
    
    def __init__(self, user_agent=None):
        super().__init__(
            store_name='Independent Grocer',
            base_url='https://www.realcanadiansuperstore.ca',  # Update
            user_agent=user_agent
        )
        
    def scrape_products(self, category=None):
        """Scrape products from Independent Grocer"""
        
        # OPTION A: Using their API (if available)
        # url = f"{self.base_url}/api/products?limit=100&category={category}"
        # response = self.fetch_page(url)
        # data = json.loads(response)
        # return self._parse_api_response(data)
        
        # OPTION B: Scraping HTML
        url = f"{self.base_url}/shop/grocery/dairy"  # Update with real URL
        html = self.fetch_page(url)
        soup = self.parse_html(html)
        
        products = []
        
        # Update selectors based on actual HTML structure
        product_elements = soup.select('.product-card')  
        
        for element in product_elements:
            try:
                # Extract data - UPDATE THESE SELECTORS
                name_elem = element.select_one('.product-name')
                price_elem = element.select_one('.price')
                unit_elem = element.select_one('.unit')
                
                if not name_elem or not price_elem:
                    continue
                
                name = self.clean_product_name(name_elem.text)
                price = self.clean_price(price_elem.text)
                unit = unit_elem.text.strip() if unit_elem else 'each'
                
                # Determine category from element or use provided
                category_elem = element.select_one('.category')
                item_category = category_elem.text if category_elem else (category or 'General')
                
                products.append({
                    'name': name,
                    'price': price,
                    'unit': unit,
                    'category': item_category,
                    'on_sale': 'sale' in element.get('class', [])
                })
                
            except Exception as e:
                logger.error(f"Error parsing product: {e}")
                continue
        
        logger.info(f"Scraped {len(products)} products")
        return products
    
    def get_available_categories(self):
        """Scrape or return hardcoded categories"""
        # Option 1: Hardcode known categories
        return ['Produce', 'Dairy', 'Meat', 'Bakery', 'Pantry']
        
        # Option 2: Scrape from website
        # url = f"{self.base_url}/shop"
        # html = self.fetch_page(url)
        # soup = self.parse_html(html)
        # return [cat.text for cat in soup.select('.category-link')]
```

### Step 3: Handle Pagination

Many stores spread products across multiple pages:

```python
def scrape_products(self, category=None):
    all_products = []
    page = 1
    max_pages = 10  # Safety limit
    
    while page <= max_pages:
        url = f"{self.base_url}/shop?page={page}&category={category}"
        html = self.fetch_page(url)
        soup = self.parse_html(html)
        
        products = self._parse_page(soup)
        
        if not products:  # No more products
            break
            
        all_products.extend(products)
        
        # Check for next page
        next_button = soup.select_one('.pagination-next')
        if not next_button or 'disabled' in next_button.get('class', []):
            break
        
        page += 1
        time.sleep(2)  # Rate limiting!
    
    return all_products
```

### Step 4: Handle JavaScript-Rendered Sites

Some modern stores use React/Vue and render content with JavaScript. BeautifulSoup can't handle this.

**Solution: Use Selenium**

```python
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class IndependentScraper(BaseScraper):
    
    def __init__(self, user_agent=None):
        super().__init__(...)
        
        # Setup Selenium
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')  # Run without GUI
        options.add_argument(f'user-agent={self.user_agent}')
        self.driver = webdriver.Chrome(options=options)
    
    def scrape_products(self, category=None):
        url = f"{self.base_url}/shop/dairy"
        self.driver.get(url)
        
        # Wait for products to load
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "product-card"))
        )
        
        # Scroll to load lazy-loaded content
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        
        # Now parse the rendered HTML
        html = self.driver.page_source
        soup = BeautifulSoup(html, 'lxml')
        
        # ... continue parsing as before
```

### Step 5: Error Handling

```python
def scrape_products(self, category=None):
    try:
        products = []
        
        # Your scraping logic here
        
        if not products:
            logger.warning(f"No products found for category: {category}")
        
        return products
        
    except requests.RequestException as e:
        logger.error(f"Network error: {e}")
        return []
        
    except Exception as e:
        logger.error(f"Unexpected error in scraper: {e}")
        return []
```

### Step 6: Testing

Create `test_scraper.py`:

```python
from scrapers.independent_scraper import IndependentScraper

def test_scraper():
    scraper = IndependentScraper()
    
    # Test category listing
    categories = scraper.get_available_categories()
    print(f"Found {len(categories)} categories")
    
    # Test product scraping
    products = scraper.scrape_products('Dairy')
    print(f"Found {len(products)} products")
    
    # Print sample products
    for product in products[:5]:
        print(f"  - {product['name']}: ${product['price']} ({product['unit']})")

if __name__ == '__main__':
    test_scraper()
```

Run test:
```bash
python test_scraper.py
```

### Step 7: Enable in Production

Once scrapers are working:

```python
# In app.py
scraper_manager = ScraperManager(DATABASE, use_demo=False)  # Disable demo mode
```

## Advanced Topics

### Handling Sessions & Cookies

Some stores require cookies or sessions:

```python
def __init__(self, user_agent=None):
    super().__init__(...)
    
    # Initialize session
    self.session.get(self.base_url)  # Get cookies
    
    # Add auth if needed
    # self.session.post(f"{self.base_url}/login", data={...})
```

### Handling CAPTCHAs

If you encounter CAPTCHAs:
1. **Don't try to bypass** - it's against ToS
2. **Slow down** - you're scraping too fast
3. **Use official API** - the right solution
4. **Contact store** - explain your use case

### Proxy Rotation

For production at scale (after getting permission):

```python
proxies = {
    'http': 'http://proxy1.com:8080',
    'https': 'https://proxy1.com:8080',
}

response = self.session.get(url, proxies=proxies)
```

### Data Quality

```python
def clean_price(self, price_text):
    """Enhanced price cleaning"""
    if not price_text:
        return None
    
    # Handle various formats
    # "$4.99 ea" → 4.99
    # "2 for $5" → 2.50
    # "$3.99/lb" → 3.99
    
    cleaned = price_text.replace('$', '').strip()
    
    # Handle "X for $Y" format
    if 'for' in cleaned.lower():
        parts = cleaned.split('for')
        quantity = float(parts[0].strip())
        price = float(parts[1].replace('$', '').strip())
        return round(price / quantity, 2)
    
    # Extract first number
    import re
    match = re.search(r'\d+\.?\d*', cleaned)
    if match:
        return float(match.group())
    
    return None
```

## Store-Specific Notes

### Independent Grocer / Loblaws Stores
- Likely shares infrastructure with Real Canadian Superstore
- May have Loblaw Digital API
- Check for PC Express API

### Extra Foods
- Part of Loblaw Companies
- Similar structure to above

### The Co-op
- Independent co-operative
- May have different system per region
- Check local Yellowknife Co-op website

### Save-On-Foods
- Owned by Pattison Food Group
- May have regional variations

## Troubleshooting

### "403 Forbidden" Error
- Store is blocking your requests
- Add better User-Agent header
- Slow down request rate
- Check if IP is banned

### Empty Results
- Selectors are wrong (HTML changed)
- Content is JavaScript-rendered (use Selenium)
- Check if URL is correct

### Inconsistent Data
- Add more validation
- Handle edge cases in price parsing
- Log failures for review

## Getting Help

1. **Check existing issues** on GitHub
2. **Review store's robots.txt**
3. **Test with simple curl first**:
   ```bash
   curl -A "Mozilla/5.0" https://store.com/shop
   ```
4. **Use browser DevTools** to inspect network calls

## Remember

- ✅ Always respect ToS
- ✅ Add delays between requests
- ✅ Handle errors gracefully
- ✅ Log everything
- ✅ Test thoroughly
- ✅ Monitor for changes
- ❌ Don't scrape personal data
- ❌ Don't overwhelm servers
- ❌ Don't bypass security measures

---

**Good luck, and happy (ethical) scraping! 🕷️**
