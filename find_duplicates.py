'''
Short script to check for duplicate Titles in the game info files that we scraped data and saved to csv files. This will assist in cleaning up the files due to the duplicate records due to pricecharting having multiple UPC's on some game information pages.
'''

import pandas as pd
from pathlib import Path
from datetime import datetime

# Global for filename/location:
REL_FILE_PATH = Path(__file__, "../").resolve()

# Console Name:
CONSOLE = "gameboy"

# Global for the console path to be checking for duplicates.
CONSOLE_PATH = REL_FILE_PATH.joinpath(
    f"Consoles/2023_10_22-{CONSOLE}-Game_List.csv")


# Read in the game info csv file using pandas:
console_games_list = pd.read_csv(
    CONSOLE_PATH, lineterminator="\n", encoding="utf-8")

# Find duplicated items in the "Title" column and save into separate DF:
duplicates_df = console_games_list[console_games_list.duplicated(
    ["PC_ID"], keep=False)]

# Save the duplicate items into a csv file:
# duplicates_df.to_csv(REL_FILE_PATH.joinpath(
#     f"{CONSOLE}-Duplicates.csv"), lineterminator="\n", index=False)

console_games_list.drop_duplicates(subset=["PC_ID"], inplace=True)
console_games_list.replace(to_replace="none", value="Unknown", inplace=True)
# Tried doublequote=False, escapechar="\\" but didn't work gotta go back and scrape with those too.
console_games_list.to_csv(REL_FILE_PATH.joinpath(
    f"./Duplicates/{datetime.today().strftime('%Y_%m_%d')}-{CONSOLE}-Duplicates_Dropped.csv"), lineterminator="\n", index=False, encoding="utf-8")
