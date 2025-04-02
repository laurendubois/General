import sys
import datetime
from pathlib import Path
import requests
from bs4 import BeautifulSoup

""" Uses Alma API to list all holdings associated with the MMS IDs provided """
""" Useful when list of MMS ID too long for analytics """

# Constants for file names
ROOT_FILE_NAME = "alma_unassigned"
TIMESTAMP = datetime.datetime.now().strftime('_%Y%m%d_%H%M%S')

IN_DIR = Path("../input")
OUT_DIR = Path("../output")

API_KEY_FILE = IN_DIR / 'psb_prod.txt'
MMS_IDS_FILE = IN_DIR / 'bibs.txt'
OUTPUT_FILE = OUT_DIR / f"{ROOT_FILE_NAME}{TIMESTAMP}.txt"
ERROR_FILE = OUT_DIR / f"{ROOT_FILE_NAME}{TIMESTAMP}_errors.txt"

BASE_URL = "https://api-na.hosted.exlibrisgroup.com/almaws/v1/"

def read_api_key(file_path):
    """Reads and returns the API key from a file."""
    with open(file_path, 'r') as file:
        return file.read().strip()

# Read API key
API_KEY = read_api_key(API_KEY_FILE)

# API headers
HEADERS = {
    "Authorization": f"apikey {API_KEY}",
    "Content-Type": "application/xml",
    "Accept": "application/xml"
}

sys.stdout.write("Checking API key...")
test_api = requests.get(BASE_URL + "bibs/test", headers=HEADERS)
if test_api.status_code == 400:
    print("\nInvalid API key - please confirm key has r/w permission for /bibs", )
    sys.exit()
elif test_api.status_code != 200:
    print(f'\nError: Failed to connect to API. Status code: {test_api.status_code}')
    sys.exit()
else:
    sys.stdout.write("OK\n")

# Read MMS IDs from file
with open(MMS_IDS_FILE, 'r') as file:
    mms_ids = [line.strip() for line in file]


def get_holdings(mms_id):
    # Retrieves holding XML based on MMS ID
    url = f"{BASE_URL}bibs/{mms_id}/holdings"
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        holdings_xml = response.text
        return holdings_xml
    else:
        print(f"Failed to retrieve holdings for MMS ID: {mms_id}")
        return None


def extract_holding_details(xml_string):
    # Extracts specific fields from the holding XML
    soup = BeautifulSoup(xml_string, 'xml')
    holding_record_details = []
    for holding in soup.find_all('holding'):
        holding_id = holding.find('holding_id').text.strip()
        location = holding.find('location').get('desc') if holding.find('location') else ""
        holding_record_details.append((holding_id, location))

    return holding_record_details


def write_mms_and_holding_details(filename, mms_id, holding_details):
    # Writes the extracted field details to a txt
    with open(filename, 'a') as file:  # Use 'a' mode to append each line to file
        for holding_detail in holding_details:
            holding_id, location = holding_detail
            file.write(
                f"MMSID: {mms_id}|HoldingID: {holding_id}|Location: {location}\n")


# Then loop through all the MMS IDs listed and write to the same txt
for mms_id in mms_ids:
    holdings_xml = get_holdings(mms_id)
    if holdings_xml:
        holding_details = extract_holding_details(holdings_xml)
        if holding_details:
            write_mms_and_holding_details(OUTPUT_FILE, mms_id, holding_details)
            print(f"MMS ID {mms_id} appended to {OUTPUT_FILE}")
        else:
            with open(ERROR_FILE, 'a') as file:
                file.write(f"No record: {mms_id}\n")
            print(f"No record for {mms_id}. Written to {ERROR_FILE}")
    else:
        with open(ERROR_FILE, 'a') as file:
            file.write(f"Failed MMS ID: {mms_id}\n")
        print(f"Failed to retrieve {mms_id}. Written to {ERROR_FILE}")