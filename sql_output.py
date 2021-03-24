
# TODO Remove print funcitions

import mysql.connector
import json

CONFIG_FILENAME = 'configSQL.json'


def save_to_database(assets_names, assets_values):
    load_json()
    db_files = connect_mysql()
    create_table(db_files[0], assets_names)
    insert_row(db_files[0], db_files[1], assets_values, assets_names)
    # print_table(db_files[0])


def load_json():
    with open(CONFIG_FILENAME) as config_file:
        global data
        data = json.load(config_file)


def connect_mysql():
    mydb = mysql.connector.connect(
        host=data['host'],
        user=data['user'],
        password=data['password'],
        database=data['database']
    )
    mycursor = mydb.cursor()
    return mycursor, mydb


def create_table(mycursor, asset_names):
    mycursor.execute("SHOW TABLES")

    table_exists = False
    for x in mycursor:
        table_exists = True

    if not table_exists:
        mycursor.execute("CREATE TABLE assets (\
            time TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON" +
                         " UPDATE CURRENT_TIMESTAMP)")

    for asset in asset_names:
        if not column_exists(mycursor, asset):
            print("Adding column asset %s" % asset)
            mycursor.execute("ALTER TABLE assets ADD COLUMN \
                            %s FLOAT NOT NULL" % asset)
    return mycursor


def column_exists(mycursor, column_name):
    mycursor.execute("SELECT COUNT(*) FROM INFORMATION_SCHEMA.COLUMNS \
                                    WHERE TABLE_SCHEMA='%s' \
                                    AND TABLE_NAME='assets'\
                                    AND COLUMN_NAME='%s'" %
                     (data['database'], column_name))

    return mycursor.fetchone()[0] != 0


def insert_row(mycursor, mydb, quotes_list, coins):
    coin_list = ", ".join(coins)
    quote_list = ", ".join(str(q) for q in quotes_list)

    sql = "INSERT INTO assets (%s) VALUES (%s)" %\
        (coin_list, quote_list)

    mycursor.execute(sql)

    mydb.commit()


# def print_table(mycursor):
#     # execute your query
#     mycursor.execute("SELECT * FROM assets")

#     # fetch all the matching rows
#     result = mycursor.fetchall()

#     # loop through the rows
#     for row in result:
#         print(row)
#         print("\n")

#     print("END")
