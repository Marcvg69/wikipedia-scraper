# main.py
from src.wikipedia_scraper import WikipediaScraper

scraper = WikipediaScraper()

# Fetch data
countries = scraper.get_countries()
for country in countries:
    scraper.get_leaders(country)

# Save to file
scraper.to_json_file("leaders.json")
