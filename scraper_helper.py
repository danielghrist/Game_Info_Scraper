'''
Helper module for scraping pages, with things like scrolling to bottom of page and initiating a webdriver, as well as creating a list of URLs to be looped through to scrape each page, and obtaining the html webpage source code for use with BeautifulSoup scraping.
'''

from selenium import webdriver
from selenium.webdriver.common.by import By
# from selenium.webdriver import ActionChains
# from selenium.webdriver import Keys
from datetime import datetime
from pathlib import Path
import time
import pandas as pd
from bs4 import BeautifulSoup

### -----BEGIN CONSTANTS----- ###
# Amount to pause between each scroll action:
SCROLL_PAUSE_TIME = 1
# Create a path to where we are running this script from to find data files:
REL_FILE_PATH = Path(__file__, "../").resolve()
# "true" if you want to exclude variants, "false" if you want to include them:
EXCLUDE_VARIANTS = "true"
EXCLUDE_HARDWARE = "true"
### -----END CONSTANTS----- ###


class Scraper:
    def __init__(self, console: str) -> None:
        '''
        Creates Scraper object with whatever console is passed in and creates the link needed to begin scraping as well as initializing a Chrome webdriver.
        '''
        self.__console = console.lower()
        self.__link = f"https://www.pricecharting.com/console/{self.__console}?sort=name&genre-name=&exclude-variants={EXCLUDE_VARIANTS}&exclude-hardware={EXCLUDE_HARDWARE}&when=none&release-date={self.get_string_date_dashes()}&show-images=true"
        self.driver = self.__init_webdriver(self.__link)

    def __init_webdriver(self, url: str) -> webdriver:
        '''
        Set webdriver options for detach in Chrome and initialize and return a Chrome webdriver from the given URL.
        '''
        # Get Chrome options and set up brower to not auto close:
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_experimental_option("detach", True)

        # Create webdriver:
        driver = webdriver.Chrome(options=chrome_options)
        driver.get(url=self.__link)
        return driver

    # Code to scroll to bottom of page using execute to execute JavaScript code:
    def scroll_to_bottom(self) -> None:
        '''
        Scroll to the bottom of the page to be certain all elements are loaded before scraping.
        '''
        # Initialize webdriver and options:
        # driver = self.__init_webdriver(self.url)

        # Get current scroll height
        last_height = self.driver.execute_script(
            "return document.body.scrollHeight")

        while True:
            # Scroll to bottom of current visible window:
            self.driver.execute_script(
                "window.scrollTo(0, document.body.scrollHeight);")

            # Wait for the page to load:
            time.sleep(SCROLL_PAUSE_TIME)

            # Calculate new scroll height and compare with last scroll height
            new_height = self.driver.execute_script(
                "return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height
        ### End scrolling to bottom of page ###

    # Save df with all game data to a csv file:
    def save_to_csv(self, df: pd.DataFrame, dir_name: str, file_name: str) -> None:
        '''
        Save the DataFrame passed in to a csv file with the name format:
        "dir_name/YYYY_MM_DD-CONSOLE-file_name.csv" with no index and "\n" line terminator.
        '''
        df.to_csv(REL_FILE_PATH.joinpath(
            f"{dir_name}/{self.get_string_date_underscores()}-{self.__console}-{file_name}.csv"), lineterminator="\n", index=False, encoding="utf-8")

    # Close the webdriver browser:
    def close_webdriver(self) -> None:
        '''Close the webdriver that was opened when object created to close browser window.'''
        self.driver.quit()

    # Return the html of a webpage for BeautifulSoup to use:
    def get_page_source(self) -> str:
        '''Returns the source code of the current webpage pointed to by self.driver.'''
        return self.driver.page_source

    # Get current date as a string in YYYY_MM_DD format:
    def get_string_date_underscores(self) -> str:
        '''Returns the current date in YYYY_MM_DD format.'''
        return datetime.today().strftime("%Y_%m_%d")

    # Get current date as a string in YYYY_MM_DD format:
    def get_string_date_dashes(self) -> str:
        '''Returns the current date in YYYY-MM-DD format.'''
        return datetime.today().strftime("%Y-%m-%d")

    # Return the current console system being scraped by this object:
    def get_console(self) -> str:
        '''Returns the platform being scraped.'''
        return self.__console

    #
    #
    #
    # game_price_list = []

    # # Obtain all row data in the #games_table on the website:
    # game_data_row = driver.find_elements(
    #     By.CSS_SELECTOR, "#games_table tbody tr")

    # # Loop through each row and extract image, title, loose price, cib_price, and new_price
    # for row in game_data_row:
    #     # Find the URL of the thumbnail view of a game image:
    #     image_src = row.find_element(
    #         By.CSS_SELECTOR, "td div img.photo").get_property("src")
    #     title = row.find_element(By.CSS_SELECTOR, "td.title").text
    #     loose_price = row.find_element(By.CSS_SELECTOR, "td.used_price").text
    #     cib_price = row.find_element(By.CSS_SELECTOR, "td.cib_price").text
    #     new_price = row.find_element(By.CSS_SELECTOR, "td.new_price").text

    #     # Add data as dictionary for each game to game price list:
    #     game_price_list.append({
    #         "image_link": image_src,
    #         "title": title,
    #         "loose_price": loose_price,
    #         "cib_price": cib_price,
    #         "new_price": new_price
    #     })

    #     game_df = pd.DataFrame(game_price_list)
    #     print(game_df)
    #     game_df.to_csv(
    #         f"{self.getStringDate()}-{self.__console.title()}-Price_List.csv")


# nes_scrape = Scraper("nes")
# nes_scrape.scroll_to_bottom()
# html = nes_scrape.get_page_source()
# print(html)
# nes_scrape.close_webdriver()
