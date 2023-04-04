import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
import re

URL = 'https://stlouisco.civicweb.net/document/111851/'

def extract_spans(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    spans = soup.find_all('span')
    return spans, soup

def write_spans_to_txt(spans, file_name):
    start_flag = False
    end_flag = False
    sections = ['PERFECTION OF BILLS', 'FINAL PASSAGE OF BILLS']

    with open(file_name, "w", encoding="utf8") as file:
        for span in spans:
            if not start_flag:
                if span.text == sections[0]:
                    start_flag = True
                    sections.pop(0)
            else:
                if span.text == sections[0]:
                    end_flag = True
                    break
                else:
                    file.write(span.text + "\n")  # write span text to file

    if not start_flag:
        print(f'Text not found. "{sections[0]}" not found in the document.')
    elif not end_flag:
        print(f'Text not found. "{sections[0]}" not found in the document.')
    else:
        print(f'Spans written to {file_name}')

def remove_duplicates(spans):
    seen = set()
    result = []
    for span in spans:
        if span.text not in seen:
            seen.add(span.text)
            result.append(span)
    return result

def generate_markdown_table(final_spans):
    headers = ['Bill Number', 'Sponsor', 'Description']
    table = [headers]

    for span in final_spans:
        row = span.text.split('\n', 2)
        if len(row) == 3:
            table.append(row)

    markdown_table = pd.DataFrame(table[1:], columns=table[0]).to_markdown(index=False)
    return markdown_table

def extract_date(soup):
    date_string = soup.find('div', {'class': 'lblTitle'}).text
    match = re.search(r'\b(?:Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|Sep(?:tember)?|Oct(?:ober)?|(?:Nov|Dec)(?:ember)?)\s+\d{1,2},\s+\d{4}\b', date_string)
    if match:
        return match.group()
    return None

if __name__ == '__main__':
    spans, soup = extract_spans(URL)
    write_spans_to_txt(spans, 'perfectionbills.txt')
    final_spans = remove_duplicates(spans)
    write_spans_to_txt(final_spans, 'finalbills.txt')

    # Create the output directory if it doesn't exist
    os.makedirs('output', exist_ok=True)

    # Extract the date from the agenda URL
    date = extract_date(soup)

    # Write the Markdown table to a file
    with open('output/agenda_data.md', 'a', encoding='utf-8') as f:
        if date:
            f.write(f'\nDate: {date}\n')
        f.write(generate_markdown_table(final_spans))
        f.write('\n------\n')  # Add a separator between each run
