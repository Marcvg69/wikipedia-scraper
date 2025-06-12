# Wikipedia Scraper 

- Repository: `wikipedia-scraper`
- Type: `Consolidation`
- Duration: `3 days`
- Deadline: `13/06/2025 4:30 PM`
- Team: `solo`
- Author: Marc Van Goolen

This project demonstrates how to collect structured and semi-structured data from an open API and enrich it with data scraped from Wikipedia.

You will retrieve historical political leaders for several countries using a REST API, then scrape their biographies using BeautifulSoup. Finally, the data is saved locally for further use in data science workflows.



## Prerequisites

Make sure you have **Python 3.12.10** installed.

- Download from: https://www.python.org/downloads/release/python-31210/
- Add Python to your system PATH.

>  This project was tested with Python 3.12.10. Other versions may cause compatibility issues (e.g., with pandas or ipykernel).


## Environment Setup

This project uses a virtual environment (`.myvenv`) to isolate its dependencies.

### Why use a virtual environment?

- Prevents conflicts between Python packages
- Ensures consistency across machines
- Keeps your system Python clean

### Setup Instructions

install the requirements :
pip install -r requirements.txt


## Running the Application

You can run the project either via **Jupyter Notebook** or as a **standalone script**.

### Run in Notebook Mode

1. Open `wikipedia_scraper.ipynb` in **VS Code**
2. Select the `.myvenv` kernel
3. Run each cell step by step


### Run in Script Mode (recommended)

This mode uses `main.py` to launch the full scraping pipeline. It requests the user 
to run multi-processing mode y/n. After scraping is completed, it prompts the user 
where to store the output (json or csv file)


## Technologies Used

- **Python 3.12.10**  
  The main programming language used for building the entire scraping pipeline.

- **`requests`**  
  For sending HTTP requests to APIs and web pages to retrieve data.

- **`beautifulsoup4`**  
  Used for parsing and navigating HTML content from Wikipedia pages.

- **`pandas`**  
  Powerful library for manipulating and organizing data into structured DataFrames.

- **`json`**  
  Native Python module to serialize and deserialize JSON data (used for saving final output).

- **`re` (regex)**  
  Python's built-in regular expressions module for text pattern matching and data cleaning.

- **`multiprocessing`** *(optional)*  
  For parallelizing API requests or processing multiple items simultaneously to improve performance.

## Branch Strategy

This repository is structured using two branches:
- `main`: Contains the required MVP with all mandatory features.
- `feature/advanced`: Contains nice-to-have additions such as `Session()`, regex text cleaning, and multithreading.

This approach ensures a clean separation between baseline functionality and performance/UX improvements.

## Feature Completion Table (**this is not yet accurate - implementation pending**)

## ✅ Feature Checklist

| Feature                                                                                                    | Required Type  | Implemented |
|------------------------------------------------------------------------------------------------------------|----------------|-------------|
| Create a virtual environment using `venv`                                                                  | Mandatory      | ✅ Yes       |
| Install required packages via `requirements.txt`                                                           | Mandatory      | ✅ Yes       |
| Call an external API using `requests`                                                                      | Mandatory      | ✅ Yes       |
| Handle cookies to access the API                                                                           | Mandatory      | ✅ Yes       |
| Retrieve list of countries via `/countries` endpoint                                                       | Mandatory      | ✅ Yes       |
| Retrieve list of leaders via `/leaders` endpoint                                                           | Mandatory      | ✅ Yes       |
| Retrieve and parse Wikipedia bio from `wikipedia_url`                                                      | Mandatory      | ✅ Yes       |
| Extract first paragraph using `BeautifulSoup`                                                              | Mandatory      | ✅ Yes       |
| Save results in a structured JSON file                                                                     | Mandatory      | ✅ Yes       |
| Create a custom exception with proper handling                                                             | Mandatory      | ✅ Yes       |
| Provide a Jupyter notebook (`wikipedia_scraper.ipynb`) that shows the workflow                            | Mandatory      | ✅ Yes       |
| Refactor into a Python module `leaders_scraper.py` with OOP design (`WikipediaScraper` class)             | Mandatory      | ✅ Yes       |
| Provide a `main.py` script to run the scraper                                                              | Mandatory      | ✅ Yes       |
| Create a GitHub repository with meaningful name and clean folder structure                                 | Mandatory      | ✅ Yes       |
| Write a clear README with description, installation, usage, visuals, etc.                                  | Mandatory      | ✅ Yes       |

### WikipediaScraper Class Implementation

| Feature                                                                                                    | Required Type  | Implemented |
|------------------------------------------------------------------------------------------------------------|----------------|-------------|
| Attribute: `base_url`                                                                                      | Mandatory      | ✅ Yes       |
| Attribute: `country_endpoint`                                                                              | Mandatory      | ✅ Yes       |
| Attribute: `leaders_endpoint`                                                                              | Mandatory      | ✅ Yes       |
| Attribute: `cookies_endpoint`                                                                              | Mandatory      | ✅ Yes       |
| Attribute: `leaders_data`                                                                                  | Mandatory      | ✅ Yes       |
| Attribute: `cookie`                                                                                        | Mandatory      | ✅ Yes       |
| Method: `refresh_cookie()`                                                                                 | Mandatory      | ✅ Yes       |
| Method: `get_countries()`                                                                                  | Mandatory      | ✅ Yes       |
| Method: `get_leaders(country)`                                                                             | Mandatory      | ✅ Yes       |
| Method: `get_first_paragraph(wikipedia_url)`                                                               | Mandatory      | ✅ Yes       |
| Method: `to_json_file(filepath)`                                                                           | Mandatory      | ✅ Yes       |

### Nice-to-have / Advanced Features

| Feature                                                                                                    | Required Type  | Implemented  |
|------------------------------------------------------------------------------------------------------------|----------------|--------------|
| Use `requests.Session()` instead of `requests.get()`                                                       | Optional       | ✅ Yes       |
| Implement CSV export option                                                                                | Optional       | ✅ Yes       |
| Speed up scraping using multithreading (e.g. with `ThreadPoolExecutor`)                                    | Optional       | ✅ Yes       |
| Use regex to clean text data from Wikipedia                                                                | Optional       | ✅ Yes       |
| Organize must-have and nice-to-have code in separate Git branches (partially done, as the branching strategy was applied later in the process)           | Optional       | ✅ Yes       |

## License
This code is protected under the MIT license.

## Evaluation

| Criterion      | Indicator                                                    | Yes/No |
| -------------- | ------------------------------------------------------------ | ------ |
| 1. Is complete | Executes whithout errors                                     |        |
|                | Stores the correct information from the API in the file      |        |
| 2. Is correct  | The code is well typed                                       |        |
|                | Good usage of OOP                                            |        |
| 3. Is great    | Possibility to store output as a CSV file                    |        |
|                | Correct usage of `Session()`                                 |        |
|                | Multi-processing                                             |        |

## You got this!
