# Mock databases

## Python Script

There is a python script in the script.
`mock-database.py`
It will:
1. Delete the existing mock databases.
2. Create the databases in the mock-database directory:
3. Populate the databases.

## How to add more tables/data.

Each database has two directories. One contains a DDL script for each table contained within the database, named [database]_ddl_scripts. The other, [database]_data, contains CSV files containing the data for each table.


The naming conventions are extremely important as the code uses these to establish where to write each table.



The directory caboodle_ddl_script contains files named with the format [address_dim].sql, Where the name between the square brackets is the name of the table, all in lowercase, with an underscore between each separate word. For example, [address_dim] represents the SQL used to create the table AddressDim.

The directory caboodle_data contain files named with the format [address_dim].csv which again return refers to the AddressDim table.

### Add data to an exising table

Open the corresponding csv file (for AddressDim from Caboodle this would be address_dim.csv in caboodle_data directory).
Add rows to the csv making sure to adhere to column headings.

### Add a new attribute to an existing table

Open the corresponding sql file (for AddressDim from Caboodle this would be address_dim.sql in caboodle_ddl_scripts directory).
Add the new column name and type to the sql code.

Open the corresponding csv file (for AddressDim from Caboodle this would be address_dim.csv in caboodle_data directory).
Add a new column heading.
Add data for that column to all existing rows - or just the comma if not value is being added.

### Add a new table

Assuming the name of the table is NewTable.

Add a sql file new_table.sql to the appropriate [database]_ddl_scripts directory.

Add a csv file new_table.csv to the appropriate [database]_data directory. 

## Adding tables from a new database

Create directories [newdatabase]_ddl scripts and [newdatabase]_data.

Populate these with appropriate csv and sql files.

Edit the mock-database.py script by adding the name of the database to the list.