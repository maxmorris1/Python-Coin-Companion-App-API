"""
Validation script - checks if Sold_listings.txt matches the search query
"""
import re
import sys

def extract_search_info(search_query):
    """Extract key identifying terms from search query"""
    search_lower = search_query.lower()
    
    # Extract year if present
    year_match = re.search(r'\b(19\d{2}|20\d{2})\b', search_query)
    year = year_match.group(1) if year_match else None
    
    # Extract key terms (excluding common words)
    common_words = {'the', 'and', 'or', 'a', 'an', 'coin', 'australian', 'australia'}
    words = search_query.lower().split()
    keywords = [w for w in words if w not in common_words and not w.isdigit()]
    
    # Identify special search types
    search_type = []
    if 'no sd' in search_lower or 'missing sd' in search_lower:
        search_type.append('error-no-sd')
    elif 'mule' in search_lower:
        search_type.append('error-mule')
    elif 'double strike' in search_lower:
        search_type.append('error-double-strike')
    
    if 'mintmark' in search_lower or 'privy' in search_lower:
        search_type.append('mintmark')
    
    if 'silver' in search_lower or 'proof' in search_lower:
        search_type.append('proof')
    
    if 'pcgs' in search_lower or 'ngc' in search_lower or 'graded' in search_lower:
        search_type.append('graded')
    
    return {
        'year': year,
        'keywords': keywords,
        'search_type': search_type,
        'original': search_query
    }

def validate_listing(title, search_info):
    """Check if a listing title matches the search criteria"""
    title_lower = title.lower()
    
    # Check year match (strict)
    if search_info['year']:
        title_years = re.findall(r'\b(19\d{2}|20\d{2})\b', title)
        # If title has years but search year not among them, it's a mismatch
        if title_years and search_info['year'] not in title_years:
            return False, f"Year mismatch (expected {search_info['year']}, found {title_years})"
    
    # Check keyword matches (require at least 50% of keywords to match)
    if search_info['keywords']:
        # Count how many keywords appear in the title
        matched_keywords = [kw for kw in search_info['keywords'] if kw in title_lower]
        match_rate = len(matched_keywords) / len(search_info['keywords'])
        
        if match_rate < 0.5:
            missing = [kw for kw in search_info['keywords'] if kw not in title_lower]
            return False, f"Too few keywords matched (missing: {missing})"
    
    return True, "Match"

def analyze_sold_listings(search_query, filename='Sold_listings.txt'):
    """Analyze Sold_listings.txt and check if results match search query"""
    
    print("="*80)
    print("EBAY SCRAPER RESULTS VALIDATION")
    print("="*80)
    print(f"\nSearch Query: '{search_query}'")
    
    search_info = extract_search_info(search_query)
    
    print(f"\nSearch Analysis:")
    print(f"  Year filter: {search_info['year'] if search_info['year'] else 'None'}")
    print(f"  Key terms: {', '.join(search_info['keywords'])}")
    print(f"  Special types: {', '.join(search_info['search_type']) if search_info['search_type'] else 'None'}")
    
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        print(f"\n❌ ERROR: {filename} not found!")
        return
    
    # Find all listings
    listings = []
    current_listing = {}
    
    for line in content.split('\n'):
        if line.startswith('[') and ']' in line:
            # Category marker
            if current_listing:
                listings.append(current_listing)
                current_listing = {}
            category_match = re.search(r'\[(.*?)\]', line)
            if category_match:
                current_listing['category'] = category_match.group(1)
                current_listing['in_stats'] = '✓ INCLUDED IN STATS' in line
        elif line.startswith('Title:'):
            current_listing['title'] = line.replace('Title:', '').strip()
        elif line.startswith('Price:'):
            current_listing['price'] = line.replace('Price:', '').strip()
        elif line.startswith('Date:'):
            current_listing['date'] = line.replace('Date:', '').strip()
    
    if current_listing:
        listings.append(current_listing)
    
    print(f"\n{'='*80}")
    print(f"RESULTS FOUND: {len(listings)} listings")
    print(f"{'='*80}")
    
    if len(listings) == 0:
        print("\n⚠️  No listings found in file.")
        return
    
    # Validate each listing
    matching = 0
    mismatched = []
    
    # Count by category
    category_counts = {}
    
    for listing in listings:
        if 'title' not in listing:
            continue
        
        # Count categories
        cat = listing.get('category', 'UNKNOWN')
        category_counts[cat] = category_counts.get(cat, 0) + 1
        
        # Validate against search
        is_valid, reason = validate_listing(listing['title'], search_info)
        
        if is_valid:
            matching += 1
        else:
            mismatched.append({
                'title': listing['title'][:100] + '...' if len(listing['title']) > 100 else listing['title'],
                'reason': reason,
                'category': cat
            })
    
    # Print category breakdown
    print("\nCategory Breakdown:")
    for cat, count in sorted(category_counts.items()):
        print(f"  {cat}: {count}")
    
    # Print validation results
    print(f"\n{'='*80}")
    print("VALIDATION RESULTS")
    print(f"{'='*80}")
    
    total = len([l for l in listings if 'title' in l])
    match_rate = (matching / total * 100) if total > 0 else 0
    
    print(f"\nTotal listings analyzed: {total}")
    print(f"✓ Matching search criteria: {matching} ({match_rate:.1f}%)")
    print(f"✗ Not matching: {len(mismatched)} ({100-match_rate:.1f}%)")
    
    # Determine pass/fail
    if match_rate >= 90:
        print(f"\n{'='*80}")
        print("✅ VALIDATION PASSED - Excellent match rate!")
        print("="*80)
    elif match_rate >= 75:
        print(f"\n{'='*80}")
        print("⚠️  VALIDATION WARNING - Acceptable but some mismatches found")
        print("="*80)
    else:
        print(f"\n{'='*80}")
        print("❌ VALIDATION FAILED - Too many mismatched results")
        print("="*80)
    
    # Show mismatched examples (up to 10)
    if mismatched:
        print(f"\nSample Mismatched Listings (showing up to 10):")
        print("-" * 80)
        for i, item in enumerate(mismatched[:10], 1):
            print(f"\n{i}. [{item['category']}]")
            print(f"   Title: {item['title']}")
            print(f"   Issue: {item['reason']}")
    
    # Recommendations
    print(f"\n{'='*80}")
    print("RECOMMENDATIONS")
    print("="*80)
    
    if match_rate < 90:
        print("\n⚠️  Consider improving the search query or scraper filters if needed:")
        if search_info['year'] and any('Year mismatch' in m['reason'] for m in mismatched):
            print("  • Year filtering may need refinement")
        if any('keywords' in m['reason'].lower() for m in mismatched):
            print("  • Keyword matching logic could be more flexible")
    else:
        print("\n✅ Results look good! The scraper is working as expected.")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        search_query = ' '.join(sys.argv[1:])
    else:
        search_query = input("Enter the search query you used: ")
    
    analyze_sold_listings(search_query)
