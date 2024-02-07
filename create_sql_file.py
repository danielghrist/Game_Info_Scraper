'''
Creates a txt file which contains all the necessary SQL Statements to 
create the DataBase, Tables, and insert all relevant data. Also creates
a .csv file for use when debugging or testing.
'''

# NOTE: NEED TO MAKE A LOT OF THIS INTO FUNCTIONS TO KEEP IT DRY NOTE #

import os
import pandas as pd
import numpy as np
# from sqlalchemy import create_engine, Connection, text, types
from datetime import datetime
from pathlib import Path
import sql_strings

### ----- BEGIN GLOBAL VARIABLES ----- ###
# Schema to create:
SCHEMA = "Retro_Games"
# List of the Table names that need to be created:
TABLE_NAMES = ["Publisher", "Developer", "Console", "Genre",
               "Price", "User", "Game", "Publishes", "Develops", "Collection"]
# List of Consoles:
CONSOLE = ["Gameboy", "Gameboy Advance", "NES", "Super Nintendo",
           "Nintendo 64", "Sega Game Gear", "Nintendo 3DS"]
TODAY = datetime.today().strftime("%Y-%m-%d")
REL_FILE_PATH = Path(__file__, "../").resolve()
# Name of combined pricing file for all consoles:
COMBINED_PRICES = REL_FILE_PATH.joinpath(
    "./Combined/2023_11_15-Combined_Prices.csv")
# Name of Directory for updated Summary column files:
SUMMARIES_DIR = "./Summaries_Added/"
# The relative path to the game data files with duplicates removed:
DUPLICATES_DIR = "./Duplicates/"
### ----- END GLOBAL CONSTANTS ----- ###

# TODO: Make this into a function:
### ----- BEGIN READING IN .csv FILES FOR MERGING ----- ###
combined_price_list = pd.read_csv(COMBINED_PRICES, dtype={
                                  "PC_ID": str}, index_col=False, lineterminator="\n", encoding="utf-8")
### ----- END READING IN .csv FILES FOR MERGING ----- ###


# TODO: THIS WAS ONLY NEEDED TO COMBINE SUMMARY UPDATES, NEED TO CREATE ONE
# TODO: COMBINED FILE WITH THE UPDATED SUMMARIES THEN CAN GET RID OF THIS:
### ----- BEGIN COMBINING CORRECTED SUMMARY CSV FILES ----- ###
# Create one combined file for all consoles:
# List all files from the directory:
# file_list = os.listdir(file_path)

# Append all Duplicate PC_ID removed .csv files together. Loop
# through all files, read file, append to combined DataFrame:
df_summaries_combined = pd.DataFrame()
for file in os.listdir(SUMMARIES_DIR):
    summaries_csv_fp = f"{SUMMARIES_DIR}{file}"
    df_summaries_temp = pd.read_csv(summaries_csv_fp, usecols=["PC_ID", "Summary"], dtype={
        "PC_ID": str}, index_col=False, lineterminator="\r", encoding="utf-8", encoding_errors="ignore")
    df_summaries_combined = pd.concat(
        [df_summaries_combined, df_summaries_temp], ignore_index=True)
### ----- BEGIN COMBINING CORRECTED SUMMARY CSV FILES ----- ###

# TODO: MAKE THIS INTO A FUNCTION:
### ----- BEGIN COMBINING GAME NON-DUPLICATE PC_ID CSV FILES ----- ###
# Create one combined file for all consoles:
# List all files from the directory:
# file_list = os.listdir(file_path)
# print(file_list) # DEBUGGING

# Append all Duplicate PC_ID removed .csv files together. Loop
# through all files, read file, append to combined DataFrame:
df_info_combined = pd.DataFrame()
for file in os.listdir(DUPLICATES_DIR):
    game_csv_fp = f"{DUPLICATES_DIR}{file}"
    df_temp = pd.read_csv(
        game_csv_fp, dtype={"UPC": str, "PC_ID": str}, index_col=False,  lineterminator="\n", encoding="utf-8")
    df_info_combined = pd.concat(
        [df_info_combined, df_temp], ignore_index=True)
# print(df_info_combined) # DEBUGGING
### ----- END COMBINING GAME NON-DUPLICATE PC_ID CSV FILES ----- ###


### ----- BEGIN MERGE COMBINED SUMMARY, GAME INFO, AND PRICE CSV'S ----- ###
# Inserting the Date column into the combined price file as I forgot
# include that column when originally scraping prices and merging:
combined_price_list.insert(0, "Price_Date", "2023-11-15")
df_data_combined = pd.merge(
    df_info_combined, combined_price_list, on="PC_ID", how="left")
df_data_combined = pd.merge(
    df_data_combined, df_summaries_combined, on="PC_ID", how="left")
# df_data_combined["Summary"] = df_summaries_combined["Summary"]

print(df_data_combined)
### ----- END MERGE COMBINED SUMMARY, GAME INFO, AND PRICE CSV'S ----- ###


# Generate ID's in new column to be used as Keys for unique values:
def create_ids(df: pd.DataFrame, old_col: str, new_col: str) -> None:
    '''Create unique IDs for a column within a DataFrame'''
    unique_ids = df[f"{old_col}"].unique()
    unique_ids.sort()
    unique_ids = pd.Series(
        np.arange(start=1, stop=len(unique_ids) + 1), unique_ids)
    df[f"{new_col}"] = df[f"{old_col}"].apply(unique_ids.get)


# Create unique Console_ID column in df_data_combined DataFrame:
create_ids(df=df_data_combined, old_col="Console", new_col="Console_ID")

# Create unique Genre_ID column in df_data_combined DataFrame:
create_ids(df=df_data_combined, old_col="Genre", new_col="Genre_ID")

# Create unique ESRB_ID column in df_data_combined DataFrame:
create_ids(df=df_data_combined, old_col="ESRB", new_col="ESRB_ID")

# Create unique Publisher_ID column in df_data_combined DataFrame:
create_ids(df=df_data_combined, old_col="Publisher", new_col="Publisher_ID")

# Create unique Developer_ID column in df_data_combined DataFrame:
create_ids(df=df_data_combined, old_col="Developer", new_col="Developer_ID")


print(df_data_combined[["Console", "Console_ID",
      "Publisher", "Publisher_ID", "Developer", "Developer_ID", "Genre", "Genre_ID", "Loose_Price", "CIB_Price", "New_Price"]].head())

##### ----- WAS TESTING STUFF OUT, NOT NEEDED RIGHT NOW ----- #####
# for index, row in df_data_combined.iterrows():
#     print(index, row)

# for publisher in publishers:
#     print(publisher)
##### ----- END TESTING STUFF OUT, NOT NEEDED RIGHT NOW ----- #####

##### ----- Create Test file with SQL lines needed to create Database and some Tables ----- #####
### ----- BEGIN CREATE SCHEMA AND TABLES SQL ----- ###
output_string = ""
output_string += sql_strings.header_comment
output_string += sql_strings.create_schema
output_string += sql_strings.user_table
output_string += sql_strings.console_table
output_string += sql_strings.genre_table
output_string += sql_strings.esrb_table
output_string += sql_strings.price_table
output_string += sql_strings.publisher_table
output_string += sql_strings.developer_table
output_string += sql_strings.game_table
output_string += sql_strings.publishes_table
output_string += sql_strings.develops_table
output_string += sql_strings.collection_table
output_string += sql_strings.collected_table
### ----- END CREATE SCHEMA AND TABLES SQL ----- ###

# Dummy input data for User Table Insert statements:
output_string += sql_strings.user_inserts

# Insert statements for Console Table:
unique_consoles = df_data_combined["Console"].unique()
# unique_console_ids = df_data_combined["Console_ID"].unique()
output_string += "\n/* Insert Console row data: */\nSTART TRANSACTION;\n"
for console in sorted(unique_consoles):
    if console == "nes" or console == "super-nintendo" or console == "nintendo-64":
        console_type = "Home Console"
    else:
        console_type = "Handheld Console"

    output_string += f"INSERT INTO Console(Console_Name, Console_Type) VALUES(\"{console.title()}\", \"{console_type}\");\n"
output_string += sql_strings.commit

# Insert statements for Genre Table:
unique_genre = df_data_combined["Genre"].unique()
output_string += "\n/* Insert Genre row data: */\nSTART TRANSACTION;\n"
for genre in sorted(unique_genre):
    output_string += f"INSERT INTO Genre(Genre_Name) VALUES(\"{genre}\");\n"
output_string += sql_strings.commit

# Insert statements for ESRB Table:
unique_esrb = df_data_combined["ESRB"].unique()
output_string += "\n/* Insert ESRB row data: */\nSTART TRANSACTION;\n"
for esrb in sorted(unique_esrb):
    output_string += f"INSERT INTO ESRB(ESRB_Name) VALUES(\"{esrb}\");\n"
output_string += sql_strings.commit

# Insert statements for Price Table:
df_data_combined["Loose_Price"].fillna("NULL", inplace=True)
df_data_combined["CIB_Price"].fillna("NULL", inplace=True)
df_data_combined["New_Price"].fillna("NULL", inplace=True)
output_string += "\n/* Insert Price row data: */\nSTART TRANSACTION;\n"
for index, row in df_data_combined.iterrows():
    output_string += f"INSERT INTO Price(Price_Date, Price_Loose, Price_CIB, Price_Sealed) VALUES(\"{row['Price_Date']}\",{row['Loose_Price']}, {row['CIB_Price']}, {row['New_Price']});\n"
output_string += sql_strings.commit

# Insert statements for Publisher Table:
unique_publisher = df_data_combined["Publisher"].unique()
output_string += "\n/* Insert Publisher row data: */\nSTART TRANSACTION;\n"
for publisher in sorted(unique_publisher):
    output_string += f"INSERT INTO Publisher(Publisher_Name) VALUES(\"{publisher}\");\n"
output_string += sql_strings.commit

# Insert statements for Developer Table:
unique_developer = df_data_combined["Developer"].unique()
output_string += "\n/* Insert Developer row data: */\nSTART TRANSACTION;\n"
for developer in sorted(unique_developer):
    output_string += f"INSERT INTO Developer(Developer_Name) VALUES(\"{developer}\");\n"
output_string += sql_strings.commit

# Insert statements for Game Table:
df_data_combined["Release_Date"].fillna("NULL", inplace=True)
df_data_combined["Summary_y"] = df_data_combined["Summary_y"].str.replace(
    '"', '\\"')
output_string += "\n/* Insert Game row data: */\nSTART TRANSACTION;\n"
price_id = 1
for index, row in df_data_combined.iterrows():
    release_date = row["Release_Date"]
    # print(release_date)
    if release_date == "NULL":
        release_date = "NULL"
    else:
        release_date = f"\"{row['Release_Date']}\""
    output_string += f"INSERT INTO Game(Game_Title, Game_Release_Date, Game_UPC, Game_Summary, Game_URL, Console_ID, Genre_ID, ESRB_ID, Price_ID) VALUES(\"{row['Title']}\", {release_date}, \"{row['UPC']}\",\"{row['Summary_y']}\", \"{row['URL']}\", {row['Console_ID']}, {row['Genre_ID']}, {row['ESRB_ID']}, {price_id});\n"
    price_id += 1
output_string += sql_strings.commit

# Insert statements for Publishes and Develops Tables:
game_id = 1
publishes_string, develops_string = "", ""
output_string += "\n/* Insert Publishes and Develops row data: */\nSTART TRANSACTION;\n"
for index, row in df_data_combined.iterrows():
    publishes_string += f"INSERT INTO Publishes(Publisher_ID, Game_ID) VALUES({row['Publisher_ID']}, {game_id});\n"
    develops_string += f"INSERT INTO Develops(Developer_ID, Game_ID) VALUES({row['Developer_ID']}, {game_id});\n"
    game_id += 1
output_string += publishes_string
output_string += develops_string
output_string += sql_strings.commit

# Dummy input data for Collection and Collected Insert statements:
output_string += sql_strings.collection_inserts
output_string += sql_strings.collected_inserts

# Write the SQL statements to a .txt file to copy and paste into MySQL:
with open(file=f"output_testing-{TODAY}.txt", mode="w", encoding="utf-8", newline="\n") as file:
    file.write(output_string)
##### ----- End Create Test file with SQL lines needed to create Database and some Tables ----- #####

# Write combined game data DataFrame to .csv including Foreign Key IDs:
df_data_combined.to_csv(f"./Combined/{TODAY}-Special-Combined-Game_Info-TESTING.csv",
                        lineterminator="\n", index=False, encoding="utf-8")

print(df_data_combined)


##### ----- BEGIN EXTRA DB CONNECTION STUFF I DON'T NEED RIGHT NOW ----- #####
# Have to connect to MySQL database using the Python interface for connecting:
# mydb = mysql.connector.connect(
#     host="localhost", user="root", password="mdL3.nYf-YkxYnnY@jcy", database="n64_games")
# Use SQLAlchemy instead of mysql.connector
# engine = create_engine(
#     'mysql://root:mdL3.nYf-YkxYnnY%40jcy@localhost')
# with engine.connect() as connection:
#     connection.execute(text("CREATE DATABASE n64_games"))
# connection = engine.connect()
# connection.execute(text(f"CREATE DATABASE {SCHEMA}"))
# connection.execute(text(f"USE {SCHEMA}"))
# connection.execute(text(f'''CREATE TABLE game_list (
#     Game_ID INT UNSIGNED AUTO_INCREMENT,
#     Console VARCHAR(255),
#     Title VARCHAR(255),
#     Release_Date DATE,
#     ESRB VARCHAR(255),
#     Publisher VARCHAR(255),
#     Developer VARCHAR(255),
#     Genre VARCHAR(255),
#     UPC VARCHAR(255),
#     PC_ID VARCHAR(255),
#     Summary VARCHAR(3000),
#     URL VARCHAR(255),
#     PRIMARY KEY(Game_ID)
# )'''))

# connection.commit()


# mycursor = mydb.cursor()

# Have to create a table first
### ----- TABLE MUST HAVE THE SAME STRUCTURE AS THE DATAFRAME ----- ###
# mycursor.execute('''CREATE TABLE game_list (
#     Console VARCHAR(255),
#     Title VARCHAR(255),
#     Release_Date DATE,
#     ESRB VARCHAR(255),
#     Publisher VARCHAR(255),
#     Developer VARCHAR(255),
#     Genre VARCHAR(255),
#     UPC VARCHAR(255),
#     PC_ID VARCHAR(255),
#     Summary VARCHAR(3000),
#     URL VARCHAR(255),
#     PRIMARY KEY(PC_ID)
# );''')
### ----- CAN'T GET THE ABOVE SQL QUERY TO WORK ----- ###

# Import pandas csv and convert to sql
# df = pd.read_csv(
#     "./Consoles/2023_09_29-nintendo-64-Game_List.csv", index_col=False, lineterminator="\n", encoding="utf8")
# df = pd.read_csv(
#     "./Duplicates/2023_10_29-nes-Duplicates_Dropped.csv", index_col=0, lineterminator="\n", encoding="utf8")

# print(df.head)
# df.to_sql(name="game_list", schema="nes", con=connection, if_exists='append')

# connection.close()
##### ----- END EXTRA DB CONNECTION STUFF I DON'T NEED RIGHT NOW ----- #####
