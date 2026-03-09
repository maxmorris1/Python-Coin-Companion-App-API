"""
Test script for eBay scraper - automatically runs test searches and validates results
"""
import subprocess
import time
import re
from pathlib import Path

# Test searches to run (selected from Test_Searches.txt)
test_searches = [
    "1972 5 cent no SD",                    # Error coin with year
    "2012 red poppy $2",                    # Popular collectible
    "1966 round 50 cent silver",            # Year-specific + proof
    "Australian $1 coin",                   # Basic search
    "2018 $1 mintmark C",                   # Mintmark test
]

def extract_key_terms(search_query):
    """Extract key identifying terms from search query"""
    search_lower = search_query.lower()
    
    # Extract year if present
    year_match = re.search(r'\b(19\d{2}|20\d{2})\b', search_query)
    year = year_match.group(1) if year_match else None
    
    # Extract denomination
    denominations = {
        '$1': 'dollar', '1 dollar': 'dollar', 'one dollar': 'dollar',
        '$2': 'dollar', '2 dollar': 'dollar', 'two dollar': 'dollar',
        '50 cent': 'cent', '50c': 'cent',
        '20 cent': 'cent', '20c': 'cent',
        '10 cent': 'cent', '10c': 'cent',
        '5 cent': 'cent', '5c': 'cent',
        '2 cent': 'cent', '2c': 'cent',
        '1 cent': 'cent', '1c': 'cent',
    }
    
    denom = None
    for key, value in denominations.items():
        if key in search_lower:
            denom = value
            break
    
    # Extract special keywords
    keywords = []
    
    # Error keywords
    if 'no sd' in search_lower or 'missing sd' in search_lower:
        keywords.append('sd')
    if 'mule' in search_lower:
        keywords.append('mule')
    if 'double strike' in search_lower:
        keywords.append('double')
    if 'off center' in search_lower or 'off-center' in search_lower:
        keywords.append('center')
    
    # Proof/Premium keywords
    if 'silver' in search_lower:
        keywords.append('silver')
    if 'proof' in search_lower:
        keywords.append('proof')
    
    # Mintmark keywords
    if 'mintmark' in search_lower or 'privy' in search_lower:
        keywords.append('mintmark')
    
    # Design/commemorative keywords
    if 'poppy' in search_lower:
        keywords.append('poppy')
    if 'bee' in search_lower or 'honey bee' in search_lower:
        keywords.append('bee')
    if 'firefighter' in search_lower:
        keywords.append('firefighter')
    if 'federation' in search_lower:
        keywords.append('federation')
    
    return {
        'year': year,
        'denomination': denom,
        'keywords': keywords,
        'original': search_query
    }

def validate_results(search_query, sold_listings_file):
    """Validate that sold listings match the search query"""
    search_info = extract_key_terms(search_query)
    
    print(f"\n{'='*70}")
    print(f"VALIDATING: {search_query}")
    print(f"{'='*70}")
    print(f"Expected - Year: {search_info['year']}, Keywords: {search_info['keywords']}")
    
    try:
        with open(sold_listings_file, 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        print("❌ ERROR: Sold_listings.txt not found!")
        return False
    
    # Find all listings in the file
    listings = content.split('---\n')
    
    total_listings = 0
    matching_listings = 0
    mismatched_listings = []
    
    for listing in listings:
        if 'Title:' not in listing:
            continue
        
        total_listings += 1
        
        # Extract title from listing
        title_match = re.search(r'Title: (.+)', listing)
        if not title_match:
            continue
        
        title = title_match.group(1).lower()
        
        # Check year match (if year was specified)
        year_valid = True
        if search_info['year']:
            # Find all years in title
            title_years = re.findall(r'\b(19\d{2}|20\d{2})\b', title)
            if title_years and search_info['year'] not in title_years:
                year_valid = False
                mismatched_listings.append({
                    'title': title[:80],
                    'reason': f"Year mismatch (expected {search_info['year']}, found {title_years})"
                })
        
        # Check keyword matches
        keyword_valid = True
        if search_info['keywords']:
            # For keyword searches, we want at least some keywords to match
            keyword_matches = sum(1 for kw in search_info['keywords'] if kw in title)
            if keyword_matches == 0:
                keyword_valid = False
                mismatched_listings.append({
                    'title': title[:80],
                    'reason': f"No keywords matched (expected: {search_info['keywords']})"
                })
        
        # Check denomination match (less strict - many listings use different formats)
        denom_valid = True
        if search_info['denomination']:
            if search_info['denomination'] not in title and not any(d in title for d in ['$', 'cent', 'dollar']):
                denom_valid = False
        
        if year_valid and keyword_valid:
            matching_listings += 1
    
    # Print results
    print(f"\n📊 VALIDATION RESULTS:")
    print(f"   Total listings: {total_listings}")
    print(f"   ✓ Matching: {matching_listings}")
    print(f"   ✗ Mismatched: {len(mismatched_listings)}")
    
    if total_listings > 0:
        match_percentage = (matching_listings / total_listings) * 100
        print(f"   Match rate: {match_percentage:.1f}%")
        
        if match_percentage >= 80:
            print(f"   ✅ PASS - Most listings match the search criteria")
            validation_result = True
        elif match_percentage >= 60:
            print(f"   ⚠️  WARNING - Some listings don't match well")
            validation_result = False
        else:
            print(f"   ❌ FAIL - Many listings don't match the search")
            validation_result = False
    else:
        print(f"   ℹ️  No listings found")
        validation_result = True
    
    # Show sample mismatches if any
    if mismatched_listings and len(mismatched_listings) <= 5:
        print(f"\n⚠️  Mismatched listings:")
        for i, mismatch in enumerate(mismatched_listings[:5], 1):
            print(f"   {i}. {mismatch['title']}")
            print(f"      Reason: {mismatch['reason']}")
    
    return validation_result

def run_test(search_query):
    """Run the scraper with a given search query"""
    print(f"\n{'='*70}")
    print(f"RUNNING TEST: {search_query}")
    print(f"{'='*70}")
    
    # Run the scraper with the search query as input
    try:
        result = subprocess.run(
            ['python', 'ebay scraper.py'],
            input=search_query,
            text=True,
            capture_output=True,
            timeout=120  # 2 minute timeout
        )
        
        print("SCRAPER OUTPUT:")
        print(result.stdout)
        
        if result.stderr:
            print("ERRORS/WARNINGS:")
            print(result.stderr)
        
        if result.returncode != 0:
            print(f"❌ Scraper exited with code {result.returncode}")
            return False
        
        return True
        
    except subprocess.TimeoutExpired:
        print("❌ Scraper timed out after 2 minutes")
        return False
    except Exception as e:
        print(f"❌ Error running scraper: {e}")
        return False

def main():
    print("="*70)
    print("EBAY SCRAPER AUTOMATED TEST SUITE")
    print("="*70)
    print(f"Running {len(test_searches)} test searches...\n")
    
    results = []
    
    for i, search in enumerate(test_searches, 1):
        print(f"\n{'#'*70}")
        print(f"TEST {i}/{len(test_searches)}")
        print(f"{'#'*70}")
        
        # Run the scraper
        scraper_success = run_test(search)
        
        if scraper_success:
            # Give it a moment to write the file
            time.sleep(1)
            
            # Validate results
            validation_success = validate_results(search, 'Sold_listings.txt')
            
            results.append({
                'search': search,
                'scraper_ran': True,
                'validation_passed': validation_success
            })
        else:
            results.append({
                'search': search,
                'scraper_ran': False,
                'validation_passed': False
            })
        
        # Wait between tests
        if i < len(test_searches):
            print(f"\nWaiting 5 seconds before next test...")
            time.sleep(5)
    
    # Print summary
    print("\n" + "="*70)
    print("TEST SUMMARY")
    print("="*70)
    
    total = len(results)
    scraper_success_count = sum(1 for r in results if r['scraper_ran'])
    validation_success_count = sum(1 for r in results if r['validation_passed'])
    
    print(f"\nTotal tests: {total}")
    print(f"Scraper ran successfully: {scraper_success_count}/{total}")
    print(f"Validation passed: {validation_success_count}/{total}")
    
    print("\nDetailed Results:")
    for i, result in enumerate(results, 1):
        status = "✅ PASS" if result['validation_passed'] else "❌ FAIL"
        print(f"  {i}. {status} - {result['search']}")
    
    print("\n" + "="*70)
    print("Testing complete!")
    print("="*70)

if __name__ == "__main__":
    main()
