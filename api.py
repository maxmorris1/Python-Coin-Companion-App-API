from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List, Dict
from bs4 import BeautifulSoup
import time
import random
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import statistics
import re

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

# ============================================================================
# CONSTANTS AND HELPER FUNCTIONS (from original scraper)
# ============================================================================

ONE_DOLLAR = ['$1', '1 dollar', 'one dollar', '1dollar', 'kangaroo', 'kangaroos', 'mob of roos']
TWO_DOLLAR = ['$2', '2 dollar', 'two dollar', '2dollar', 'aboriginal elder', 'southern cross']
FIFTY_CENTS = ['50c', '50 cent', 'fifty cent', 'half dollar', 'coat of arms']
TWENTY_CENTS = ['20c', '20 cent', 'twenty cent', 'platypus']
TEN_CENTS = ['10c', '10 cent', 'ten cent', 'dime', 'lyrebird']
FIVE_CENTS = ['5c', '5 cent', 'five cent', 'nickel', 'echidna', 'spiny anteater']
TWO_CENT = ['2c', '2 cent', 'two cent', 'frilled neck lizard', 'frill neck']
ONE_CENT = ['1c', '1 cent', 'one cent', 'penny', 'feather-tailed glider', 'feather tailed glider']

PROOF_KEYWORDS = [
    'silver', 'proof', 'gold', 'investment coin',
    'ram proof', 'royal australian mint proof', 
    'fine silver', '.999 silver', '.999', 
    'proof set', 'silver proof', 'gold proof',
    'piedfort', 'specimen'
]

C_MINTMARK_KEYWORDS = [
    'c mint mark', 'c mintmark', 'c privy', 'canberra mintmark', 
    's mint mark', 's mintmark', 'sydney mintmark',
    'm mint mark', 'm mintmark', 'melbourne mintmark',
    'b mint mark', 'b mintmark', 'brisbane mintmark',
    'a mint mark', 'a mintmark', 'adelaide mintmark',
    'mint mark', 'privy mark', 'mintmark', 'privy'
]

ERROR_KEYWORDS = [
    'mule', 'mule error', '$1 $10 mule', 'dollar ten cent mule',
    'no sd', 'missing sd', 'sd error', '1972 no sd',
    'double strike', 'double struck', 'struck twice',
    'double header', 'double obverse', 'two heads', 'double tail',
    'off center', 'off-center', 'misaligned', 'shifted strike',
    'clipped planchet', 'clip', 'straight clip', 'curved clip',
    'wrong planchet', 'wrong stock',
    'broadstrike', 'broad strike', 'no collar',
    'die crack', 'cud', 'die break', 'die error',
    'rotated die', 'medal alignment',
    'struck through', 'filled die', 'grease strike',
    'weak strike', 'insufficient strike',
    'brockage', 'mirror strike',
    'missing clad', 'delamination', 'lamination',
    'peeling', 'clad error',
    'frosted', 'frosted anzac', 'incuse flag',
    'variety', 'error variety',
    'mintmark error', 'missing mintmark',
    'error', 'mint error', 'minting error',
    'rare error', 'major error'
]

GRADED_KEYWORDS = ['pcgs', 'ngc', 'anacs', 'icg', 'graded', 'ms65', 'ms66', 'ms67', 'ms68', 'ms69', 'ms70', 'pf', 'pr', 'proof', 'ms']

ROLL_KEYWORDS = ['roll', 'rolls', '50 coins', 'bank roll', 'full roll', 'half roll', 'quarter roll', 'cotton & co', 'bag', 'cotton and co', 'security roll']
ROLL_SKIP_KEYWORDS = ['ex', 'ex mint', 'card']

SKIP_KEYWORDS = [
    'lot', 'bulk', 'collection', 'set of', 'mixed', 'assorted', 
    'proof set', 'mint set', 'uncirculated set',
    '2 x', '3 x', '4 x', '5 x', '6 x', '7 x', '8 x', '9 x', '10 x',
    '2x', '3x', '4x', '5x', '6x', '7x', '8x', '9x', '10x',
    'x 2', 'x 3', 'x 4', 'x 5', 'x 6', 'x 7', 'x 8', 'x 9', 'x 10',
    ' x2', ' x3', ' x4', ' x5', ' x6', ' x7', ' x8', ' x9', ' x10',
    'pair of', 'trio', 'quad', 'multiple coins', 'two coins', 'three coins',
    'four coins', 'five coins', 'six coins',
    'euro', '€', 'eur', 'gbp', '£', 'pound sterling', 'pounds',
    'cad', 'canadian dollar', 'aud', 'australian dollar',
    'nzd', 'new zealand dollar', 'jpy', '¥', 'yen',
    'cny', 'rmb', 'yuan', 'inr', 'rupee', 'rupees',
    'mxn', 'peso', 'pesos', 'chf', 'swiss franc',
    'sek', 'krona', 'dkk', 'krone', 'nok',
    'sgd', 'singapore dollar', 'hkd', 'hong kong dollar',
    'krw', 'won', 'php', 'thb', 'baht', 'zar', 'rand'
]

def denomination_checker(search_term: str) -> Optional[str]:
    """Detect coin denomination from search term"""
    search_lower = search_term.lower()
    
    if any(denomination in search_lower for denomination in ONE_DOLLAR):
        return 'one dollar'
    if any(denomination in search_lower for denomination in TWO_DOLLAR):
        return 'two dollar'
    if any(denomination in search_lower for denomination in FIFTY_CENTS):
        return 'fifty cents'
    if any(denomination in search_lower for denomination in TWENTY_CENTS):
        return 'twenty cents'
    if any(denomination in search_lower for denomination in TEN_CENTS):
        return 'ten cents'
    if any(denomination in search_lower for denomination in FIVE_CENTS):
        return 'five cents'
    if any(denomination in search_lower for denomination in TWO_CENT):
        return 'two cents'
    if any(denomination in search_lower for denomination in ONE_CENT):
        return 'one cent'
    
    return None

def extract_year(search_term: str) -> Optional[str]:
    """Extract year from search term"""
    year_match = re.search(r'\b(19\d{2}|20\d{2})\b', search_term)
    if year_match:
        return year_match.group(1)
    return None

def matches_specific_coin(title: str, search_term: str, search_year: Optional[str]) -> bool:
    """Check if listing matches the specific coin being searched for"""
    title_lower = title.lower()
    search_lower = search_term.lower()
    
    if search_year:
        title_years = re.findall(r'\b(19\d{2}|20\d{2})\b', title)
        if title_years and search_year not in title_years:
            return False
    
    error_phrases = ['no sd', 'missing sd', 'double strike', 'double header', 
                     'off center', 'off-center', 'no collar', 'die crack']
    
    for phrase in error_phrases:
        if phrase in search_lower:
            if phrase in title_lower:
                return True
    
    common_words = {'the', 'and', 'or', 'a', 'an', 'coin', 'australian', 'australia', 'cent', 'dollar'}
    search_keywords = set(search_lower.split()) - common_words - {search_year.lower() if search_year else ''}
    
    if search_keywords:
        matches = sum(1 for keyword in search_keywords if keyword in title_lower)
        if matches < len(search_keywords) * 0.6:
            return False
    
    return True

def has_keyword_without_no(title_lower: str, keywords: List[str]) -> bool:
    """Check if keyword appears without being negated by 'no'"""
    no_exceptions = [
        'no sd', 'no collar', 'missing sd', 'sd error',
        '1972 no sd', 'no clad'
    ]
    
    for exception in no_exceptions:
        if exception in title_lower:
            return True
    
    for keyword in keywords:
        if keyword in title_lower:
            no_pattern = f"no {keyword}"
            if no_pattern not in title_lower:
                return True
    return False

def categorize_listing(title: str) -> tuple:
    """Categorize listing and determine if it should be included"""
    title_lower = title.lower()
    
    if any(keyword in title_lower for keyword in SKIP_KEYWORDS):
        return 'skip', False
    
    if has_keyword_without_no(title_lower, ERROR_KEYWORDS):
        return 'error', True
    
    if has_keyword_without_no(title_lower, PROOF_KEYWORDS):
        return 'proof', True
    
    if has_keyword_without_no(title_lower, GRADED_KEYWORDS):
        return 'graded', True
    
    if has_keyword_without_no(title_lower, C_MINTMARK_KEYWORDS):
        return 'mint mark', True
    
    if has_keyword_without_no(title_lower, ROLL_KEYWORDS):
        if not any(skip in title_lower for skip in ROLL_SKIP_KEYWORDS):
            return 'roll', True
    
    return 'raw', True

def calculate_stats(prices: List[float]) -> Optional[CategoryStats]:
    """Calculate statistics for a price category"""
    if not prices:
        return None
    
    unique_prices = sorted(list(set(prices)))
    
    return CategoryStats(
        count=len(unique_prices),
        lowest_price=round(min(unique_prices), 2),
        highest_price=round(max(unique_prices), 2),
        average=round(sum(unique_prices) / len(unique_prices), 2),
        median=round(statistics.median(unique_prices), 2),
        prices=unique_prices
    )

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
    
    search_term = request.search_item
    search_year = extract_year(search_term)
    denomination = denomination_checker(search_term)
    
    # Format search for URL
    search_query = "+".join(search_term.split())
    
    # Initialize price lists
    error_prices = []
    proof_prices = []
    graded_prices = []
    mintmark_prices = []
    roll_prices = []
    raw_prices = []
    
    # Store all listings
    all_listings = []
    
    # Tracking
    total_items_written = 0
    total_items_in_stats = 0
    
    # Set up Chrome driver
    options = uc.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_argument('--start-maximized')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    
    try:
        driver = uc.Chrome(options=options, version_main=145)
    except Exception:
        try:
            driver = uc.Chrome(options=options, use_subprocess=True)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to start browser: {str(e)}")
    
    try:
        # Scrape pages
        for i in range(1, request.num_pages + 1):
            url = f"https://www.ebay.com/sch/i.html?_nkw={search_query}&_sacat=0&rt=nc&LH_Sold=1&LH_Complete=1&_pgn={i}"
            
            driver.get(url)
            
            try:
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "srp-river-results"))
                )
            except:
                continue
            
            time.sleep(random.uniform(1, 2))
            
            page_source = driver.page_source
            doc = BeautifulSoup(page_source, "html.parser")
            page_container = doc.find(class_="srp-river-results clearfix")
            
            if page_container is None:
                continue
            
            listings = page_container.find_all("li", class_="s-card")
            
            for item in listings:
                title_elem = item.find(class_="s-card__title")
                price_elem = item.find(class_="s-card__price")
                date_elem = item.find("span", class_="su-styled-text positive default")
                link_elem = item.find("a", class_="s-card__link")
                
                if not title_elem or not price_elem:
                    continue
                
                title = title_elem.text.strip()
                
                if not matches_specific_coin(title, search_term, search_year):
                    continue
                
                price = price_elem.text.strip()
                date = date_elem.text.strip() if date_elem else "N/A"
                link = link_elem['href'].split("?")[0] if link_elem and link_elem.get('href') else "N/A"
                
                category, should_include = categorize_listing(title)
                
                if not should_include:
                    continue
                
                # Skip non-USD currencies
                non_usd_symbols = ['€', '£', '¥', 'AU$', 'C$', 'CA$', 'NZ$', 'HK$']
                if any(symbol in price for symbol in non_usd_symbols):
                    continue
                
                included_in_stats = False
                price_aud = None
                
                if price and price != "N/A":
                    price_clean = price.replace("$", "").replace(",", "")
                    if 'to' in price_clean:
                        price_clean = sum([float(num) for num in price_clean.split() if num != 'to']) / 2
                        price_clean = round(price_clean, 2)
                    
                    try:
                        price_float = float(price_clean)
                        price_aud = round(price_float * request.usd_to_aud_rate, 2)
                        
                        # Categorize and add to appropriate list
                        if category == 'error':
                            error_prices.append(price_aud)
                            included_in_stats = True
                        elif category == 'proof':
                            proof_prices.append(price_aud)
                            included_in_stats = True
                        elif category == 'graded':
                            graded_prices.append(price_aud)
                            included_in_stats = True
                        elif category == 'mint mark':
                            mintmark_prices.append(price_aud)
                            included_in_stats = True
                        elif category == 'roll':
                            # Apply denomination-specific price filters
                            min_prices = {
                                'one cent': 0.75, 'two cents': 1.5, 'five cents': 3,
                                'ten cents': 6, 'twenty cents': 6, 'fifty cents': 15,
                                'one dollar': 30, 'two dollar': 75
                            }
                            min_price = min_prices.get(denomination, 0)
                            if price_aud > min_price:
                                roll_prices.append(price_aud)
                                included_in_stats = True
                        elif category == 'raw':
                            raw_prices.append(price_aud)
                            included_in_stats = True
                    
                    except ValueError:
                        pass
                
                # Add to listings
                listing_data = {
                    "title": title,
                    "price_usd": price,
                    "price_aud": price_aud,
                    "date": date,
                    "link": link,
                    "category": category,
                    "included_in_stats": included_in_stats
                }
                all_listings.append(listing_data)
                total_items_written += 1
                if included_in_stats:
                    total_items_in_stats += 1
            
            # Delay between pages
            if i < request.num_pages:
                time.sleep(random.uniform(2, 4))
    
    finally:
        driver.quit()
    
    # Calculate statistics for each category
    return ScrapeResponse(
        search_query=search_term,
        detected_year=search_year,
        detected_denomination=denomination,
        total_listings_found=total_items_written,
        total_items_in_stats=total_items_in_stats,
        total_items_documented_only=total_items_written - total_items_in_stats,
        error_coins=calculate_stats(error_prices),
        proof_coins=calculate_stats(proof_prices),
        graded_coins=calculate_stats(graded_prices),
        mintmark_coins=calculate_stats(mintmark_prices),
        coin_rolls=calculate_stats(roll_prices),
        raw_coins=calculate_stats(raw_prices),
        listings=all_listings
    )

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
