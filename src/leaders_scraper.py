import requests
from bs4 import BeautifulSoup
import re
import json
import time

def get_first_paragraph(wikipedia_url, session):
    print(wikipedia_url)
    try:
        response = session.get(wikipedia_url, timeout=10)
        if response.status_code != 200:
            raise Exception(f"Request failed with status {response.status_code}")
    except Exception as e:
        print(f"Error fetching {wikipedia_url}: {e}")
        time.sleep(2)
        try:
            response = session.get(wikipedia_url, timeout=10)
        except Exception as e:
            print(f"Retry failed: {e}")
            return None

    soup = BeautifulSoup(response.text, 'html.parser')
    paragraphs = soup.find_all('p')
    first_paragraph = ""
    for p in paragraphs:
        text = p.get_text()
        if text.strip() and not text.lower().startswith("coordinates"):
            first_paragraph = text
            break

    clean_paragraph = re.sub(r"\[\d+\]|\(.*?\)|<.*?>|\/|—|–|†|→|pronunciation:.*|citation needed", "", first_paragraph, flags=re.IGNORECASE)
    clean_paragraph = re.sub(r"\s+", " ", clean_paragraph)

    return clean_paragraph.strip()

def get_leaders():
    root_url = "https://country-leaders.onrender.com"
    cookie_url = f"{root_url}/cookie"
    countries_url = f"{root_url}/countries"
    leaders_url = f"{root_url}/leaders"

    def fetch_cookie():
        resp = requests.get(cookie_url)
        cookie_header = resp.headers.get("Set-Cookie")
        if cookie_header:
            cookie_name, cookie_value = cookie_header.split(";", 1)[0].split("=", 1)
            return {cookie_name: cookie_value}
        else:
            raise Exception("No Set-Cookie header found in response.")

    cookies = fetch_cookie()

    response = requests.get(countries_url, cookies=cookies)
    if response.status_code == 403:
        cookies = fetch_cookie()
        response = requests.get(countries_url, cookies=cookies)
    countries = response.json()

    leaders_per_country = {}

    with requests.Session() as session:
        for country in countries:
            response = requests.get(f"{leaders_url}?country={country}", cookies=cookies)
            if response.status_code == 403:
                cookies = fetch_cookie()
                response = requests.get(f"{leaders_url}?country={country}", cookies=cookies)
            if response.status_code != 200:
                print(f"Failed to get leaders for {country}")
                continue

            leaders = response.json()
            for leader in leaders:
                url = leader.get("wikipedia_url")
                leader["summary"] = get_first_paragraph(url, session) if url else None

            leaders_per_country[country] = leaders

    return leaders_per_country

def save(leaders_per_country):
    with open("leaders.json", "w", encoding="utf-8") as f:
        json.dump(leaders_per_country, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    leaders_per_country = get_leaders()
    save(leaders_per_country)
    print("Saved to leaders.json")
