"""
projekt_3.py: třetí projekt do Engeto Online Python Akademie

author: Vladimír Kosťukovič
email: kostyukovych@gmail.com
"""



import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import sys
from tqdm import tqdm  # progress bar

BASE_URL = "https://www.volby.cz/pls/ps2017nss/"

# Check command-line arguments
if len(sys.argv) != 3:
    print("❌ Error: You must enter two arguments!")
    print("Usage: python script.py <ps32_link> <output_file.csv>")
    sys.exit(1)

# Get arguments
input_url = sys.argv[1]  # Expected link to the region (ps32)
output_file = sys.argv[2]  # Name of the output file

# Validate the input URL
if not input_url.startswith(BASE_URL) or "ps32" not in input_url:
    print("❌ Error: Enter a valid link to the region (ps32)")
    sys.exit(1)

# Function to get a list of ps311 links (villages in the municipality)
def get_ps311_links(ps32_link):
    url = ps32_link
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    ps311_links = [a["href"] for a in soup.find_all("a", href=True) if "ps311" in a["href"]]
    return ps311_links

# Function to collect election data from ps311 (final voting results)
def get_election_data(ps311_link):
    url = BASE_URL + ps311_link
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    try:
        municipality_code = ps311_link.split("xobec=")[-1].split("&")[0]

        municipality_h3 = soup.find("h3", string=lambda x: x and "Obec" in x)
        if municipality_h3:
            municipality_name = municipality_h3.text.split(": ")[1].strip()
        else:
            raise ValueError("❌ Municipality name not found")

        table = soup.find("table", {"id": "ps311_t1"})
        if not table:
            raise ValueError("❌ Statistics table not found")

        rows = table.find_all("tr")[2:]
        summary_data = [td.text.strip() for td in rows[0].find_all("td")]

        voters = summary_data[3]  # Voters
        ballots_issued = summary_data[4]  # Ballots issued
        valid_votes = summary_data[7]  # Valid votes

        # Data for partiess
        parties_votes = {}
        parties_table = soup.find_all("table", {"class": "table"})[1:]

        for party_table in parties_table:
            for row in party_table.find_all("tr")[2:]:
                cols = row.find_all("td")
                if len(cols) < 5:
                    continue
                party_name = cols[1].text.strip()
                votes = cols[2].text.strip()
                parties_votes[party_name] = votes

        return {
            "Kód obce": municipality_code,
            "Obec": municipality_name,
            "Voliči": voters,
            "Vydané lístky": ballots_issued,
            "Platné hlasy": valid_votes,
            **parties_votes
        }
    except Exception as e:
        print(f"❌ Error processing {url}: {e}")
        return None

# 🔄 Start parsing
all_data = []
ps311_links = get_ps311_links(input_url)

if not ps311_links:
    print("❌ No ps311 links found in the region. Check the link.")
    sys.exit(1)

print(f"🏙️ Found {len(ps311_links)} municipalities, processing all...")

seen_municipalities = set()  # Store already processed municipalities

for ps311_link in tqdm(ps311_links, desc="📊 Processing data", unit="link"):
    print(f"🔍 Downloading data from {BASE_URL + ps311_link}")

    election_data = get_election_data(ps311_link)

    if election_data:
        # Remove duplicates by "Kód obce"
        municipality_code = election_data["Kód obce"]
        if municipality_code not in seen_municipalities:
            all_data.append(election_data)
            seen_municipalities.add(municipality_code)
        else:
            print(f"⚠️ Duplicate entry for {municipality_code}, skipped.")

    time.sleep(0.5)  # 🔹 Delay to avoid blocking

# Create DataFrame and remove duplicates
df = pd.DataFrame(all_data)
df.drop_duplicates(inplace=True)

# Add .csv extension if not present
if not output_file.endswith(".csv"):
    output_file += ".csv"

print(f"📁 Saving file: {output_file}")
df.to_csv(output_file, index=False, encoding="utf-8")
print("✅ Data successfully saved!")