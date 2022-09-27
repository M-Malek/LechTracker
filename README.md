# Lech Tracker

## Description
Simple API created to track current Lech Poznań statistics. The API allows you to actively track the results of matches 
and positions in the *PKO BP Ekstraklasa Premier League* table.


## Introduction
### GET Method
Using  APIis based on calling the current network location of the server. Default API address is:

> http://127.0.0.1:5000

Calling this URL results in displaying a website with the current league table of the Lech Poznań team and the 
table of the team's position in the *PKO PB Premier League*

### GET .json file
API allows to get raw `.json` file with data collected for a web API version

> http://127.0.0.1:5000/json

### Troubleshooting
- API based on online web services, sometimes, when meeting's data were not provided API can return a blank row without 
data,
- WEB page appearance has been customized only to 15,6" laptop screen,

### Data providers
- Data on the current games came from the [Sportowe Fakty WP](https://sportowefakty.wp.pl) website. 
- Data on the current Lech Poznań table position came from [Gol24](https://gol24.pl/) website.

The service was created for educational purposes only. The owners of the above websites do not allow the full 
webscraping of their pages.

### Used technologies
- Flask
- Requests

## Author
Michał Malek, Poland, Poznań september 2022

