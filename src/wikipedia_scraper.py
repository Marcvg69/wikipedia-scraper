import requests
from bs4 import BeautifulSoup
import json
import re
import time

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
        resp = requests.get(self.base_url + self.country_endpoint, cookies=self.cookie)
        if resp.status_code == 403:
            self.cookie = self.refresh_cookie()
            resp = requests.get(self.base_url + self.country_endpoint, cookies=self.cookie)
        return resp.json()

    def get_leaders(self, country: str) -> None:
        """Fetch leaders for a specific country and store them in leaders_data."""
        url = f"{self.base_url}{self.leaders_endpoint}?country={country}"
        resp = requests.get(url, cookies=self.cookie)
        if resp.status_code == 403:
            self.cookie = self.refresh_cookie()
            resp = requests.get(url, cookies=self.cookie)

        if resp.status_code == 200:
            leaders = resp.json()
            for leader in leaders:
                url = leader.get("wikipedia_url")
                leader["summary"] = self.get_first_paragraph(url) if url else None
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
