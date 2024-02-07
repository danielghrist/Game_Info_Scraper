import pandas as pd
# import mysql.connector   # DOESN'T WORK, TRYING SQLALCHEMY INSTEAD
from sqlalchemy import create_engine, Connection, text, types

# Schema to create:
SCHEMA = "Group03-Team_Project"

# List of the Table names that need to be created:
TABLE_NAMES = ["Publisher", "Developer", "Console", "Genre",
               "Price", "User", "Game", "Publishes", "Develops", "Collection"]

# List of Consoles:
CONSOLE = ["gameboy", "gameboy-advance", "nes", "super-nintendo",
           "nintendo-64", "sega-game-gear", "nintendo-3ds"]

# Have to connect to MySQL database using the Python interface for connecting:
# mydb = mysql.connector.connect(
#     host="localhost", user="root", password="mdL3.nYf-YkxYnnY@jcy", database="n64_games")
# Use SQLAlchemy instead of mysql.connector
engine = create_engine(
    'mysql://root:mdL3.nYf-YkxYnnY%40jcy@localhost')
# with engine.connect() as connection:
#     connection.execute(text("CREATE DATABASE n64_games"))
connection = engine.connect()
connection.execute(text(f"CREATE DATABASE {SCHEMA}"))
connection.execute(text(f"USE {SCHEMA}"))
connection.execute(text(f'''CREATE TABLE game_list (
    Game_ID INT UNSIGNED AUTO_INCREMENT,
    Console VARCHAR(255),
    Title VARCHAR(255),
    Release_Date DATE,
    ESRB VARCHAR(255),
    Publisher VARCHAR(255),
    Developer VARCHAR(255),
    Genre VARCHAR(255),
    UPC VARCHAR(255),
    PC_ID VARCHAR(255),
    Summary VARCHAR(3000),
    URL VARCHAR(255),
    PRIMARY KEY(Game_ID)
)'''))

connection.commit()

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
df = pd.read_csv(
    "./Duplicates/2023_10_29-nes-Duplicates_Dropped.csv", index_col=0, lineterminator="\n", encoding="utf8")

print(df.head)
df.to_sql(name="game_list", schema="nes", con=connection, if_exists='append')

connection.close()
