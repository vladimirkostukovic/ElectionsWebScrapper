🗳️ Czech Elections Scraper

Welcome! This script allows you to scrape election results from the Czech National Election website. It extracts voting data for a selected region and saves it in a structured CSV file.

📌 Features

Scrapes election results for any selected region (municipality level)

Extracts voter statistics and party results

Saves the data as a CSV file

Handles errors and duplicate entries

🛠️ Installation

Before running the script, make sure you have Python installed and set up a virtual environment (optional but recommended):

python -m venv venv
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate    # Windows

Install the required dependencies:

pip install -r requirements.txt

🚀 Usage

Run the script with two arguments:

python script.py <region_url> <output_file.csv>

<region_url>: The link to the region (must be from the official election website)

<output_file.csv>: The name of the output file (it will be saved in CSV format)

Example:

python script.py https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=9 election_results.csv

⚠️ Important Notes

Make sure you provide a valid ps32 URL from the election website.

If the arguments are incorrect or missing, the script will display an error and exit.

The script automatically prevents duplicate data entries.

📄 Output Format

The script generates a CSV file with the following structure:

Kód obce, Obec, Voliči, Vydané lístky, Platné hlasy, [Party Names...]

Each row represents a municipality with election statistics and votes for each party.

🏁 Conclusion

This scraper is a useful tool for extracting structured election data from the Czech elections website. If you encounter any issues, feel free to improve or modify the script! Happy coding! 🚀

