# Deployment Guide

## Quick Deploy Options

### Option 1: Railway (Recommended - Free Tier Available)

1. **Push your code to GitHub**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin <your-repo-url>
   git push -u origin main
   ```

2. **Deploy to Railway**
   - Go to [railway.app](https://railway.app)
   - Click "New Project" → "Deploy from GitHub repo"
   - Select your repository
   - Railway will auto-detect the Python app
   - Add environment variables:
     - `SCRAPING_ENABLED=true`
     - `SCRAPING_INTERVAL_HOURS=6`
   - Deploy!

3. **Your app will be live at**: `https://your-app.railway.app`

### Option 2: Render (Free Tier Available)

1. **Push code to GitHub** (same as above)

2. **Deploy to Render**
   - Go to [render.com](https://render.com)
   - Click "New" → "Web Service"
   - Connect your GitHub repository
   - Use these settings:
     - **Build Command**: `pip install -r requirements.txt`
     - **Start Command**: `gunicorn app:app`
   - Add environment variables (see below)
   - Click "Create Web Service"

3. **Your app will be live at**: `https://your-app.onrender.com`

### Option 3: Heroku

1. **Install Heroku CLI**
   ```bash
   # macOS
   brew tap heroku/brew && brew install heroku
   
   # Windows
   # Download from https://devcenter.heroku.com/articles/heroku-cli
   ```

2. **Deploy**
   ```bash
   # Copy Procfile to root
   cp deployment/Procfile .
   
   # Login and create app
   heroku login
   heroku create yellowknife-grocery-tracker
   
   # Set environment variables
   heroku config:set SCRAPING_ENABLED=true
   heroku config:set SCRAPING_INTERVAL_HOURS=6
   heroku config:set FLASK_ENV=production
   
   # Deploy
   git push heroku main
   
   # Open your app
   heroku open
   ```

## Environment Variables

Set these variables in your deployment platform:

| Variable | Value | Description |
|----------|-------|-------------|
| `FLASK_ENV` | `production` | Flask environment |
| `SECRET_KEY` | (auto-generated) | Secret key for Flask sessions |
| `SCRAPING_ENABLED` | `true` | Enable automatic price scraping |
| `SCRAPING_INTERVAL_HOURS` | `6` | How often to scrape (in hours) |
| `DATABASE_URL` | (optional) | PostgreSQL URL for production |

## Database Options

### SQLite (Default - Good for testing)
- No configuration needed
- Data stored in `grocery_prices.db` file
- **Note**: Railway/Render ephemeral storage means data may be lost on restart
- **Best for**: Testing, development

### PostgreSQL (Recommended for Production)

1. **Add PostgreSQL to your deployment**
   - Railway: Click "New" → "Database" → "PostgreSQL"
   - Render: Click "New" → "PostgreSQL"
   - Heroku: `heroku addons:create heroku-postgresql:mini`

2. **Update your app to use PostgreSQL**
   - The `DATABASE_URL` environment variable will be automatically set
   - Install: `pip install psycopg2-binary`
   - Modify `app.py` to use PostgreSQL when `DATABASE_URL` is set

## Production Checklist

- [ ] Push code to GitHub
- [ ] Choose deployment platform (Railway/Render/Heroku)
- [ ] Create new web service
- [ ] Set environment variables
- [ ] Add database (PostgreSQL recommended)
- [ ] Deploy application
- [ ] Test scraping functionality
- [ ] Set up monitoring/alerts (optional)

## Custom Domain (Optional)

### Railway
1. Go to your project settings
2. Click "Domains"
3. Add custom domain
4. Update your DNS records

### Render
1. Go to your web service
2. Click "Settings" → "Custom Domains"
3. Add your domain
4. Update DNS records

## Monitoring

### Check scraping status
Visit: `https://your-app.com/api/scrape/status`

### Manual trigger scrape
```bash
curl -X POST https://your-app.com/api/scrape
```

### View logs
- Railway: Click on your service → "Deployments" → "View Logs"
- Render: Click on your service → "Logs"
- Heroku: `heroku logs --tail`

## Troubleshooting

### Scraping not working?
1. Check logs for errors
2. Verify `SCRAPING_ENABLED=true`
3. Check `/api/scrape/status` endpoint
4. Try manual trigger: POST to `/api/scrape`

### Data being lost?
- You're likely using SQLite on ephemeral storage
- Solution: Add PostgreSQL database (see above)

### App sleeping/slow?
- Free tiers often have cold starts
- Railway: No sleeping on free tier
- Render: 15 min inactivity = sleep
- Heroku: 30 min inactivity = sleep

## Cost Estimates

| Platform | Free Tier | Paid (Starter) |
|----------|-----------|----------------|
| Railway | $5/month credit | $5/month + usage |
| Render | Free (limited) | $7/month |
| Heroku | No free tier | $5/month |

## Security Notes

1. **Always set a strong SECRET_KEY** in production
2. **Never commit `.env` file** to git
3. **Use environment variables** for all sensitive data
4. **Enable HTTPS** (automatic on all platforms)
5. **Rate limit scraping** to avoid being blocked

## Scaling

To handle more traffic:
1. Upgrade to paid tier
2. Use PostgreSQL instead of SQLite
3. Add caching (Redis)
4. Enable CDN for static files
5. Use worker dynos for background tasks
