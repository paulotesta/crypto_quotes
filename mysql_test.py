# TODO Segment program into single action functions
# TODO Make SQL query('sql') flexible to not just a fixed number of assets
# TODO Check if any other assets were added after first table creation
# TODO Remove print funcitions
# TODO Integrate with cryptoCSV.py

import mysql.connector
import json

# assets list will be given by the cryptoCSV file
assets = ["BTC", "ETH", "DOGE", "ETC"]

CONFIG_FILENAME = 'configSQL.json'

with open(CONFIG_FILENAME) as config_file:
    data = json.load(config_file)

mydb = mysql.connector.connect(
  host=data['host'],
  user=data['user'],
  password=data['password'],
  database=data['database']
)

mycursor = mydb.cursor()

mycursor.execute("SHOW TABLES")

table_exists = False
for x in mycursor:
    table_exists = True

if not table_exists:
    mycursor.execute("CREATE TABLE assets (\
        time TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP)")
    for asset in assets:
        mycursor.execute("ALTER TABLE assets ADD COLUMN %s FLOAT NOT NULL" %
                         asset)

# quotes list will be given by the cryptoCSV file
quotes_list = [34339.76271, 1326.288021, 0.04720086692, 11.720020426273300]

sql = "INSERT INTO assets (BTC, ETH, DOGE, ETC) VALUES (%f, %f, %f, %f)" %\
        (quotes_list[0], quotes_list[1], quotes_list[2], quotes_list[3])
mycursor.execute(sql)

mydb.commit()

# execute your query
mycursor.execute("SELECT * FROM assets")

# fetch all the matching rows
result = mycursor.fetchall()

# loop through the rows
for row in result:
    print(row)
    print("\n")

print("END")
