'''
Testing out different BeautifulSoup methods of finding game information
on gaming websites to scrape game details to store and compare against 
personal collection. Scrapes game information from Price Charting 
with help of scraper_helper.py.
'''

import requests
import pandas as pd
from datetime import datetime
from scraper_helper import Scraper
from bs4 import BeautifulSoup
from pathlib import Path

### ----- LIST OF CONSOLE NAMES ----- ###
# ["nes", "super-nintendo", "nintendo-64", "gameboy" "gameboy-advance", "sega-game-gear", "nintendo-ds", "nintendo-3ds"]
### ----- ENDLIST OF CONSOLE NAMES ----- ###

# Create a path to where we are running this script from to find data files:
REL_FILE_PATH = Path(__file__, "../").resolve()
CONSOLE = "wii"
WEBSITE = "https://www.pricecharting.com"
# URL = f"https://www.pricecharting.com/console/{CONSOLE}?sort=name&genre-name=&exclude-variants=false&exclude-hardware=true&when=none&release-date=2023-09-21&show-images=true"

# Create Scraper object for CONSOLE to scroll to bottom of the page.
console_scraper = Scraper(CONSOLE)
console_scraper.scroll_to_bottom()
html = console_scraper.get_page_source()
console_scraper.close_webdriver()

# Create soup out of html scraped above:
soup = BeautifulSoup(html, "html.parser")


### ----- TESTING WITH JUST FINDING ONE ELEMENT USING CSS SELECTORS ----- ###
# first_game_url = soup.select_one(
#     "#games_table tbody tr td.title a").get("href")
# first_game_title = soup.select_one(
#     "#games_table tbody tr td.title").getText().replace("\n", "")
### ----- END TESTING WITH JUST FINDING ONE ELEMENT USING CSS SELECTORS ----- ###

# List to hold dictionaries of the title and url of each game
games_list = []

# Get a list of all the td's in the game table with a class of "title":
game_rows = soup.select(selector="#games_table tbody tr td.title")

# Loop through all the td's with class "title" that were found and add the title and url as dict to # games_list
for row in game_rows:
    pc_id = row.get("title").strip()
    title = row.getText().replace("\n", "")
    url = f"{WEBSITE}{row.find(name='a').get('href')}"
    games_list.append({
        "PC_ID": pc_id,
        "Title": title,
        "URL": url
    })

print(len(games_list))

game_data = []
print("Scraping data...")
for i in range(0, len(games_list)):
    print(
        f"Scraping for game #{games_list[i]['PC_ID']}:\t {i:04}: {games_list[i]['Title']}")
    session_object = requests.Session()
    response = session_object.get(games_list[i]["URL"])
    # response.raise_for_status()
    game_soup = BeautifulSoup(response.text, "html.parser")
    date_string = game_soup.find(
        "td", itemprop="datePublished").getText(strip=True)

    # Test the date string to make sure it isn't empty:
    if (date_string == "none" or ""):
        release_date_string = None
    else:
        release_date_datetime = datetime.strptime(
            date_string, "%B %d, %Y")
        release_date_string = release_date_datetime.strftime("%Y-%m-%d")

    try:
        title = games_list[i]["Title"]
        esrb = game_soup.find(
            "td", itemprop="contentRating").getText(strip=True)
        publisher = game_soup.find(
            "td", itemprop="publisher").getText(strip=True)
        developer = game_soup.find("td", itemprop="author").getText(strip=True)
        genre = game_soup.find("td", itemprop="genre").getText(strip=True)
        upc = game_soup.find("td", itemprop="value").getText(strip=True)
        # pricecharting_id = game_soup.find(
        # "td", class_="title", string="PriceCharting ID:").findNextSibling().getText(strip=True)
        pricecharting_id = games_list[i]["PC_ID"]
        summary = game_soup.find(
            "td", itemprop="description").getText(strip=True)
        game_url = games_list[i]["URL"]
    except Exception as e:
        print(f"You had an exception {e}.")

    # Check if UPC has multiple values then tokenize and create new row in df by appending dictionaries for the same game multiple times with just the UPC being different:
    if ',' in upc:
        upc_list = upc.split(sep=",")
        print(upc_list)
        for code in upc_list:
            # print(code)
            game_data.append({
                "Title": title,
                "Release_Date": release_date_string,
                "ESRB": esrb,
                "Publisher": publisher,
                "Developer": developer,
                "Genre": genre,
                "UPC": code,
                "PC_ID": pricecharting_id,
                "Summary": summary,
                "URL": game_url,
            })
    else:
        game_data.append({
            "Title": title,
            "Release_Date": release_date_string,
            "ESRB": esrb,
            "Publisher": publisher,
            "Developer": developer,
            "Genre": genre,
            "UPC": upc,
            "PC_ID": pricecharting_id,
            "Summary": summary,
            "URL": game_url,
        })

# Create DataFrame to save data to CSV:
df = pd.DataFrame(game_data)
# Add column in DataFrame for the current CONSOLE:
df.insert(0, "Console", CONSOLE)
# df["UPC"].astype(str)
print(df.head())

# Save DataFrame with all game data to a csv file:
console_scraper.save_to_csv(
    df=df, dir_name="./Consoles", file_name="Game_List")
# df.to_csv(REL_FILE_PATH.joinpath(
#     f"./Consoles/{console_scrape.get_string_date_underscores()}-{console_scrape.get_console()}-Game_List.csv"), lineterminator="\n", index=False)

print("Finished Scraping and saving to csv file.")
