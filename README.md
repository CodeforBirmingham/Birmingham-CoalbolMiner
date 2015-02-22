# Birmingham-CoalbolMiner
COALbol Miner - Converts old data into SQL databases.

# Copyright
(C) Code For Birmingham <http://codeforbirmingham.org>
@author: Marcus Dillavou <marcus.dillavou@codeforbirmingham.org>
@license: MIT License

# Requirements
COALBOL Miner (cbminer) is a python library. You will need the following:

 - python 2.7.x
 - sqlalchemy

# Usage
CBMiner can be run in two ways: in batch through the command line or through the web interface. It is recommended that you use the web interface to at least setup and configure cb miner's database backend.

To start the webserver, run:

 $ python cbminer-server

This will start a small http server on port 8080. Point your webbrowser to http://127.0.0.1:8080/

From here, you will first be able to configure the sql database backend that will be used. There are several options, including Microsoft SQL Server, postgresql, mysql, and sqlite.

Once configured, this data is saved in the cbminer.ini and is persistent for both the batch mode and the web mode.

At this point, you will first need to upload the Schema file. This file tells us the translations we will use along with the tables that will be created. Once the schema is parsed, the available tables will be shown. You can then being uploading the old csv data for the appropriate tables.

You can also run this in batch mode on the command line. You need to make sure your cbminer.ini is configured either manually, or through the web. For batch mode, you will run the cbminer program.

 $ python cbminer

The cbminer has several require parameters. You MUST include the schema file as an option and then specify one or more database related to tables in the schema. For example, if you had a schema for the employee table and an employee dataset, your would run as follows:

 $ python cbminer employee_schema.csv --table Employee employee_data.csv

If your schema contains multiple tables, for example, the schema has an employee table and a product table, you would run as follows:

 $ python cbminer schema.csv --table Employees employee_data.csv --table Products product_data.csv

# Other Information

The biggest issue around this project is normalizing and converting data. The data conversion has been encapsulated in the ColumnFactory class. This class has two main goals:

 1. Converting the column types named in the schema into a SQLAlchemy Column type
 2. Converting the actual data into the correct python type.

For example, for converting the data, the Schema will list a Date type, and the data will have a string like 92280. This needs to be correctly parsed in converting into a python Date object first. The ColumnFactory will likely need to be extended as more data is available and more types are discovered.