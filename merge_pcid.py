'''
Script to merge files based on UPC or PC_ID (e.g., Merge game info 
csv file with price csv file).
'''

import os
import pandas as pd
from pathlib import Path
from scraper_helper import Scraper
from datetime import datetime

# List of Consoles:
CONSOLE = ["Gameboy", "Gameboy Advance", "NES", "Super Nintendo",
           "Nintendo 64", "Sega Game Gear", "Nintendo 3DS"]

### ----- BEGIN CONSTANTS ----- ###
CONSOLE = "Wii"
REL_FILE_PATH = Path(__file__, "../").resolve()
# MY_COLLECTION_PATH = REL_FILE_PATH.joinpath(
#     "./My_Collection/2023_09_30-iCollect Everything Collection.csv")
COMBINED_GAME_INFO = REL_FILE_PATH.joinpath(
    "2023_11_16-Combined-Game_Info.csv")
COMBINED_PRICES = REL_FILE_PATH.joinpath("2023_11_15-Combined_Prices.csv")
### ----- END CONSTANTS ----- ###

# Read in csv files to be merged:
# my_collection = pd.read_csv(
#     MY_COLLECTION_PATH, usecols=["Platform", "Title", "Barcode"], index_col=False, lineterminator="\n", encoding="utf-8")
combined_games_list = pd.read_csv(COMBINED_GAME_INFO, dtype={
                                  "PC_ID": str}, index_col=False, lineterminator="\n", encoding="utf-8")
combined_price_list = pd.read_csv(COMBINED_PRICES, dtype={
                                  "PC_ID": str}, index_col=False, lineterminator="\n", encoding="utf-8")

# Create DataFrame which only includes the CONSOLE I want to view prices for:
##### ----- ONLY USE THIS WHEN PERFORMING MERGE ACTIONS WITH MY COLLECTION ----- #####
# my_collection.query(f"Platform == '{CONSOLE}'", inplace=True)
# my_collection.rename(columns={"Barcode": "UPC"}, inplace=True)
# wii_price_list.rename(columns={"PC_ID": "PriceCharting_ID"}, inplace=True)
# my_collection["Barcode"] = pd.to_numeric(
#     my_collection["Barcode"]).astype(float)
# my_collection = my_collection.convert_dtypes()

# Merge my personal collection with a particular console's game list:
# merged_with_upc = pd.merge(
#     my_collection, wii_games_list, on="UPC", how="left")

# print(my_collection[["Title", "UPC"]])
# print(merged_with_upc.dtypes)
# print(merged_with_upc[["Title", "UPC", "PriceCharting_ID"]])
# print(merged_with_upc)

# merged_with_pc_id = pd.merge(
#     merged_with_upc, wii_price_list, on="PC_ID", how="left")

# print(merged_with_pc_id)
# merged_with_upc.to_csv(REL_FILE_PATH.joinpath(

#     f"./Prices/{CONSOLE}-Merged_With_UPC.csv"), lineterminator="\n", index=False, encoding="utf-8")
##### ----- ONLY USE THIS WHEN PERFORMING MERGE ACTIONS WITH MY COLLECTION ----- #####

##### ----- BEGIN MERGE COMBINED GAME INFO AND COMBINED PRICE CSV'S ----- #####
merged_with_pc_id = pd.merge(
    combined_games_list, combined_price_list, on="PC_ID", how="left")
print(merged_with_pc_id)
##### ----- END MERGE COMBINED GAME INFO AND COMBINED PRICE CSV'S ----- #####

# Write combined merged info and price DataFrame to .csv:
##### ----- MERGED USING PC_ID IN THE "create_sql.py" FILE ----- #####
# merged_with_pc_id.to_csv(f"{datetime.today().strftime('%Y_%m_%d')}-Combined-Game_Info-TEST.csv",
#                          lineterminator="\n", index=False, encoding="utf-8")
##### ----- MERGED USING PC_ID IN THE "create_sql.py" FILE ----- #####

##### ----- BEGIN OLDER STUFF FROM MERGING PERSONAL COLLECTION ----- #####
# Save DataFrame with all game pricing info for my collection to a csv file:
# merged_with_pc_id = pd.DataFrame()
# merged_with_pc_id.to_csv(REL_FILE_PATH.joinpath(
#     f"./Prices/{Scraper.get_string_date_underscores(Scraper)}-{CONSOLE}-Collection_Price_List.csv"), lineterminator="\n", index=False, encoding="utf-8")
##### ----- END OLDER STUFF FROM MERGING PERSONAL COLLECTION ----- #####

##### ----- BEGIN MESSING AROUND WITH FILDERS AND .loc ----- #####
# wii_games_list.where(
#     cond=my_collection["UPC"] == wii_games_list["UPC"], inplace=True)
# print(wii_games_list.loc[filt, ["Title", "UPC"]])
# print(wii_games_list[["Title", "UPC"]])
##### ----- END MESSING AROUND WITH FILDERS AND .loc ----- #####
