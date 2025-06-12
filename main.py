# main.py
from src.wikipedia_scraper import WikipediaScraper

scraper = WikipediaScraper()

# Fetch data
countries = scraper.get_countries()
for country in countries:
    scraper.get_leaders(country)

# Save to file
# scraper.to_json_file("leaders.json")
# Ask user how to save the data (JSON or CSV file ?)
while True:
    choice = input("How would you like to save the data? Type 'json' or 'csv': ").strip().lower()
    if choice in ("json", "csv"):
        break
    print("Invalid choice. Please type only 'json' or 'csv'.")

# Step 4: Save the data in chosen format
if choice == "json":
    scraper.to_json_file("leaders.json")
    print("Data saved to leaders.json")
else:
    scraper.to_csv_file("leaders.csv")
    print("Data saved to leaders.csv")