from bs4 import BeautifulSoup
import time
import random
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import statistics

search_item = input("Input the eBay item: ")
original_search = search_item
search_item = search_item.split(" ")
search_item = ("+").join(search_item)

# Extract year from search to filter specific coin year
import re
search_year = None
year_match = re.search(r'\b(19\d{2}|20\d{2})\b', original_search)
if year_match:
    search_year = year_match.group(1)
    print(f"Detected specific year: {search_year}")

one_dollar = ['$1', '1 dollar', 'one dollar', '1dollar', 'kangaroo', 'kangaroos', 'mob of roos']
two_dollar = ['$2', '2 dollar', 'two dollar', '2dollar', 'aboriginal elder', 'southern cross']
fifty_cents = ['50c', '50 cent', 'fifty cent', 'half dollar', 'coat of arms']
twenty_cents = ['20c', '20 cent', 'twenty cent', 'platypus']
ten_cents = ['10c', '10 cent', 'ten cent', 'dime', 'lyrebird']
five_cents = ['5c', '5 cent', 'five cent', 'nickel', 'echidna', 'spiny anteater']
two_cent = ['2c', '2 cent', 'two cent', 'frilled neck lizard', 'frill neck']
one_cent = ['1c', '1 cent', 'one cent', 'penny', 'feather-tailed glider', 'feather tailed glider']

def denomination_checker():
    search_lower = original_search.lower() 
    
    if any(denomination in search_lower for denomination in one_dollar):
        return 'one dollar'
    if any(denomination in search_lower for denomination in two_dollar):
        return 'two dollar'
    if any(denomination in search_lower for denomination in fifty_cents):
        return 'fifty cents'
    if any(denomination in search_lower for denomination in twenty_cents):
        return 'twenty cents'
    if any(denomination in search_lower for denomination in ten_cents):
        return 'ten cents'
    if any(denomination in search_lower for denomination in five_cents):
        return 'five cents'
    if any(denomination in search_lower for denomination in two_cent):
        return 'two cents'
    if any(denomination in search_lower for denomination in one_cent):
        return 'one cent'
    
    return None 

print(f"\nSearching eBay for '{original_search}'...")
print("Opening browser (this may take a moment on first run)...")

# Set up undetected Chrome driver
options = uc.ChromeOptions()
# Comment out headless mode so you can see the browser working
options.add_argument('--headless')
options.add_argument('--disable-blink-features=AutomationControlled')
options.add_argument('--start-maximized')

# Let undetected_chromedriver handle version automatically
try:
    driver = uc.Chrome(options=options, version_main=145)
except Exception as e:
    print(f"Error starting browser: {e}")
    print("Trying without version specification...")
    driver = uc.Chrome(options=options, use_subprocess=True)

price_list = []
f = open("Sold_listings.txt", "w", encoding="utf-8")

# Write header explaining the markers
f.write("="*70 + "\n")
f.write("SOLD LISTINGS - eBay Scraper Results\n")
f.write("="*70 + "\n")
f.write("LEGEND:\n")
f.write("  ✓ INCLUDED IN STATS - Price was used in final statistics calculation\n")
f.write("  ○ Documented only - Listing recorded but not included in stats\n")
f.write("                      (e.g., price too low for rolls, invalid price)\n")
f.write("="*70 + "\n\n")

# Separate price lists for each category
error_prices = []
proof_prices = []
graded_prices = []
mintmark_prices = []
roll_prices = []
raw_prices = []

# ============================================================================
# COMPREHENSIVE KEYWORD LISTS FOR AUSTRALIAN COIN CATALOG
# ============================================================================
# These keywords ensure all coins in the Australian Coins Catalog can be 
# properly identified and categorized. Keywords cover:
# - Error coins and varieties
# - Mintmark variations
# - Proof and premium coins
# - Popular collectibles ("Big Four" colored $2s, Honey Bee, etc.)
# ============================================================================

proof_keywords = [
    'silver', 'proof', 'gold', 'investment coin',
    'ram proof', 'royal australian mint proof', 
    'fine silver', '.999 silver', '.999', 
    'proof set', 'silver proof', 'gold proof',
    'piedfort', 'specimen'
]

# Comprehensive mintmark keywords for all variations
c_mintmark_keywords = [
    'c mint mark', 'c mintmark', 'c privy', 'canberra mintmark', 
    's mint mark', 's mintmark', 'sydney mintmark',
    'm mint mark', 'm mintmark', 'melbourne mintmark',
    'b mint mark', 'b mintmark', 'brisbane mintmark',
    'a mint mark', 'a mintmark', 'adelaide mintmark',
    'mint mark', 'privy mark', 'mintmark', 'privy'
]


# Error coin keywords - comprehensive list for all known errors
error_keywords = [
    # Major error types
    'mule', 'mule error', '$1 $10 mule', 'dollar ten cent mule',
    'no sd', 'missing sd', 'sd error', '1972 no sd',
    'double strike', 'double struck', 'struck twice',
    'double header', 'double obverse', 'two heads', 'double tail',
    'off center', 'off-center', 'misaligned', 'shifted strike',
    
    # Planchet errors
    'clipped planchet', 'clip', 'straight clip', 'curved clip',
    'wrong planchet', 'wrong stock',
    'broadstrike', 'broad strike', 'no collar',
    
    # Die errors
    'die crack', 'cud', 'die break', 'die error',
    'rotated die', 'medal alignment',
    
    # Strike errors
    'struck through', 'filled die', 'grease strike',
    'weak strike', 'insufficient strike',
    'brockage', 'mirror strike',
    
    # Material errors
    'missing clad', 'delamination', 'lamination',
    'peeling', 'clad error',
    
    # Varieties
    'frosted', 'frosted anzac', 'incuse flag',
    'variety', 'error variety',
    'mintmark error', 'missing mintmark',
    
    # General error terms
    'error', 'mint error', 'minting error',
    'rare error', 'major error'
]

# Keywords to identify graded coins
graded_keywords = ['pcgs', 'ngc', 'anacs', 'icg', 'graded', 'ms65', 'ms66', 'ms67', 'ms68', 'ms69', 'ms70', 'pf', 'pr', 'proof', 'ms']

# Keywords to identify coin rolls
roll_keywords = ['roll', 'rolls', '50 coins', 'bank roll', 'full roll', 'half roll', 'quarter roll', 'cotton & co', 'bankbag', 'bag', 'cotton and co', 'security roll']
roll_skip_keywords = ['ex', 'ex mint', 'card']

# Keywords that indicate lots/sets we should skip entirely
skip_keywords = [
    'lot', 'bulk', 'collection', 'set of', 'mixed', 'assorted', 
    'proof set', 'mint set', 'uncirculated set',
    # Multiple coin patterns
    '2 x', '3 x', '4 x', '5 x', '6 x', '7 x', '8 x', '9 x', '10 x',
    '2x', '3x', '4x', '5x', '6x', '7x', '8x', '9x', '10x',
    'x 2', 'x 3', 'x 4', 'x 5', 'x 6', 'x 7', 'x 8', 'x 9', 'x 10',
    ' x2', ' x3', ' x4', ' x5', ' x6', ' x7', ' x8', ' x9', ' x10',
    'pair of', 'trio', 'quad', 'multiple coins', 'two coins', 'three coins',
    'four coins', 'five coins', 'six coins',
    # Currencies to exclude (non-USD listings)
    'euro', '€', 'eur', 'gbp', '£', 'pound sterling', 'pounds',
    'cad', 'canadian dollar', 'aud', 'australian dollar',
    'nzd', 'new zealand dollar', 'jpy', '¥', 'yen',
    'cny', 'rmb', 'yuan', 'inr', 'rupee', 'rupees',
    'mxn', 'peso', 'pesos', 'chf', 'swiss franc',
    'sek', 'krona', 'dkk', 'krone', 'nok',
    'sgd', 'singapore dollar', 'hkd', 'hong kong dollar',
    'krw', 'won', 'php', 'thb', 'baht', 'zar', 'rand'
]

def matches_specific_coin(title, search_term, search_year):
    """
    Check if the listing title matches the specific coin being searched for.
    Returns True only if the coin matches the year and key identifiers.
    """
    title_lower = title.lower()
    search_lower = search_term.lower()
    
    # If a specific year was detected in the search
    if search_year:
        # Extract all 4-digit years from the title
        title_years = re.findall(r'\b(19\d{2}|20\d{2})\b', title)
        
        # If title has years but none match our search year, exclude it
        if title_years and search_year not in title_years:
            return False
    
    # Check for compound error phrases first (treat as single units)
    error_phrases = ['no sd', 'missing sd', 'double strike', 'double header', 
                     'off center', 'off-center', 'no collar', 'die crack']
    
    # If search contains a compound error phrase, check if title contains it
    for phrase in error_phrases:
        if phrase in search_lower:
            # For error searches, be more lenient - just check year and error phrase
            if phrase in title_lower:
                return True
    
    # Extract key words from search (excluding common words)
    common_words = {'the', 'and', 'or', 'a', 'an', 'coin', 'australian', 'australia', 'cent', 'dollar'}
    search_keywords = set(search_lower.split()) - common_words - {search_year.lower() if search_year else ''}
    
    # Check if at least most of the key search terms appear in the title
    if search_keywords:
        matches = sum(1 for keyword in search_keywords if keyword in title_lower)
        # Require at least 60% of keywords to match
        if matches < len(search_keywords) * 0.6:
            return False
    
    return True

def has_keyword_without_no(title_lower, keywords):
    """
    Check if any keyword appears in the title WITHOUT being preceded by 'no'.
    Returns True only if keyword is found and NOT negated by 'no'.
    
    Exception: Some error types include 'no' as part of their name (e.g., 'no SD', 'no collar').
    These are treated as positive matches.
    """
    # Error terms where "no" is part of the actual error name, not a negation
    no_exceptions = [
        'no sd', 'no collar', 'missing sd', 'sd error',
        '1972 no sd', 'no clad'
    ]
    
    # First check if any exception phrases are present
    for exception in no_exceptions:
        if exception in title_lower:
            return True
    
    for keyword in keywords:
        if keyword in title_lower:
            # Check if 'no' appears immediately before the keyword
            no_pattern = f"no {keyword}"
            if no_pattern not in title_lower:
                return True
    return False

def categorize_listing(title):
    title_lower = title.lower()
    
    # Skip lots/bulk/sets
    if any(keyword in title_lower for keyword in skip_keywords):
        return 'skip', False
    
    # Check for error coins (HIGH PRIORITY - often valuable)
    # Skip if listing says "no errors" or similar
    if has_keyword_without_no(title_lower, error_keywords):
        return 'error', True
    
    # Check for proof/premium coins
    # Skip if listing says "no proof" or similar
    if has_keyword_without_no(title_lower, proof_keywords):
        return 'proof', True
    
    # Check for graded coins
    if has_keyword_without_no(title_lower, graded_keywords):
        return 'graded', True
    
    # Check for mintmark coins
    # Skip if listing says "no mintmark" or similar
    if has_keyword_without_no(title_lower, c_mintmark_keywords):
        return 'mint mark', True
    
    # Check for rolls (but exclude false positives)
    # Skip if listing says "no roll" or similar
    if has_keyword_without_no(title_lower, roll_keywords):
        # Skip if it's actually a coin FROM a roll, not a roll itself
        if not any(skip in title_lower for skip in roll_skip_keywords):
            return 'roll', True
    
    # Default to raw coin
    return 'raw', True


# Currency conversion (update this rate as needed)
USD_TO_AUD = 1.52  # 1 USD = 1.52 AUD (adjust this rate as needed)

denomination = denomination_checker()
print(f"Detected denomination: {denomination}")
print(f"Currency: Converting USD to AUD (rate: {USD_TO_AUD})")

# Global tracking across all pages
total_items_written = 0
total_items_in_stats = 0

try:
    # The range of pages starting at page 1
    for i in range(3)[1:]:
        url = f"https://www.ebay.com/sch/i.html?_nkw={search_item}&_sacat=0&rt=nc&LH_Sold=1&LH_Complete=1&_pgn={i}"
        print(f"\nFetching page {i}...")
        
        # Navigate to the URL
        driver.get(url)
        
        # Wait for page to load - wait for search results container
        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "srp-river-results"))
            )
        except:
            print(f"⚠️ Timed out waiting for page {i} to load")
            continue
        
        # Small random delay to seem more human
        time.sleep(random.uniform(1, 2))
        
        # Get page source and parse with BeautifulSoup
        page_source = driver.page_source
        doc = BeautifulSoup(page_source, "html.parser")

        page_container = doc.find(class_="srp-river-results clearfix")
        
        # Check if the results container was found
        if page_container is None:
            print(f"⚠️  Could not find results container on page {i}")
            listings = []
        else:
            # eBay uses s-card class for listings, not s-item
            listings = page_container.find_all("li", class_="s-card")
            print(f"✓ Found {len(listings)} listings on page {i}")
        
        items_written = 0
        items_in_stats = 0  # Track items actually used in price statistics
        skipped_count = 0
        graded_count = 0
        raw_count = 0
        roll_count = 0
        error_count = 0
        proof_count = 0
        mintmark_count = 0
        wrong_coin_count = 0  # Track coins filtered out for not matching search
        
        for item in listings:
            # Add None checks to prevent crashes - new eBay structure uses different classes
            title_elem = item.find(class_ = "s-card__title")
            price_elem = item.find(class_ = "s-card__price")
            date_elem = item.find("span", class_="su-styled-text positive default")
            link_elem = item.find("a", class_ = "s-card__link")
            
            # Skip items that don't have required fields
            if not title_elem or not price_elem:
                continue
                
            title = title_elem.text.strip()
            
            # FILTER: Check if this listing matches the specific coin we're searching for
            if not matches_specific_coin(title, original_search, search_year):
                wrong_coin_count += 1
                continue
            
            price = price_elem.text.strip()
            date = date_elem.text.strip() if date_elem else "N/A"
            link = link_elem['href'].split("?")[0] if link_elem and link_elem.get('href') else "N/A"
            
            # Categorize the listing
            category, should_include = categorize_listing(title)
            denomination= denomination_checker()
            
            if not should_include:
                skipped_count += 1
                continue
            
            # Skip non-USD currencies (check price field for currency symbols)
            non_usd_symbols = ['€', '£', '¥', 'AU$', 'C$', 'CA$', 'NZ$', 'HK$']
            if any(symbol in price for symbol in non_usd_symbols):
                skipped_count += 1
                continue
            
            # Track if this item will be included in stats
            included_in_stats = False
            
            if price and price != "N/A":
                price_clean = price.replace("$", "").replace(",", "")
                if 'to' in price_clean:
                    price_clean = sum([float(num) for num in price_clean.split() if num != 'to']) / 2
                    price_clean = round(price_clean, 2)
                
                try:
                    price_float = float(price_clean)
                    # Convert USD to AUD
                    price_aud = round(price_float * USD_TO_AUD, 2)
                    
                    # Add to appropriate category with different price ranges (using AUD)
                    if category == 'error':
                        error_prices.append(price_aud)
                        error_count += 1
                        included_in_stats = True
                    elif category == 'proof':
                        proof_prices.append(price_aud)
                        proof_count += 1
                        included_in_stats = True
                    elif category == 'graded':
                        graded_prices.append(price_aud)
                        graded_count += 1
                        included_in_stats = True
                    elif category == 'mint mark':
                        mintmark_prices.append(price_aud)
                        mintmark_count += 1
                        included_in_stats = True
                    elif category == 'roll' and denomination == 'one cent':
                        if price_aud > 0.75: 
                            roll_prices.append(price_aud)
                            roll_count += 1
                            included_in_stats = True
                    elif category == 'roll' and denomination == 'two cents':
                        if price_aud > 1.5: 
                            roll_prices.append(price_aud)
                            roll_count += 1
                            included_in_stats = True
                    elif category == 'roll' and denomination == 'five cents':
                        if price_aud > 3: 
                            roll_prices.append(price_aud)
                            roll_count += 1
                            included_in_stats = True
                    elif category == 'roll' and denomination == 'ten cents':
                        if price_aud > 6: 
                            roll_prices.append(price_aud)
                            roll_count += 1
                            included_in_stats = True
                    elif category == 'roll' and denomination == 'twenty cents':
                        if price_aud > 6: 
                            roll_prices.append(price_aud)
                            roll_count += 1
                            included_in_stats = True
                    elif category == 'roll' and denomination == 'fifty cents':
                        if price_aud > 15: 
                            roll_prices.append(price_aud)
                            roll_count += 1
                            included_in_stats = True
                    elif category == 'roll' and denomination == 'one dollar':
                        if price_aud > 30: 
                            roll_prices.append(price_aud)
                            roll_count += 1
                            included_in_stats = True
                    elif category == 'roll' and denomination == 'two dollar':
                        if price_aud > 75: 
                            roll_prices.append(price_aud)
                            roll_count += 1
                            included_in_stats = True
                    elif category == 'raw':
                        raw_prices.append(price_aud)
                        raw_count += 1
                        included_in_stats = True
                            
                except ValueError:
                    # Skip prices that can't be converted to float
                    pass
            
            # Write to file with category label and stats indicator
            stats_marker = "✓ INCLUDED IN STATS" if included_in_stats else "○ Documented only"
            f.write(f"[{category.upper()}] {stats_marker}\n")
            f.write(f"Title: {title}\n")
            f.write(f"Price: {price}\n")
            f.write(f"Date: {date}\n")
            f.write(f"Link: {link}\n")
            f.write("---\n")
            items_written += 1
            if included_in_stats:
                items_in_stats += 1
        
        print(f"  Scraped {items_written} items from page {i}")
        print(f"    • {items_in_stats} included in stats | {items_written - items_in_stats} documented only")
        print(f"    • {raw_count} raw coins, {roll_count} rolls, {graded_count} graded")
        if skipped_count > 0:
            print(f"    • Skipped {skipped_count} listings (lots/bulk/sets)")
        if wrong_coin_count > 0:
            print(f"    • Filtered {wrong_coin_count} listings (different coin/year)")
        
        # Update global counters
        total_items_written += items_written
        total_items_in_stats += items_in_stats
        
        # Random delay between pages
        if i < 2:  # Don't wait after the last page
            delay = random.uniform(2, 4)
            print(f"  Waiting {delay:.1f} seconds before next page...")
            time.sleep(delay)

finally:
    # Always close the browser
    driver.quit()
    print("\nBrowser closed.")

# Remove duplicates and sort for each category
error_prices = sorted(list(set(error_prices)))
proof_prices = sorted(list(set(proof_prices)))
graded_prices = sorted(list(set(graded_prices)))
mintmark_prices = sorted(list(set(mintmark_prices)))
roll_prices = sorted(list(set(roll_prices)))
raw_prices = sorted(list(set(raw_prices)))

total_items = len(error_prices) + len(proof_prices) + len(graded_prices) + len(mintmark_prices) + len(roll_prices) + len(raw_prices)

print(f"\n{'='*60}")
print(f"SCRAPING SUMMARY")
print(f"{'='*60}")
print(f"Total sold listings found: {total_items_written}")
print(f"Items included in statistics: {total_items}")
print(f"Items documented only: {total_items_written - total_items}")
print(f"\n{'='*60}")
print(f"PRICE ANALYSIS BY CATEGORY")
print(f"{'='*60}")
print(f"Total unique prices analyzed: {total_items}\n")

def print_stats(category_name, prices, price_list):
    """Helper function to print statistics for a category"""
    if prices:
        avg = round(sum(prices) / len(prices), 2)
        median = round(statistics.median(prices), 2)
        
        print(f"{category_name}:")
        print(f"  Count: {len(prices)}")
        print(f"  Range: AU${min(prices)} - AU${max(prices)}")
        print(f"  Average: AU${avg}")
        print(f"  Median: AU${median}")
        
        price_list.write(f"\n{'='*40}\n")
        price_list.write(f"{category_name.upper()}\n")
        price_list.write(f"{'='*40}\n")
        price_list.write(f"Count: {len(prices)}\n")
        price_list.write(f"Lowest Price: AU${min(prices)}\n")
        price_list.write(f"Highest Price: AU${max(prices)}\n")
        price_list.write(f"Average (Mean): AU${avg}\n")
        price_list.write(f"Median: AU${median}\n")
        
        return True
    else:
        print(f"{category_name}: No items found")
        return False

# Print statistics for each category (only if data exists)
any_found = False

if error_prices:
    print_stats("🚨 ERROR COINS (Mules, Strikes, Die Errors)", error_prices, f)
    any_found = True

if proof_prices:
    if any_found:
        print()
    print_stats("💎 PROOF COINS (Silver, Gold, RAM Proof)", proof_prices, f)
    any_found = True

if graded_prices:
    if any_found:
        print()
    print_stats("⭐ GRADED COINS (PCGS/NGC/etc)", graded_prices, f)
    any_found = True

if mintmark_prices:
    if any_found:
        print()
    print_stats("🏛️ MINTMARK COINS (C/S/M/B/A)", mintmark_prices, f)
    any_found = True

if roll_prices:
    if any_found:
        print()
    print_stats("🎲 COIN ROLLS (Full/Half Rolls)", roll_prices, f)
    any_found = True

if raw_prices:
    if any_found:
        print()
    print_stats("📌 RAW COINS (Standard Circulation)", raw_prices, f)
    any_found = True

if any_found:
    f.write(f"\n{'='*40}\n")
    f.write(f"Note: Skipped lots, bulk purchases, and sets\n")
    f.write(f"Categories detected automatically from listing titles\n")
    print(f"\n💡 Tip: Use the category that matches what you're buying/selling")
    print(f"\n✓ Results saved to Sold_listings.txt")
else:
    print("No items found matching the criteria.")

f.close()
print("Done!")