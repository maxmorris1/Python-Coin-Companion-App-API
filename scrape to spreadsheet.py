import csv
from coin_scraper import scrape_ebay_coin
australian_coins_regular = 'Australian_Coins_Regular.txt'
australian_coins_graded = 'Australian_Coins_Graded.txt'
with open('coin_prices_regular.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['Title', 'Year', 'Price AUD', 'Date', 'Category'])
    with open(australian_coins_regular, 'r') as file:
        for line in file:
            words = line.split()
            words_length = len(words)
            if words_length > 3: