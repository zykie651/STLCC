import re
import pandas as pd
import BILLGRAB
import requests
import os

#Agenda URL 
url = 'https://stlouisco.civicweb.net/document/118713/'

def find_date_in_html_page(url):
    # Make a request to the webpage and get the HTML content
    response = requests.get(url)
    html = response.text

    # Use regular expressions to find the date in the HTML content
    pattern = r"\w+,\s\w+\s\d+,\s\d{4}\s\w+\s\d+:\d+\s\w+"
    match = re.search(pattern, html)

    # If a match is found, return the date string. Otherwise, return None.
    if match:
        return match.group()
    else:
        return None

def generate_markdown_table(df):
    return df.to_markdown(index=False)

def write_output_to_markdown_file(output, file_name):
    with open(file_name, 'a', encoding='utf-8') as f:
        f.write(output)
        f.write('\n------\n')

date = find_date_in_html_page(url)

b = BILLGRAB
b.PERFECTBILLLGRAB(url)
b.FINALBILLGRAB(url)

with open('bills.txt',encoding="utf8") as f:
    text = f.read()

bill_no_pattern = r'BILL NO\. (\d+), (\d+), INTRODUCED BY COUNCIL MEMBER(?:S)? ((?:\w+)(?: AND \w+)*)?, ENTITLED:'
amount_pattern = r'\$([\d,]+)'
purpose_pattern = r'FOR SUPPORT OF (.+)[;|\.]'
source_pattern = r"FROM (?:THE )?([A-Z\s]+)"

bill_no_regex = re.compile(bill_no_pattern)
amount_regex = re.compile(amount_pattern)
purpose_regex = re.compile(purpose_pattern)
source_regex = re.compile(source_pattern)

bill_no = []
council_member = []
amount = []
purpose = []
source = []

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

data = {'Bill Number': bill_no, 
        'Council Member': council_member, 
        'Amount': amount, 
        'Purpose': purpose, 
        'Source': source}
df = pd.DataFrame(data)

df = df[df['Amount'] != '']

output = f'#######################################\nThis is the STL County Council Meeting for:\n{date}\n#######################################\n'
output += generate_markdown_table(df)

print(output)

with pd.ExcelWriter('stlcc.xlsx') as writer:
    df.to_excel(writer, index=False)

def stats(df):
    df['Amount'] = df['Amount'].str.replace(',', '').astype(int)
    grouped = df.groupby('Council Member').apply(lambda x: x.drop_duplicates(subset=['Amount'])).reset_index(drop=True)
    total_amounts = grouped.groupby('Council Member')['Amount'].sum().map('${:,.2f}'.format)
    stats = pd.DataFrame({'Total Amount': total_amounts})
    print(stats)

stats(df)

def main():
    pass

if __name__ == "__main__":
    main()

# Create the output directory if it doesn't exist
os.makedirs('output', exist_ok=True)

# Write the output to the markdown file
write_output_to_markdown_file(output, 'output/agenda_data.md')
