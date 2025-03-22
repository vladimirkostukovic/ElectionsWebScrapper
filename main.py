import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import sys
from tqdm import tqdm

BASE_URL = "https://www.volby.cz/pls/ps2017nss/"

# Check script arguments
def check_arguments():
    if len(sys.argv) != 3:
        print("You must enter two arguments!")
        print("python script.py <ps32_link> <output_file.csv>")
        sys.exit(1)

    input_url = sys.argv[1]
    output_file = sys.argv[2]

    if not input_url.startswith(BASE_URL) or "ps32" not in input_url:
        print("Enter a valid link to the region")
        sys.exit(1)

    return input_url, output_file

# Get links to all villages from region page
def get_village_links(region_url):
    response = requests.get(region_url)
    soup = BeautifulSoup(response.text, "html.parser")
    return [a["href"] for a in soup.find_all("a", href=True) if "ps311" in a["href"]]

# Get name of the village
def get_village_name(soup):
    tag = soup.find("h3", string=lambda x: x and "Obec" in x)
    if tag:
        return tag.text.split(": ")[1].strip()
    return "Unknown"

# Get summary data: voters, ballots, valid votes
def get_summary_data(soup):
    table = soup.find("table", {"id": "ps311_t1"})
    rows = table.find_all("tr")[2:]
    cells = rows[0].find_all("td")
    return cells[3].text.strip(), cells[4].text.strip(), cells[7].text.strip()

# Get votes per party
def get_party_votes(soup):
    party_data = {}
    tables = soup.find_all("table", class_="table")[1:]
    for table in tables:
        for row in table.find_all("tr")[2:]:
            cols = row.find_all("td")
            if len(cols) >= 3:
                name = cols[1].text.strip()
                votes = cols[2].text.strip()
                party_data[name] = votes
    return party_data

# Get all election data from one village
def get_village_data(link):
    url = BASE_URL + link
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    try:
        code = link.split("xobec=")[-1].split("&")[0]
        name = get_village_name(soup)
        voters, ballots, valid = get_summary_data(soup)
        parties = get_party_votes(soup)

        data = {
            "Kód obce": code,
            "Obec": name,
            "Voliči": voters,
            "Vydané lístky": ballots,
            "Platné hlasy": valid
        }
        data.update(parties)
        return data
    except Exception as e:
        print(f"Error {url}: {e}")
        return None

# Main script
input_url, output_file = check_arguments()
all_data = []
village_links = get_village_links(input_url)

if not village_links:
    print("No links found in the region. Check the link.")
    sys.exit(1)

print(f"Found {len(village_links)} municipalities, processing all...")
seen = set()

for link in tqdm(village_links, desc="📊 Processing data", unit="link"):
    print(f"Downloading data from {BASE_URL + link}")
    result = get_village_data(link)
    if result:
        code = result["Kód obce"]
        if code not in seen:
            all_data.append(result)
            seen.add(code)
        else:
            print(f"Duplicate entry for {code}, skipped.")
    time.sleep(0.5)

# Save to CSV
df = pd.DataFrame(all_data)
df.drop_duplicates(inplace=True)
if not output_file.endswith(".csv"):
    output_file += ".csv"
df.to_csv(output_file, index=False, encoding="utf-8")
print(f"Data successfully saved to {output_file}!")
