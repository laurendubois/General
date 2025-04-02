import json
import datetime
import pandas as pd
from bookops_worldcat import WorldcatAccessToken, MetadataSession
from io import BytesIO
from pymarc import XmlHandler, parse_xml, Field, Subfield

"""Looks at GSheet with MMS/OCLC ID pairs, extracts .mrc from OCLC, inserts MMS ID in 001,
adjusts fields per Dave pycat"""

# Set up file paths
ROOT_FILE_NAME = "cgp_bibs"
TIMESTAMP = datetime.datetime.now().strftime('_%Y%m%d_%H%M%S')

# Load creds
with open('../input/my_wskey.json', 'r') as file:
    token_data = json.load(file)

# Create access token
token = WorldcatAccessToken(
    key=token_data['key'],
    secret=token_data['secret'],
    scopes=token_data['scopes']
)

# Convert MarcXML
def parse_xml_record(data):
    handler = XmlHandler()
    parse_xml(data, handler)
    return handler.records[0]

# Defines a new 590 field to help track records in Alma, do not change
my_590 = Field(
    tag="590",
    indicators=["0", " "],
    subfields=[Subfield(code="a", value="Imported with PyCat.")]
)

# Read OCLC numbers from a gsheet
gsheet = pd.read_csv(
    "https://docs.google.com/spreadsheets/d/1dDEJbAQzxUx0WyOR9_hw2uX07g4aWhTUl0-sczV1hZk/export?format=csv"
)

# Create a dictionary of OCLC/MMS pairs
id_dict = pd.Series(gsheet.MMSID.values, index=gsheet.OCLCID).to_dict()

# Define output path for bib records
output_path = f"../output/{ROOT_FILE_NAME}{TIMESTAMP}.mrc"

missing_mms_ids = []

# Loop over the OCLC IDs and make API calls
with MetadataSession(authorization=token) as session:
    for oclc_number in gsheet["OCLCID"]:
        # Make the API call to get the MARC record
        response = session.bib_get(oclcNumber=str(oclc_number))

        # Convert the response to a BytesIO object, then parse it with pymarc
        data = BytesIO(response.content)
        bib = parse_xml_record(data)

        # Add the custom 590 field
        bib.add_ordered_field(my_590)

        # Get the OCLC ID (001 field), look it up in the dictionary and replace it with MMS ID for Alma import
        oclc_id = bib["001"].value() if "001" in bib else ""
        oclc_id = oclc_id.removeprefix('on').strip()  # Remove prefix
        mms_id = id_dict.get(int(oclc_id))  # Convert the OCLC ID to an integer for correct lookup
        print(oclc_id,"|",mms_id)

        if mms_id:
            bib.remove_field(bib["001"])
            mms001 = Field(tag="001", data=mms_id)
            bib.add_ordered_field(mms001)
        else:
            missing_mms_ids.append(oclc_id)

        bib.remove_fields("015", "016", "017", "019", "029", "055", "060", "070", "072", "082", "084", "263", "856", "938")
        subjects = bib.get_fields("600", "610", "611", "630", "647", "648", "650", "651", "653", "654", "655", "656", "657", "658", "662")
        for s in subjects:
            if "7" in s.indicator2:
                bib.remove_field(s)

        # Write the updated record
        with open(output_path, "ab") as out:
            out.write(bib.as_marc())

# Print missing pairs for futher review
if missing_mms_ids:
    print("OCLC IDs MISSING MMS ID: ")
    for oclc_id in missing_mms_ids:
        print(oclc_id)

print("Processing complete.")
