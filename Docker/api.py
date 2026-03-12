from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List, Dict
from coin_scraper import scrape_ebay_coin

app = FastAPI(
    title="eBay Coin Scraper API",
    description="API for scraping and analyzing eBay sold listings for Australian coins",
    version="1.0.0"
)

# Allow CORS for all origins (adjust in production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ScrapeRequest(BaseModel):
    search_item: str
    num_pages: int = 2
    usd_to_aud_rate: float = 1.52

class CategoryStats(BaseModel):
    count: int
    lowest_price: float
    highest_price: float
    average: float
    median: float
    prices: List[float]

class ScrapeResponse(BaseModel):
    search_query: str
    detected_year: Optional[str]
    detected_denomination: Optional[str]
    total_listings_found: int
    total_items_in_stats: int
    total_items_documented_only: int
    error_coins: Optional[CategoryStats] = None
    proof_coins: Optional[CategoryStats] = None
    graded_coins: Optional[CategoryStats] = None
    mintmark_coins: Optional[CategoryStats] = None
    coin_rolls: Optional[CategoryStats] = None
    raw_coins: Optional[CategoryStats] = None
    listings: List[Dict]

@app.post("/scrape", response_model=ScrapeResponse)
async def scrape_ebay(request: ScrapeRequest):
    """
    Scrape eBay sold listings for Australian coins
    
    - **search_item**: The coin to search for (e.g., "1966 Australian 50 cent")
    - **num_pages**: Number of pages to scrape (default: 2, max: 10)
    - **usd_to_aud_rate**: USD to AUD conversion rate (default: 1.52)
    """
    if request.num_pages > 10:
        raise HTTPException(status_code=400, detail="Maximum 10 pages allowed")
    
    try:
        # Call the scraper function
        results = scrape_ebay_coin(
            search_item=request.search_item,
            num_pages=request.num_pages,
            usd_to_aud_rate=request.usd_to_aud_rate
        )
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
async def root():
    """API information"""
    return {
        "name": "eBay Coin Scraper API",
        "version": "1.0.0",
        "documentation": "/docs",
        "endpoints": {
            "POST /scrape": "Scrape eBay sold listings for coins"
        }
    }

@app.get("/health")
async def health():
    """Health check endpoint"""
    return {"status": "healthy"}
