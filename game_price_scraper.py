'''
Program to scrape average eBay sold game price data for loose, CIB, and new versions of game and save to csv for that day's date. The console that is being scraped can be changed by changing the CONSOLE constant.
'''

import pandas as pd
# from selenium import webdriver
from selenium.webdriver.common.by import By
from scraper_helper import Scraper
# from selenium.webdriver import ActionChains
# from selenium.webdriver import Keys
from datetime import datetime
# from pathlib import Path

### ----- LIST OF CONSOLE NAMES ----- ###
CONSOLE_LIST = ["gameboy-advance", "gameboy", "nes",
                "nintendo-3ds", "nintendo-64", "sega-game-gear", "super-nintendo"]
TODAY = datetime.today().strftime("%Y-%m-%d")
### ----- ENDLIST OF CONSOLE NAMES ----- ###


### -----BEGIN CONSTANTS----- ###
# Create a path to where we are running this script from to find data files:
# REL_FILE_PATH = Path(__file__, "../").resolve()
# URL with filtered search for Wii game on price charting site:
# URL = f"https://www.pricecharting.com/console/{CONSOLE}?sort=name&genre-name=&exclude-variants=false&exclude-hardware=true&when=none&release-date=2023-10-22&show-images=true"

# Constant to use for which console we want to search for:
CONSOLE = "sega-game-gear"
### -----END CONSTANTS----- ###


# Scrape price data using Selenium into a dictionary and
# create DataFrame with that dictionary and return DataFrame:
def scrape_console_prices(curr_console: str) -> pd.DataFrame:
    '''Create Scraper object for CONSOLE to scroll to bottom of the page.
    Create webdriver, set up Chrome options using scraper_helper.py'''
    console_scraper = Scraper(curr_console)
    console_scraper.scroll_to_bottom()

    # Create list for game prices:
    game_price_list = []

    # Obtain all row data in the #games_table on the website:
    game_data_row = console_scraper.driver.find_elements(
        By.CSS_SELECTOR, "#games_table tbody tr")

    # Loop through each row and extract image, title, loose price, cib_price, and new_price:
    i = 0
    for row in game_data_row:
        # print(f"Scraping row #{i:04}.")

        try:
            price_charting_id = row.get_attribute("data-product")
            # Find the URL of the thumbnail view of a game image:
            image_src = row.find_element(
                By.CSS_SELECTOR, "td div img.photo").get_property("src")
            # title = row.find_element(By.CSS_SELECTOR, "td.title").text
            loose_price = str(row.find_element(
                By.CSS_SELECTOR, "td.used_price").text).replace("$", "")
            cib_price = str(row.find_element(
                By.CSS_SELECTOR, "td.cib_price").text).replace("$", "")
            new_price = str(row.find_element(
                By.CSS_SELECTOR, "td.new_price").text).replace("$", "")
            # loose_price.replace(",", "")
            # cib_price.replace(",", "")
            # new_price.replace(",", "")
            print(
                f"Scraping row #{i:04}: {loose_price}, {cib_price}, {new_price}.")
        except Exception as e:
            print(f"You had an error: {e}.")

        ### DEBUG PRINT ###
        # print(
        # f"Title: {title} | Loose Price: {loose_price} | CIB Price: {cib_price} | New Price: {new_price}")
        ### DEBUG PRINT ###
        # Add data for each game to game_dict dictionary:
        game_price_list.append({
            "PC_ID": price_charting_id,
            # "Title": title,
            "Loose_Price": loose_price,  # .replace(",", ""),
            "CIB_Price": cib_price,  # .replace(",", ""),
            "New_Price": new_price,  # .replace(",", ""),
            "Image_URL": image_src,
        })
        i += 1

    # Close the webdriver browser:
    console_scraper.close_webdriver()

    game_df = pd.DataFrame(game_price_list, index=None)
    print(game_df.head())
    return game_df


##### ----- BEGIN CODE TO CONCATENATE DATAFRAMES ----- #####
df_prices_combined = pd.DataFrame()
for console in CONSOLE_LIST:
    df_temp = scrape_console_prices(curr_console=console)
    df_prices_combined = pd.concat(
        [df_prices_combined, df_temp], ignore_index=True)
print(df_prices_combined)
##### ----- END CODE TO CONCATENATE DATAFRAMES ----- #####

### ----- BEGIN CODE TO ADD DATE AND REMOVE COMMAS ----- ###
# Add column in DataFrame for the current CONSOLE:
df_prices_combined.insert(0, "Price_Date", TODAY)

# Remove commas from price Columns:
# NOTE: DONE ABOVE WHILE APPENDING TO game_price_list DICTIONARY NOTE #
# df_prices_combined[["Loose_Price", "CIB_Price", "New_Price"]].replace
df_prices_combined["Loose_Price"] = df_prices_combined["Loose_Price"].str.replace(
    ",", "")
df_prices_combined["CIB_Price"] = df_prices_combined["CIB_Price"].str.replace(
    ",", "")
df_prices_combined["New_Price"] = df_prices_combined["New_Price"].str.replace(
    ",", "")

# Fill all empty cells of DataFrame with "NULL":
df_prices_combined.fillna("NULL", inplace=True)
### ----- END CODE TO ADD DATE AND REMOVE COMMAS ----- ###

# Save DataFrame with all price data to a csv file:
df_prices_combined.to_csv(f"./Combined/{TODAY}-Combined_Prices.csv",
                          lineterminator="\n", index=False, encoding="utf-8")
# Scraper.save_to_csv(
#     df=df_prices_combined, dir_name="./Prices", file_name="Combined_Price_List")
print(df_prices_combined)
print("Finished Scraping and saving to csv file.")

##### ----- BEGIN EXTRA TESTING STUFF ----- #####
# game_df.to_csv(REL_FILE_PATH.joinpath(
#     f"./Prices/{get_string_date_underscores()}-{CONSOLE.title()}-Price_List.csv"), lineterminator="\n", index=False, encoding="utf-8")

# print(game_dict)
# print()
# pprint.pprint(game_dict)

# element = driver.find_element(By.CSS_SELECTOR, "body")
##### ----- END EXTRA TESTING STUFF ----- #####

### WAS TRYING OUT USING ACTIONCHAIN TO HOLD END KEY TO SCROLL TO BOTTOM OF PAGE BUT DIDN'T WORK ###
# Create ActionChain to scroll to the bottom to make all games visible:
# action_chain = ActionChains(driver)
# action_chains.scroll(x: int, y: int, delta_x: int, delta_y: int, duration: int = 0, origin: str = 'viewport').perform()
# action_chain.send_keys_to_element(element, Keys.END)
# action_chain.key_down(Keys.END, element)
# action_chain.perform()
### WAS TRYING OUT USING ACTIONCHAIN TO HOLD END KEY TO SCROLL TO BOTTOM OF PAGE BUT DIDN'T WORK ###
