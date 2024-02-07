'''
SQL statements as strings for creating tables.
'''
commit = '''COMMIT;\n'''

# Schema name to create Database:
SCHEMA = "Retro_Games"

header_comment = f'''/* {SCHEMA} */
/* Daniel Ghrist (kda458) */
/* Carlos Martinez (mro738) */
/* CS3743.004: Database Systems */
/* Team Project (Group03): DDL */
/* Type of SQL: MySQL */
'''


create_schema = f'''
DROP DATABASE IF EXISTS {SCHEMA};
CREATE DATABASE {SCHEMA};
USE {SCHEMA};
'''

### ----- BEGIN CREATE TABLE STATEMENTS ----- ###
user_table = f'''
CREATE TABLE User (
    User_ID INT UNSIGNED AUTO_INCREMENT,
    User_Login VARCHAR(255) NOT NULL,
    User_Password VARCHAR(255) NOT NULL,
    User_Email VARCHAR(255) NOT NULL,
    User_First_Name VARCHAR(255) NOT NULL,
    User_Last_Name VARCHAR(255) NOT NULL,
    PRIMARY KEY(User_ID)
);
'''

console_table = f'''
CREATE TABLE Console (
    Console_ID INT UNSIGNED AUTO_INCREMENT,
    Console_Name VARCHAR(255),
    Console_Type VARCHAR(255),
    PRIMARY KEY(Console_ID)
);
'''

genre_table = f'''
CREATE TABLE Genre (
    Genre_ID INT UNSIGNED AUTO_INCREMENT,
    Genre_Name VARCHAR(255),
    PRIMARY KEY(Genre_ID)
);
'''

esrb_table = f'''
CREATE TABLE ESRB (
    ESRB_ID INT UNSIGNED AUTO_INCREMENT,
    ESRB_Name VARCHAR(255),
    PRIMARY KEY(ESRB_ID)
);
'''

price_table = f'''
CREATE TABLE Price (
    Price_ID INT UNSIGNED AUTO_INCREMENT,
    Price_Date DATE NULL DEFAULT NULL,
    Price_Loose DECIMAL(19, 2) DEFAULT NULL,
    Price_CIB DECIMAL(19, 2) DEFAULT NULL,
    Price_Sealed DECIMAL(19, 2) DEFAULT NULL,
    PRIMARY KEY(Price_ID)
);
'''

publisher_table = f'''
CREATE TABLE Publisher (
    Publisher_ID INT UNSIGNED AUTO_INCREMENT,
    Publisher_Name VARCHAR(255),
    PRIMARY KEY(Publisher_ID)
);
'''

developer_table = f'''
CREATE TABLE Developer (
    Developer_ID INT UNSIGNED AUTO_INCREMENT,
    Developer_Name VARCHAR(255),
    PRIMARY KEY(Developer_ID)
);
'''

game_table = f'''
CREATE TABLE Game (
    Game_ID INT UNSIGNED AUTO_INCREMENT,
    Game_Title VARCHAR(255),
    Game_Release_Date DATE NULL DEFAULT NULL,
    Game_UPC VARCHAR(255),
    Game_Summary VARCHAR(3000),
    Game_URL VARCHAR(255),
    Console_ID INT UNSIGNED,
    Genre_ID INT UNSIGNED,
    ESRB_ID INT UNSIGNED,
    Price_ID INT UNSIGNED,
    PRIMARY KEY(Game_ID),
    FOREIGN KEY(Console_ID) REFERENCES Console(Console_ID),
    FOREIGN KEY(Genre_ID) REFERENCES Genre(Genre_ID),
    FOREIGN KEY(ESRB_ID) REFERENCES ESRB(ESRB_ID),
    FOREIGN KEY(Price_ID) REFERENCES Price(Price_ID)
);
'''
# game_table = f'''
# CREATE TABLE Game (
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
#     Console_ID INT UNSIGNED,
#     Publisher_ID INT UNSIGNED,
#     Developer_ID INT UNSIGNED,
#     Genre_ID INT UNSIGNED,
#     PRIMARY KEY(Game_ID),
#     FOREIGN KEY(Console_ID) REFERENCES Console(Console_ID),
#     FOREIGN KEY(Publisher_ID) REFERENCES Publisher(Publisher_ID),
#     FOREIGN KEY(Developer_ID) REFERENCES Developer(Developer_ID),
#     FOREIGN KEY(Genre_ID) REFERENCES Genre(Genre_ID)
# );
# '''

publishes_table = f'''
CREATE TABLE Publishes (
    Publisher_ID INT UNSIGNED,
    Game_ID INT UNSIGNED,
    PRIMARY KEY(Publisher_ID, Game_ID),
    FOREIGN KEY(Publisher_ID) REFERENCES Publisher(Publisher_ID),
    FOREIGN KEY(Game_ID) REFERENCES Game(Game_ID)
);
'''

develops_table = f'''
CREATE TABLE Develops (
    Developer_ID INT UNSIGNED,
    Game_ID INT UNSIGNED,
    PRIMARY KEY(Developer_ID, Game_ID),
    FOREIGN KEY(Developer_ID) REFERENCES Developer(Developer_ID),
    FOREIGN KEY(Game_ID) REFERENCES Game(Game_ID)
);
'''

collection_table = f'''
CREATE TABLE Collection (
    Collection_ID INT UNSIGNED AUTO_INCREMENT,
    Collection_Name VARCHAR(255),
    User_ID INT UNSIGNED,
    PRIMARY KEY(Collection_ID),
    CONSTRAINT FK_User
    FOREIGN KEY(User_ID) REFERENCES User(User_ID)
        ON UPDATE CASCADE
        ON DELETE CASCADE
);
'''

collected_table = f'''
CREATE TABLE Collected (
    Collection_ID INT UNSIGNED,
    Game_ID INT UNSIGNED,
    Collected_Purch_Date DATE DEFAULT(CURRENT_DATE),
    Collected_Purch_Price DECIMAL(19, 2) DEFAULT NULL,
    Collected_Quantity INT UNSIGNED DEFAULT 1,
    Collected_Condition VARCHAR(255) DEFAULT NULL,
    PRIMARY KEY(Collection_ID, Game_ID),
    FOREIGN KEY(Collection_ID) REFERENCES Collection(Collection_ID),
    FOREIGN KEY(Game_ID) REFERENCES Game(Game_ID)
        ON UPDATE CASCADE
        ON DELETE CASCADE
);
'''
### ----- END CREATE TABLE STATEMENTS ----- ###


### ----- BEGIN INSERT STATEMENTS ----- ###
user_inserts = f'''
/* Insert User row data: */
START TRANSACTION;
INSERT INTO User(User_Login, User_Password, User_Email, User_First_Name, User_Last_Name) VALUES("danny", SHA2("1234", 256), "danny@email.com", "Daniel", "Ghrist");
INSERT INTO User(User_Login, User_Password, User_Email, User_First_Name, User_Last_Name) VALUES("carlos", SHA2("4567", 256), "carlos@email.com", "Carlos", "Martinez");
INSERT INTO User(User_Login, User_Password, User_Email, User_First_Name, User_Last_Name) VALUES("johnny", SHA2("password", 256), "johnny@email.com", "John", "Smith");
INSERT INTO User(User_Login, User_Password, User_Email, User_First_Name, User_Last_Name) VALUES("janedoe", SHA2("unknown", 256), "jane@email.com", "Jane", "Doe");
INSERT INTO User(User_Login, User_Password, User_Email, User_First_Name, User_Last_Name) VALUES("johndoe", SHA2("unknown234", 256), "johndoe@email.com", "John", "Doe");
INSERT INTO User(User_Login, User_Password, User_Email, User_First_Name, User_Last_Name) VALUES("mickey", SHA2("walt", 256), "the_mouse@email.com", "Mickey", "Mouse");
INSERT INTO User(User_Login, User_Password, User_Email, User_First_Name, User_Last_Name) VALUES("daffy", SHA2("duckzrule", 256), "daffy@email.com", "Daffy", "Duck");
INSERT INTO User(User_Login, User_Password, User_Email, User_First_Name, User_Last_Name) VALUES("minnie", SHA2("heartmickey1", 256), "minnie@email.com", "Minnie", "Mouse");
INSERT INTO User(User_Login, User_Password, User_Email, User_First_Name, User_Last_Name) VALUES("Daisy", SHA2("i'mcoolerthanminnie", 256), "daisy@email.com", "Daisy", "Duck");
INSERT INTO User(User_Login, User_Password, User_Email, User_First_Name, User_Last_Name) VALUES("dog", SHA2("imdog", 256), "dogdogdog@email.com", "Pluto", "Dog");
COMMIT;
'''

collection_inserts = f'''
/* Insert Collection row data: */
START TRANSACTION;
INSERT INTO Collection(Collection_Name, User_ID) VALUES("Danny Collection", 1);
INSERT INTO Collection(Collection_Name, User_ID) VALUES("Carlos Sealed Collection", 2);
COMMIT;
'''

collected_inserts = f'''
/* Insert Collected row data: */
START TRANSACTION;
INSERT INTO Collected(Collection_ID, Game_ID, Collected_Purch_Date, Collected_Purch_Price, Collected_Quantity, Collected_Condition) VALUES(1, 462, "2023-10-22", 10.98, 1, "Loose");
INSERT INTO Collected(Collection_ID, Game_ID, Collected_Purch_Date, Collected_Purch_Price, Collected_Quantity, Collected_Condition) VALUES(1, 1000, "2023-11-09", 35.82, 1, "Sealed in Box");
INSERT INTO Collected(Collection_ID, Game_ID, Collected_Purch_Date, Collected_Purch_Price, Collected_Quantity, Collected_Condition) VALUES(1, 526, "2023-09-15", 25.00, 1, "Complete in Box");
INSERT INTO Collected(Collection_ID, Game_ID, Collected_Purch_Date, Collected_Purch_Price, Collected_Quantity, Collected_Condition) VALUES(1, 2253, "2022-11-24", 123.00, 1, "Complete in Box");
INSERT INTO Collected(Collection_ID, Game_ID, Collected_Purch_Date, Collected_Purch_Price, Collected_Quantity, Collected_Condition) VALUES(1, 1500, "2021-07-19", 53.55, 1, "Complete in Box");
INSERT INTO Collected(Collection_ID, Game_ID, Collected_Purch_Date, Collected_Purch_Price, Collected_Quantity, Collected_Condition) VALUES(2, 4000, "2023-11-10", 50, 1, "Sealed in Box");
INSERT INTO Collected(Collection_ID, Game_ID, Collected_Purch_Date, Collected_Purch_Price, Collected_Quantity, Collected_Condition) VALUES(2, 123, "2023-01-01", 102.56, 1, "Sealed in Box");
INSERT INTO Collected(Collection_ID, Game_ID, Collected_Purch_Date, Collected_Purch_Price, Collected_Quantity, Collected_Condition) VALUES(2, 562, "2022-02-15", 59.64, 1, "Sealed in Box");
INSERT INTO Collected(Collection_ID, Game_ID, Collected_Purch_Date, Collected_Purch_Price, Collected_Quantity, Collected_Condition) VALUES(2, 2500, "2022-05-30", 350, 1, "Sealed in Box");
INSERT INTO Collected(Collection_ID, Game_ID, Collected_Purch_Date, Collected_Purch_Price, Collected_Quantity, Collected_Condition) VALUES(2, 3500, "2022-12-11", 99, 1, "Sealed in Box");
COMMIT;
'''
### ----- END INSERT STATEMENTS ----- ###
