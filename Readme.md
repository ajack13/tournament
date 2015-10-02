# Tournament - [ajay]
Database schema for a swiss style tournament

### Pre-requisites

1) Python

2) PostgreSQL

3) python-psycopg2
### Required Libraries and dependencies

1) Git (optional)

### Installation

download zip	

Unzip the file 
```sh
$ cd tournament
```
or
    
Clone github repository
	
Open the shell in mac/linux or command prompt in windows and navigate to the folder you wnat to clone the repository
	
Make sure you have installed git
	
```sh
	$ git clone https://github.com/ajack13/tournament.git
```
this should clone the repository to the folder

# Files
---------------------------------------------------
### tournament.sql
Contains the queries for creating tables and views for PostgreSQL
### tournament.py
Contains python defenitions for the following db operations
* DB connection
* Register Players
* Delete Players
* Swiss style parings
* Player Standings (Points table)
* other utilities
### tournmarnt_test.py
Test cases for the queries
# Run Test cases
---------------------------------------------------
1)	Navigate to the folder using command promt if you are in windows or the shell if you are using a mac or linux
2)	Run the file tournament_test.py using python by typing the following command to run through the test cases 

```sh
    $ cd tournament
	$ python tournament_test.py
```

### Version
1.0

### Tech
* Sublime text - Text editor 
* PostgreSQL
* python

