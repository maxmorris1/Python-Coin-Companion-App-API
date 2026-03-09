# Australian Collectible Coins Catalog
# Complete list from decimalization (1966) to 2026

AUSTRALIAN_COINS = {
    # ===== DISCONTINUED COINS =====
    "1_cent": {
        "years": list(range(1966, 1992)),  # Discontinued 1991
        "description": "1 cent - Feather-tailed Glider",
        "commemoratives": []
    },
    
    "2_cent": {
        "years": list(range(1966, 1992)),  # Discontinued 1991
        "description": "2 cent - Frilled-neck Lizard",
        "commemoratives": []
    },
    
    # ===== CURRENT CIRCULATION COINS =====
    "5_cent": {
        "years": list(range(1966, 2027)),
        "description": "5 cent - Echidna",
        "commemoratives": [
            "2016 - Changeover 50th Anniversary"
        ]
    },
    
    "10_cent": {
        "years": list(range(1966, 2027)),
        "description": "10 cent - Lyrebird",
        "commemoratives": [
            "2016 - Changeover 50th Anniversary"
        ]
    },
    
    "20_cent": {
        "years": list(range(1966, 2027)),
        "description": "20 cent - Platypus",
        "commemoratives": [
            "2001 - Centenary of Federation (9 designs - one per state/territory)",
            "2013 - 60th Anniversary of Coronation",
            "2014 - Remembrance Day",
            "2015 - Anzac Centenary",
            "2016 - Changeover 50th Anniversary",
            "2018 - Remembrance Day",
            "2020 - VE Day 75th Anniversary",
            "2021 - National Emergency Medal"
        ]
    },
    
    "50_cent": {
        "years": list(range(1966, 2027)),
        "description": "50 cent - Coat of Arms",
        "note": "1966 round 80% silver coins are highly collectible",
        "commemoratives": [
            # Silver 1966
            "1966 - Round 80% Silver (highly valuable)",
            
            # Major commemoratives
            "1970 - Captain Cook Bicentenary",
            "1977 - Silver Jubilee",
            "1981 - Royal Wedding Charles & Diana",
            "1982 - Commonwealth Games Brisbane",
            "1988 - Bicentenary",
            "1991 - 25th Anniversary of Decimal Currency",
            "1995 - End of WWII 50th Anniversary",
            "1996 - Sir Donald Bradman",
            "1998 - Bass & Flinders Bicentenary",
            "1999 - International Year of Older Persons",
            "2000 - Millennium",
            "2000 - Royal Visit",
            
            # 2001 Centenary of Federation series
            "2001 - Centenary of Federation (multiple designs)",
            "2001 - Australia",
            "2001 - New South Wales",
            "2001 - Victoria",
            "2001 - Queensland",
            "2001 - South Australia",
            "2001 - Western Australia",
            "2001 - Tasmania",
            "2001 - Northern Territory",
            "2001 - Australian Capital Territory",
            
            # 2003-2010
            "2003 - FIFA Women's World Cup",
            "2005 - 60th Anniversary End of WWII",
            "2006 - Commonwealth Games Melbourne",
            "2006 - 150th Anniversary of the Victoria Cross",
            "2008 - Centenary of Scouting",
            "2010 - 100 Years of Australian Coinage",
            
            # 2011-2020
            "2011 - Royal Wedding William & Catherine",
            "2012 - Red Poppy (Remembrance Day)",
            "2013 - Coronation 60th Anniversary",
            "2014 - Green & Gold",
            "2014 - 100 Years of Anzac",
            "2015 - Anzac Centenary (multiple designs)",
            "2015 - Red Poppy",
            "2016 - 50 Years of Decimal Currency",
            "2016 - Changeover",
            "2017 - ANZAC 50 cent",
            "2018 - Armistice Centenary",
            "2019 - International Year of Indigenous Languages",
            "2020 - VE Day 75th Anniversary",
            
            # 2021-2026
            "2021 - Queen's Birthday",
            "2022 - Queen Elizabeth II Memorial",
            "2023 - King Charles III Coronation",
            "2024 - Paris Olympics",
            "2025 - Anzac 110th Anniversary"
        ]
    },
    
    # ===== ONE DOLLAR COINS (Introduced 1984) =====
    "1_dollar": {
        "years": list(range(1984, 2027)),
        "description": "$1 - Five Kangaroos",
        "commemoratives": [
            # 1980s-1990s
            "1984 - First issue",
            "1986 - International Year of Peace",
            "1988 - Bicentenary",
            "1990 - 100 Years of Responsible Government NSW",
            "1991 - 100 Years of Responsible Government VIC",
            "1992 - Year of Space",
            "1993 - Landcare",
            "1994 - Year of the Family",
            "1995 - End of WWII 50th Anniversary",
            
            # 2000s
            "2000 - Millennium",
            "2001 - Centenary of Federation",
            "2003 - Year of the Outback",
            "2003 - Volunteers",
            "2005 - 60th Anniversary End of WWII",
            "2006 - Commonwealth Games",
            "2008 - Centenary of Scouting",
            "2009 - Space",
            
            # 2010s
            "2010 - Burke & Wills",
            "2011 - Kokoda Track",
            "2012 - Red Poppy",
            "2013 - Purple Coronation",
            "2013 - 100 Years of Canberra",
            "2014 - 100 Years of Anzac",
            "2015 - Remembrance Day",
            "2015 - Anzac Centenary (multiple designs)",
            "2016 - Changeover 50th Anniversary",
            "2016 - Olympic Team",
            "2017 - Centenary of Lions",
            "2018 - Armistice Centenary",
            "2019 - Moon Landing 50th",
            "2019 - Mr Squiggle 60th",
            "2019 - Discovery of Invincible & Sydney",
            
            # 2020s
            "2020 - Tooth Fairy",
            "2020 - Donation Dollar",
            "2021 - Judo",
            "2021 - Paralympic Team",
            "2022 - Indigenous Opportuntiy",
            "2023 - King Charles III Coronation",
            "2024 - Paris Olympics",
            "2025 - Anzac 110th Anniversary (expected)"
        ]
    },
    
    # ===== TWO DOLLAR COINS (Introduced 1988) =====
    "2_dollar": {
        "years": list(range(1988, 2027)),
        "description": "$2 - Aboriginal Elder",
        "note": "Regular design features Aboriginal tribal elder & Southern Cross",
        "commemoratives": [
            # First issue
            "1988 - First issue",
            
            # 2010s - Coloured series explosion
            "2012 - Red Poppy",
            "2012 - Remembrance Day Red Poppy",
            "2013 - Coronation",
            "2013 - Purple Stripe - Coronation",
            "2014 - Green Rosemary",
            "2014 - Remembrance Day",
            "2015 - Lest We Forget",
            "2015 - Red Poppy",
            "2015 - Orange ANZAC",
            "2016 - Olympic Team",
            "2016 - 50 Years Decimal Currency",
            "2016 - Changeover",
            "2017 - Indigenous",
            "2017 - Remembrance Day Lest We Forget",
            "2018 - Armistice Centenary",
            "2018 - Remembrance Day - Eternal Flame",
            "2019 - Moon Landing",
            "2019 - Repatriation",
            "2019 - National Emergency Medal",
            
            # 2020s - Major expansion of collectibles
            "2020 - Firefighters",
            "2020 - Donation Dollar",
            "2020 - 75th Anniversary End of WWII",
            "2021 - Olympic Team Tokyo",
            "2021 - Paralympic Team Tokyo",
            "2022 - Honey Bee (highly popular)",
            "2022 - Indigenous Flag",
            "2022 - CPEC (Cerebral Palsy)",
            "2022 - Possum Magic 40th Anniversary",
            "2022 - Mateship",
            "2023 - King Charles III Coronation",
            "2023 - Bananas in Pyjamas",
            "2023 - Women's World Cup FIFA",
            "2023 - Voice Referendum",
            "2024 - 2024C Mr Squiggle",
            "2024 - Paris Olympics",
            "2024 - Paralympics",
            "2024 - WWI Remembrance",
            "2025 - Anzac 110th (expected)",
            "2025 - Bluey (expected)",
            "2026 - Commonwealth Games (expected)"
        ]
    }
}

# ===== PROOF AND SPECIAL SETS =====
PROOF_SETS = {
    "description": "Annual RAM Proof Sets (1966-2026)",
    "years": list(range(1966, 2027)),
    "note": "Each year includes proof versions of all circulating denominations"
}

SILVER_PROOF_COINS = [
    # High-value collectibles
    "1981 - $200 Gold Coin (Charles & Diana)",
    "1988 - $10 State Series Silver Proof",
    "1990-2000 - Silver Kookaburra Series (1oz, 2oz, 10oz, 1kg)",
    "1990-2000 - Silver Koala Series (1oz)",
    "1996-2026 - Lunar Series I & II (Dragon, Snake, Horse, etc)",
    "2000 - $1 Silver Kangaroo",
    "2001 - Federation Proof Silver Set",
    "2006 - Melbourne Commonwealth Games Silver",
    "2012 - Year of the Dragon Silver",
    "2015 - ANZAC Centenary Silver Set",
    "2016 - 50th Anniversary Decimal Currency Silver Set",
    "2020 - $1 Megafauna Set (Silver)",
    "2022 - $2 Honey Bee Silver Proof"
]

SPECIAL_RELEASES = [
    # Mint Sets, Baby Sets, Wedding Sets
    "1966-2026 - Annual Mint Sets (uncirculated)",
    "1966-2026 - Baby Mint Sets",
    "Various - Wedding Coin Sets",
    
    # Special RAM releases
    "2000 - Olympic Games Sydney Series",
    "2006 - Commonwealth Games 18-coin set",
    "2008 - Beijing Olympics Coin Collection",
    "2012 - London Olympics",
    "2016 - Rio Olympics",
    "2020 - Tokyo Olympics (released 2021)",
    "2024 - Paris Olympics",
    
    # Popular collectibles
    "2012-2026 - Alphabet A-Z 20c Series",
    "2018 - Mint Mark Gold $1 (M, S, C, B, A)",
    "2019 - RAM Mintmark Set",
    "2020-2026 - RAM Collector Albums"
]

# ===== MOST VALUABLE/SOUGHT AFTER =====
HIGHLY_COLLECTIBLE = [
    "1966 - 50c Round Silver (80% silver)",
    "1972 - 5c No SD (missing SD mintmark)",
    "2000 - $1/$10 Mule Error",
    "2012 - Red Poppy $2",
    "2013 - Purple Coronation $2",
    "2014 - Green Rosemary $2",
    "2015 - Orange ANZAC $2",
    "2019 - 'Frosted' ANZAC 50c",
    "2020 - Firefighters $2",
    "2022 - Honey Bee $2 (C, S, or mintmark versions)",
    "2023 - King Charles III First Strike",
    "Various - Double Header errors",
    "Various - Struck through errors",
    "Various - Die cracks and varieties"
]

# ===== EXPORT FUNCTION =====
def get_all_coin_years(denomination):
    """Returns list of all years for a specific denomination"""
    if denomination in AUSTRALIAN_COINS:
        return AUSTRALIAN_COINS[denomination]["years"]
    return []

def get_commemoratives(denomination):
    """Returns list of commemorative coins for denomination"""
    if denomination in AUSTRALIAN_COINS:
        return AUSTRALIAN_COINS[denomination]["commemoratives"]
    return []

def print_catalog():
    """Prints the entire catalog"""
    print("=" * 80)
    print("AUSTRALIAN COLLECTIBLE COINS CATALOG (1966-2026)")
    print("=" * 80)
    
    for denom, data in AUSTRALIAN_COINS.items():
        print(f"\n{data['description'].upper()}")
        print(f"Years: {min(data['years'])}-{max(data['years'])}")
        if 'note' in data:
            print(f"Note: {data['note']}")
        
        if data['commemoratives']:
            print(f"\nCommemorative Issues ({len(data['commemoratives'])}):")
            for comm in data['commemoratives']:
                print(f"  • {comm}")
    
    print("\n" + "=" * 80)
    print("PROOF SETS")
    print("=" * 80)
    print(f"{PROOF_SETS['description']}")
    print(f"Years available: {min(PROOF_SETS['years'])}-{max(PROOF_SETS['years'])}")
    
    print("\n" + "=" * 80)
    print("SILVER PROOF COINS (High Value)")
    print("=" * 80)
    for coin in SILVER_PROOF_COINS:
        print(f"  • {coin}")
    
    print("\n" + "=" * 80)
    print("SPECIAL RELEASES & SETS")
    print("=" * 80)
    for item in SPECIAL_RELEASES:
        print(f"  • {item}")
    
    print("\n" + "=" * 80)
    print("HIGHLY COLLECTIBLE / VALUABLE")
    print("=" * 80)
    for item in HIGHLY_COLLECTIBLE:
        print(f"  • {item}")

# Run the catalog
if __name__ == "__main__":
    print_catalog()
    
    # Summary stats
    total_commemoratives = sum(len(data['commemoratives']) for data in AUSTRALIAN_COINS.values())
    print("\n" + "=" * 80)
    print(f"TOTAL COMMEMORATIVE COINS CATALOGED: {total_commemoratives}")
    print(f"TOTAL PROOF SETS: {len(PROOF_SETS['years'])}")
    print(f"TOTAL SILVER PROOFS: {len(SILVER_PROOF_COINS)}")
    print(f"TOTAL SPECIAL RELEASES: {len(SPECIAL_RELEASES)}")
    print("=" * 80)
