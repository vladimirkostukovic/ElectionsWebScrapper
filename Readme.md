# Elections Scraper

This is my third project for the Engeto Online Python Academy.

The goal of this project is to download official election results from the Czech Republic (2017) using web scraping. The data is taken from the website volby.cz.

## What this script does

- You give it a link to a region page (ps32) from volby.cz
- It finds all the municipalities (villages)
- For each village, it downloads:
  - Total voters
  - Issued ballots
  - Valid votes
  - Results for each political party
- Saves the data to a CSV file

## How to run the script

1. Make sure you have Python 3 installed.
2. Install required libraries:
   pip install requests beautifulsoup4 pandas tqdm
3. Run the script with two arguments:
   python projekt_3.py <ps32_link> <output_file.csv>

Example:
python projekt_3.py https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=6&xnumnuts=4201 vysledky.csv

## Notes

- This scraper is slow on purpose — I added delays to avoid overloading the server.
- It works only with links from the 2017 Czech parliamentary elections (ps2017nss).
- If no data is found, check if your link is correct and points to a region page (it should contain ps32 in the URL).

## File structure

main.py     # Main Python script  
README.md        # This file
requirments.txt
