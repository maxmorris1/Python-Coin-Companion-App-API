# 🪙 Australian Coin Companion API

A powerful REST API for scraping and analyzing eBay sold listings for Australian coins. Get real-time market data, price statistics, and categorized listings through simple HTTP requests.

## 🌟 Features

- 🔍 **Smart Scraping**: Automatically scrapes eBay sold listings with configurable page limits
- 📊 **Intelligent Categorization**: Classifies coins into 6 categories:
  - Error Coins (mules, double strikes, die errors, etc.)
  - Proof Coins (silver proof, gold proof, RAM sets)
  - Graded Coins (PCGS, NGC, ANACS certified)
  - Mintmark Coins (C, S, M, B, A privy marks)
  - Coin Rolls (full rolls, half rolls with smart filtering)
  - Raw Coins (standard circulation coins)
- 💰 **Price Analytics**: Automatic calculation of average, median, range, and price distribution
- ✅ **Smart Filtering**: Excludes lots, sets, non-USD currencies, and irrelevant listings
- 🌐 **RESTful API**: Clean JSON responses with comprehensive data
- 🚀 **Fast & Reliable**: Built with FastAPI and undetected-chromedriver

## 📋 Prerequisites

- Python 3.8+
- Chrome/Chromium browser (for Selenium)
- Windows/Linux/macOS

## 🚀 Quick Start

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/maxmorris1/Python-Coin-Companion-App-API.git
cd Python-Coin-Companion-App-API
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

### Running the API

#### Option 1: Using the Control Script (Windows - Easiest)
```powershell
.\api_control.ps1
```
This will:
- Check if the API is running
- Allow you to start/stop it with one command
- Show the API URL and documentation link

#### Option 2: Manual Start
```bash
uvicorn api:app --reload
```

The API will be available at `http://localhost:8000`

## 📖 API Documentation

Once running, visit:
- **Interactive Swagger UI**: http://localhost:8000/docs
- **ReDoc Documentation**: http://localhost:8000/redoc

## 🔌 API Endpoints

### Health Check
```http
GET /health
```

**Response:**
```json
{
  "status": "healthy"
}
```

### Scrape Coin Listings
```http
POST /scrape
Content-Type: application/json
```

**Request Body:**
```json
{
  "search_item": "1966 Australian 50 cent",
  "num_pages": 2,
  "usd_to_aud_rate": 1.52
}
```

**Parameters:**
- `search_item` (required): The coin to search for
- `num_pages` (optional): Number of pages to scrape (1-10, default: 2)
- `usd_to_aud_rate` (optional): USD to AUD conversion rate (default: 1.52)

**Response:**
```json
{
  "search_query": "1966 Australian 50 cent",
  "detected_year": "1966",
  "detected_denomination": "fifty cents",
  "total_listings_found": 45,
  "total_items_in_stats": 42,
  "total_items_documented_only": 3,
  "proof_coins": {
    "count": 5,
    "lowest_price": 15.20,
    "highest_price": 75.50,
    "average": 42.30,
    "median": 38.00,
    "prices": [15.20, 30.40, 38.00, 52.10, 75.50]
  },
  "raw_coins": {
    "count": 25,
    "lowest_price": 3.04,
    "highest_price": 22.80,
    "average": 9.12,
    "median": 7.60,
    "prices": [...]
  },
  "listings": [
    {
      "title": "1966 Australian 50 Cent Silver Proof",
      "price_usd": "$25.00",
      "price_aud": 38.00,
      "date": "Sold Jan 15, 2026",
      "link": "https://ebay.com/itm/...",
      "category": "proof",
      "included_in_stats": true
    }
  ]
}
```

## 💻 Usage Examples

### Python
```python
import requests

response = requests.post(
    "http://localhost:8000/scrape",
    json={
        "search_item": "2012 red poppy 2 dollar",
        "num_pages": 3,
        "usd_to_aud_rate": 1.52
    }
)

data = response.json()
print(f"Found {data['total_listings_found']} listings")

if data['raw_coins']:
    print(f"Raw coins average: AU${data['raw_coins']['average']}")
```

### cURL
```bash
curl -X POST "http://localhost:8000/scrape" \
  -H "Content-Type: application/json" \
  -d '{
    "search_item": "1988 2 dollar aboriginal",
    "num_pages": 2
  }'
```

### JavaScript/Fetch
```javascript
const response = await fetch('http://localhost:8000/scrape', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    search_item: '1972 5 cent no sd',
    num_pages: 2
  })
});

const data = await response.json();
console.log(`Average price: AU$${data.raw_coins?.average}`);
```

## 🧪 Testing

Run the included test script:
```bash
python test_api.py
```

This will:
- Test the health endpoint
- Scrape a sample coin (1966 50 cent)
- Display formatted results
- Save full output to `api_results.json`

## 📁 Project Structure

```
├── api.py                          # FastAPI server
├── api_control.ps1                 # Windows control script
├── test_api.py                     # Example client & tests
├── requirements.txt                # Python dependencies
├── ebay scraper.py                 # Original CLI scraper
├── australian_coins_catalog.py     # Coin catalog utilities
├── Australian_Coins_Regular.txt    # Regular coins list
├── Australian_Coins_Graded.txt     # Graded coins list (MS60-MS70)
├── Australian_Coins_Catalog/       # Detailed coin information
└── README.md                       # This file
```

## 🎯 Coin Categories Explained

- **Error Coins**: Mules, double strikes, die errors, missing SD, off-center, clipped planchets, etc.
- **Proof Coins**: Silver proof, gold proof, RAM proof sets (excludes "no proof" listings)
- **Graded Coins**: PCGS, NGC, ANACS certified coins with grades
- **Mintmark Coins**: C, S, M, B, A mintmarks and privy marks
- **Coin Rolls**: Full rolls, half rolls (with denomination-specific minimum prices)
- **Raw Coins**: Standard circulation coins without special features

## ⚙️ Advanced Configuration

### Change Default Port
```bash
uvicorn api:app --reload --port 8080
```

### Production Deployment
```bash
# Install gunicorn
pip install gunicorn

# Run with multiple workers
gunicorn api:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

### CORS Configuration
Modify `api.py` to restrict allowed origins:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://yourdomain.com"],  # Change from ["*"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## 🔧 Troubleshooting

### Chrome Driver Issues
If you get Chrome driver errors:
```bash
pip install --upgrade undetected-chromedriver
```

### Port Already in Use
```powershell
# Windows - Find and kill process on port 8000
Get-Process -Id (Get-NetTCPConnection -LocalPort 8000).OwningProcess | Stop-Process
```

### Import Errors
Make sure all dependencies are installed:
```bash
pip install -r requirements.txt --upgrade
```

## 📊 Coin Lists Included

- **Australian_Coins_Regular.txt**: 577 regular Australian coins (1966-2026)
- **Australian_Coins_Graded.txt**: 6,347 MS-graded variations (MS60-MS70)
- **Australian_Coins_Catalog/**: Detailed information on denominations, special releases, proof sets, and valuable coins

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📝 License

This project is open source and available under the MIT License.

## 🙏 Acknowledgments

- Built with [FastAPI](https://fastapi.tiangolo.com/)
- Scraping powered by [Selenium](https://www.selenium.dev/) and [undetected-chromedriver](https://github.com/ultrafunkamsterdam/undetected-chromedriver)
- HTML parsing with [BeautifulSoup4](https://www.crummy.com/software/BeautifulSoup/)

## 📧 Support

For issues, questions, or suggestions, please open an issue on GitHub.

---

**Made with ☕ for Australian coin collectors and numismatists**
