"""
Example client script for testing the eBay Coin Scraper API
Run the API server first: uvicorn api:app --reload
"""

import requests
import json

# API endpoint
API_URL = "http://localhost:8000"

def test_health():
    """Test the health check endpoint"""
    print("Testing health endpoint...")
    response = requests.get(f"{API_URL}/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}\n")

def scrape_coin(search_item, num_pages=2):
    """Scrape eBay for a specific coin"""
    print(f"Scraping eBay for: {search_item}")
    print(f"Pages to scrape: {num_pages}\n")
    
    payload = {
        "search_item": search_item,
        "num_pages": num_pages,
        "usd_to_aud_rate": 1.52
    }
    
    response = requests.post(f"{API_URL}/scrape", json=payload)
    
    if response.status_code == 200:
        data = response.json()
        
        print("=" * 60)
        print("SCRAPING RESULTS")
        print("=" * 60)
        print(f"Search Query: {data['search_query']}")
        print(f"Detected Year: {data['detected_year']}")
        print(f"Detected Denomination: {data['detected_denomination']}")
        print(f"\nTotal Listings Found: {data['total_listings_found']}")
        print(f"Items in Statistics: {data['total_items_in_stats']}")
        print(f"Items Documented Only: {data['total_items_documented_only']}")
        
        print("\n" + "=" * 60)
        print("PRICE ANALYSIS BY CATEGORY")
        print("=" * 60)
        
        categories = [
            ('error_coins', '🚨 Error Coins'),
            ('proof_coins', '💎 Proof Coins'),
            ('graded_coins', '⭐ Graded Coins'),
            ('mintmark_coins', '🏛️ Mintmark Coins'),
            ('coin_rolls', '🎲 Coin Rolls'),
            ('raw_coins', '📌 Raw Coins')
        ]
        
        for key, label in categories:
            category_data = data.get(key)
            if category_data:
                print(f"\n{label}:")
                print(f"  Count: {category_data['count']}")
                print(f"  Range: AU${category_data['lowest_price']} - AU${category_data['highest_price']}")
                print(f"  Average: AU${category_data['average']}")
                print(f"  Median: AU${category_data['median']}")
        
        # Show first 5 listings
        if data['listings']:
            print("\n" + "=" * 60)
            print("SAMPLE LISTINGS (First 5)")
            print("=" * 60)
            for i, listing in enumerate(data['listings'][:5], 1):
                print(f"\n{i}. [{listing['category'].upper()}] {'✓' if listing['included_in_stats'] else '○'}")
                print(f"   Title: {listing['title']}")
                print(f"   Price: {listing['price_usd']} (AU${listing['price_aud']})")
                print(f"   Date: {listing['date']}")
        
        print("\n✓ Scraping completed successfully!")
        
        # Save full results to file
        with open('api_results.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print("Full results saved to api_results.json")
        
        return data
    else:
        print(f"Error: {response.status_code}")
        print(response.text)
        return None

if __name__ == "__main__":
    # Test health endpoint
    test_health()
    
    # Example searches
    print("Starting scrape test...\n")
    
    # Example 1: Search for a specific year and denomination
    scrape_coin("1966 Australian 50 cent", num_pages=2)
    
    # Uncomment to test more searches:
    # scrape_coin("1988 2 dollar aboriginal", num_pages=2)
    # scrape_coin("1972 5 cent no sd", num_pages=2)
    # scrape_coin("2012 red poppy 50 cent", num_pages=2)
