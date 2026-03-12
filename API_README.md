# eBay Coin Scraper API

A FastAPI-based REST API for scraping and analyzing eBay sold listings for Australian coins.

## Features

- 🔍 Scrapes eBay sold listings for Australian coins
- 📊 Categorizes coins into: Error Coins, Proof Coins, Graded Coins, Mintmark Coins, Rolls, and Raw Coins
- 💰 Provides statistical analysis (average, median, price range)
- 🌐 RESTful API with automatic documentation
- ✅ Type validation and error handling

## Installation

### Option 1: Docker (Recommended)

1. Make sure Docker and Docker Compose are installed on your system
2. Navigate to the API directory:
```bash
cd API
```

3. Build and run with Docker Compose:
```bash
docker-compose up --build
```

The API will be available at `http://localhost:8000`

To run in detached mode (background):
```bash
docker-compose up -d
```

To stop the API:
```bash
docker-compose down
```

### Option 2: Local Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Start the server:
```bash
uvicorn api:app --reload
```

The API will be available at `http://localhost:8000`

## API Documentation

Once running, visit:
- **Interactive API docs**: http://localhost:8000/docs
- **Alternative docs**: http://localhost:8000/redoc

## Endpoints

### POST /scrape

Scrape eBay sold listings for a specific coin.

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
  "error_coins": null,
  "proof_coins": {
    "count": 5,
    "lowest_price": 15.20,
    "highest_price": 75.50,
    "average": 42.30,
    "median": 38.00,
    "prices": [15.20, 30.40, 38.00, 52.10, 75.50]
  },
  "graded_coins": {...},
  "mintmark_coins": {...},
  "coin_rolls": null,
  "raw_coins": {...},
  "listings": [
    {
      "title": "1966 Australian 50 Cent Silver Proof",
      "price_usd": "$25.00",
      "price_aud": 38.00,
      "date": "Sold Jan 15, 2026",
      "link": "https://ebay.com/itm/...",
      "category": "proof",
      "included_in_stats": true
    },
    ...
  ]
}
```

### GET /

Get API information

### GET /health

Health check endpoint

## Example Usage

### Python

```python
import requests

response = requests.post(
    "http://localhost:8000/scrape",
    json={
        "search_item": "1988 2 dollar aboriginal",
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
    "search_item": "1966 Australian 50 cent",
    "num_pages": 2
  }'
```

### JavaScript/Fetch

```javascript
const response = await fetch('http://localhost:8000/scrape', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    search_item: '1966 Australian 50 cent',
    num_pages: 2
  })
});

const data = await response.json();
console.log(`Found ${data.total_listings_found} listings`);
```

## Categories Explained

- **Error Coins**: Mules, double strikes, die errors, missing SD, etc.
- **Proof Coins**: Silver proof, gold proof, RAM proof sets
- **Graded Coins**: PCGS, NGC, ANACS certified coins
- **Mintmark Coins**: C, S, M, B, A mintmarks
- **Coin Rolls**: Full rolls, half rolls (with denomination-specific price filters)
- **Raw Coins**: Standard circulation coins

## Notes

- The scraper filters out lots, bulk purchases, and sets
- Non-USD currency listings are excluded
- Year-specific searches automatically filter listings
- Listings saying "no errors", "no mintmark", etc. are excluded
- Roll prices have denomination-specific minimums to filter out single coins

## Production Deployment

For production:
1. Remove `--reload` flag from uvicorn command
2. Configure CORS to allow only specific origins
3. Add authentication if needed
4. Use a production ASGI server like Gunicorn with Uvicorn workers
5. Set up proper error logging and monitoring

Example production command:
```bash
gunicorn api:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```
