import requests
import csv
from bs4 import BeautifulSoup
import json
import re
import time
from multiprocessing import Pool, cpu_count

# ---------------------------------------------------------------------------------
# 🧠 Pickling Explanation:
# Pickling is the process of serializing a Python object into a byte stream,
# so it can be saved to a file or transferred over a network.
# Unpickling is the reverse — turning that stream back into a Python object.
# 
# 🔧 What it's used for:
# - Saving models (e.g. .pkl files in machine learning)
# - Passing data between processes (like here in multiprocessing)
# - Saving and reloading program state
#
# Why it matters for multiprocessing:
# When using multiprocessing.Pool, any function or data passed to worker processes
# must be picklable. That's why we define `fetch_summary_for_leader()` OUTSIDE
# of the class — top-level functions are picklable, nested ones are not.
# ---------------------------------------------------------------------------------
# --- Standalone function for multiprocessing (must be top-level for pickling) ----

def fetch_summary_for_leader(leader):
    url = leader.get("wikipedia_url", "")
    try:
        response = requests.get(url, timeout=10)
        if response.status_code != 200:
            return leader
        soup = BeautifulSoup(response.text, 'html.parser')
        paragraphs = soup.find_all('p')
        for p in paragraphs:
            text = p.get_text()
            if text.strip() and not text.lower().startswith("coordinates"):
                # Clean and sanitize using regex
                summary = re.sub(r"\[\d+\]|\(.*?\)|<.*?>|\/|\u2014|\u2013|\u2020|\u2192|pronunciation:.*|citation needed", "", text, flags=re.IGNORECASE)
                summary = re.sub(r"\s+", " ", summary)
                leader["summary"] = summary.strip()
                return leader
    except:
        return leader
    return

class WikipediaScraper:
    def __init__(self):
        # Base URL and endpoints
        self.base_url = "https://country-leaders.onrender.com"
        self.country_endpoint = "/countries"
        self.leaders_endpoint = "/leaders"
        self.cookies_endpoint = "/cookie"

        # Internal data
        self.leaders_data = {}  # stores leaders per country
        self.cookie = self.refresh_cookie()  # sets the initial cookie

        # Single session for all Wikipedia requests
        self.session = requests.Session()

    def refresh_cookie(self) -> dict:
        """Fetch a new cookie from the API."""
        resp = requests.get(self.base_url + self.cookies_endpoint)
        cookie_header = resp.headers.get("Set-Cookie")
        if cookie_header:
            name, value = cookie_header.split(";", 1)[0].split("=", 1)
            return {name: value}
        else:
            raise Exception("No Set-Cookie header found")

    def get_countries(self) -> list:
        """Retrieve the list of countries."""
        # resp = requests.get(self.base_url + self.country_endpoint, cookies=self.cookie)
        resp = self.session.get(self.base_url + self.country_endpoint, cookies=self.cookie)

        if resp.status_code == 403:
            self.cookie = self.refresh_cookie()
            # resp = requests.get(self.base_url + self.country_endpoint, cookies=self.cookie)
            resp = self.session.get(self.base_url + self.country_endpoint, cookies=self.cookie)

        return resp.json()

    # def get_leaders(self, country: str) -> None:
    def get_leaders(self, country, use_multiprocessing=False):
        """Fetch leaders for a specific country and store them in leaders_data."""
        url = f"{self.base_url}{self.leaders_endpoint}?country={country}"
        # resp = requests.get(url, cookies=self.cookie)
        resp = self.session.get(url, cookies=self.cookie)

        if resp.status_code == 403:
            self.cookie = self.refresh_cookie()
            # resp = requests.get(url, cookies=self.cookie)

        if resp.status_code == 200:
            leaders = resp.json()

            # Multiprocessing enabled?
            if use_multiprocessing:
                with Pool(cpu_count()) as pool:
                    leaders = pool.map(fetch_summary_for_leader, leaders)
            else:
                # Fallback: sequential summary fetching
                for leader in leaders:
                    url = leader.get("wikipedia_url", "")
                    leader["summary"] = self.get_first_paragraph(url)

            self.leaders_data[country] = leaders

    def get_first_paragraph(self, wikipedia_url: str) -> str:
        """Scrape the first meaningful paragraph from a Wikipedia page."""
        print(f"Fetching: {wikipedia_url}")
        try:
            response = self.session.get(wikipedia_url, timeout=10)
            response.raise_for_status()
        except Exception as e:
            print(f"Error: {e}")
            time.sleep(2)
            try:
                response = self.session.get(wikipedia_url, timeout=10)
            except Exception as e:
                print(f"Retry failed: {e}")
                return None

        soup = BeautifulSoup(response.text, "html.parser")
        paragraphs = soup.find_all("p")
        for p in paragraphs:
            text = p.get_text().strip()
            if text and not text.lower().startswith("coordinates"):
                # Basic cleaning
                clean_text = re.sub(r"\[\d+\]|—|–|→|<.*?>|\(.*?\)|/|pronunciation:.*|citation needed", "", text, flags=re.IGNORECASE)
                return re.sub(r"\s+", " ", clean_text).strip()
        return ""

    def to_json_file(self, filepath: str) -> None:
        """Save the leaders_data to a JSON file."""
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(self.leaders_data, f, ensure_ascii=False, indent=2)


    def to_csv_file(self, filepath: str) -> None:
        """Save the leaders_data to a CSV file (flattened structure)."""
        with open(filepath, "w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=[
                "country", "id", "first_name", "last_name", "birth_year", "wikipedia_url", "summary"
            ])
            writer.writeheader()
            for country, leaders in self.leaders_data.items():
                for leader in leaders:
                    row = {
                        "country": country,
                        "id": leader.get("id", ""),
                        "first_name": leader.get("first_name", ""),
                        "last_name": leader.get("last_name", ""),
                        "birth_year": leader.get("birth_year", ""),
                        "wikipedia_url": leader.get("wikipedia_url", ""),
                        "summary": leader.get("summary", "")
                    }
                    writer.writerow(row)

