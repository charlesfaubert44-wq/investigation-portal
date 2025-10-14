#!/bin/bash

echo "🧹 Creating clean repository for Yellowknife Grocery Tracker..."
echo ""

# Create temp directory
TEMP_DIR="/tmp/yellowknife-grocery-tracker"
rm -rf $TEMP_DIR
mkdir -p $TEMP_DIR

# Copy only grocery tracker files
echo "📦 Copying project files..."

# Main files
cp /workspace/app.py $TEMP_DIR/
cp /workspace/config.py $TEMP_DIR/
cp /workspace/requirements.txt $TEMP_DIR/
cp /workspace/runtime.txt $TEMP_DIR/
cp /workspace/Procfile $TEMP_DIR/
cp /workspace/.env.example $TEMP_DIR/
cp /workspace/.gitignore $TEMP_DIR/
cp /workspace/README.md $TEMP_DIR/
cp /workspace/SCRAPING_GUIDE.md $TEMP_DIR/
cp /workspace/start.sh $TEMP_DIR/
cp /workspace/start.bat $TEMP_DIR/

# Directories
cp -r /workspace/scrapers $TEMP_DIR/
cp -r /workspace/templates $TEMP_DIR/
cp -r /workspace/static $TEMP_DIR/
cp -r /workspace/deployment $TEMP_DIR/

# Initialize git
cd $TEMP_DIR
git init
git add -A
git commit -m "Initial commit: Yellowknife Grocery Price Tracker

🛒 Automatic grocery price tracking for Yellowknife stores

Features:
- 🤖 Automatic price scraping from 4 Yellowknife stores
- 📊 Multi-store price comparison with best price highlighting
- 📈 Historical price trend analysis
- 🌐 Online deployment ready (Railway, Render, Heroku)
- 🎭 Demo mode with realistic sample data
- 📱 Responsive modern UI
- 🔄 Scheduled updates every 6 hours
- 💾 SQLite (local) or PostgreSQL (production)

Stores tracked:
- Independent Grocer
- Extra Foods  
- The Co-op
- Save-On-Foods

Built with Flask, BeautifulSoup4, APScheduler, and vanilla JS.
Deploy for free and help the Yellowknife community save money! 💰"

echo ""
echo "✅ Clean repository created at: $TEMP_DIR"
echo ""
echo "📋 Files included:"
git ls-files | wc -l
echo "files"
echo ""
echo "🚀 Next steps:"
echo ""
echo "1. Create repo on GitHub: https://github.com/new"
echo "   Name: yellowknife-grocery-tracker"
echo ""
echo "2. Run these commands:"
echo ""
echo "   cd $TEMP_DIR"
echo "   git remote add origin https://github.com/YOUR_USERNAME/yellowknife-grocery-tracker.git"
echo "   git branch -M main"
echo "   git push -u origin main"
echo ""
echo "3. Deploy to Railway/Render (see DEPLOYMENT.md)"
echo ""

