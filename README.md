# crypto_quotes

Crypto_quotes is a crypto asset monitor that can fetch assets prices and output to a CSV file or SQL database.

## Instructions

To run the program Python3 and a database management system (MySQL) are required.
A private key to the coinAPI.io and Fixer.io are also required. These need to be added as the "api_key" and "currency_key" into the config.json file.

### config.json

A "config.json" file must be present with the following fields:

* "currencies" - A list with all the Assets codes that will be tracked: ["BTC", "ETH"]
* "api_key"/"currency_key" - private keys that allow access to APIs
* "currency" - Currency in which the assets values will be presented: "GBP"
* "output" - Type of output file that's going to be creaded/modified, supported file formats: CSV or SQL

### configSQL.json

A "configSQL.json" filme must be present with the following fields:

* "host" - Host name of the SQL Database
* "user" - User name for the database
* "password" - Password to access the database
* "database" - Name of the database being used

### Runing

```sh
python3 cryptoCSV.py
```

After this command either a CSV file will be created together with the first line of data and one new line with the current asset values will be generated every whole hour until the program is terminated or a SQL table will be creaded and updated in the same way.
