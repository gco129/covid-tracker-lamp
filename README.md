# COVID-19 Tracker
A website that is run using a LAMP server to track new and confirmed cases/deaths. Scrapes a website (https://www.worldometers.info/coronavirus/country/us/) for this information.

## How do you run this?
I run the website using the Windows Subsystem for Linux in combination with files from this repository. Using the Linux shell, I move the necessary files into the proper Linux directory. This Linux subsystem hosts the Apache HTTP server, the MySQL database, and the files for the website itself (such as the main PHP file).

In order to run, the Apache server and MySQL services must be running. Afterwards, run ``getstats.sh`` to keep the website's information updated. In order for the script to work properly, ``tagsoup-1.2.1.jar`` is needed in the same directory as the script (tagsoup not included in this repo).

## Files of the LAMP Server
* covidsite.php - the website itself
* getstats.sh - downloads the website to scrape information from, runs the parser, then deletes the downloaded website (set to repeat every 30 minutes)
* parser.py - scrapes data from the downloaded website, updates the database with the updated information
* sources.txt - websites to download, source of the statistics shown on the website
