# main.py
from src.wikipedia_scraper import WikipediaScraper

if __name__ == "__main__":

    scraper = WikipediaScraper()

    # Ask user for multiprocessing y/n pass as Boolean switch True/False
    while True:
        mp_choice = input("Use multiprocessing for Wikipedia scraping? (y/n): ").strip().lower()
        if mp_choice in ("y", "n"):
            break
        print("Invalid input. Please type 'y' or 'n'.")
    use_mp = mp_choice == "y"

    # Fetch data
    countries = scraper.get_countries()
    for country in countries:
        scraper.get_leaders(country, use_multiprocessing=use_mp)

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