import re
import pandas as pd
import requests
import os
from billgrab import PERFECTBILLLGRAB, FINALBILLGRAB

# Agenda URL
url = 'https://stlouisco.civicweb.net/document/118713/'

# Function to get the date for the meeting
def find_date_in_html_page(url):
    response = requests.get(url)
    html = response.text

    pattern = r"\w+,\s\w+\s\d+,\s\d{4}\s\w+\s\d+:\d+\s\w+"
    match = re.search(pattern, html)

    if match:
        return match.group()
    else:
        return None
date = find_date_in_html_page(url)

# Create a text file from the Agenda with just bill text
PERFECTBILLLGRAB(url)
FINALBILLGRAB(url)

# Read text file
with open('bills.txt', encoding="utf8") as f:
    text = f.read()

# Define regex patterns
bill_no_pattern = r'BILL NO\. (\d+), (\d+), INTRODUCED BY COUNCIL MEMBER(?:S)? ((?:\w+)(?: AND \w+)*)?, ENTITLED:'
amount_pattern = r'\$([\d,]+)'
purpose_pattern = r'FOR SUPPORT OF (.+)[;|\.]'
source_pattern = r"FROM (?:THE )?([A-Z\s]+)"

# Compile regex patterns
bill_no_regex = re.compile(bill_no_pattern)
amount_regex = re.compile(amount_pattern)
purpose_regex = re.compile(purpose_pattern)
source_regex = re.compile(source_pattern)

# Initialize variables
bill_no = []
council_member = []
amount = []
purpose = []
source = []

# Loop through all bills in the text
for bill_text in text.split('Bill No.'):
    bill_match = bill_no_regex.search(bill_text)
    if bill_match:
        bill_no.append(bill_match.group(1))
        council_member.append(bill_match.group(3))
        
        amount_match = amount_regex.search(bill_text)
        if amount_match:
            amount.append(amount_match.group(1))
        else:
            amount.append('')
        
        purpose_match = purpose_regex.search(bill_text)
        if purpose_match:
            purpose.append(purpose_match.group(1))
        else:
            purpose.append('')
        
        source_match = source_regex.search(bill_text)
        if source_match:
            source.append(source_match.group(1))
        else:
            source.append('')

# Create dataframe
data = {'Bill Number': bill_no, 
        'Council Member': council_member, 
        'Amount': amount, 
        'Purpose': purpose, 
        'Source': source}
df = pd.DataFrame(data)

# Drop rows with empty amount
df = df[df['Amount'] != '']

#print('#######################################')
#print('This is the STL County Council Meeting for:')
#print(date)
#print('#######################################')
#print(df)

# Write the dataframe to a Markdown file
with open('output/agenda_data.md', 'w', encoding='utf-8') as f:
    f.write(df.to_markdown(index=False))

# Stats function
def stats(df):
    df['Amount'] = df['Amount'].str.replace(',', '').astype(int)
    grouped = df.groupby('Council Member').apply(lambda x: x.drop_duplicates(subset=['Amount'])).reset_index(drop=True)
    total_amounts = grouped.groupby('Council Member')['Amount'].sum().map('${:,.2f}'.format)
    stats = pd
