# Analyzer

## DBUpdater.py

- It is a code that is stored and managed in a database using stock OHLCV data provided Korea Exchange and Korean portal sites, NAVER.
- This is done using MariaDB, so [download](https://www.mariadb.com) it from the website and use via dbupdater.py
- Database creation is required through HeidiSQL before execution.  
- The example code created a database named Invest, so it needs to be modified if the name is changed.  

## config.json

- When updating the database, change how many pages you want to crawl for each event.
  
  > {"pages_to_fetch" : %d}, update_page

## Avoiding "ConnectionAbortedError" Problems

- Need to fix C:\Program Files\MariaDB(Version)\data\my.ini

  > wait_timeout = flexible time(at seconds, ex. 256000)
