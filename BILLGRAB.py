from bs4 import BeautifulSoup
import requests

def perfect_bill_grab(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    spans = soup.find_all('span')
    start_flag = False
    end_flag = False
    bills = []
    for span in spans:
        if not start_flag:
            if span.text == 'PERFECTION OF BILLS':
                start_flag = True
        else:
            if span.text == 'FINAL PASSAGE OF BILLS':
                end_flag = True
                break
            else:
                bills.append(span.text)
    if not start_flag:
        print('Text not found. "PERFECTION OF BILLS" not found in the document.')
    elif not end_flag:
        print('Text not found. "FINAL PASSAGE OF BILLS" not found in the document.')
    else:
        print('Bills extracted successfully from the document.')
    return bills

def final_bill_grab(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    spans = soup.find_all('span')
    start_flag = False
    end_flag = False
    bills = []
    for span in spans:
        if not start_flag:
            if span.text == 'FINAL PASSAGE OF BILLS':
                start_flag = True
        else:
            if span.text == 'RESOLUTIONS':
                end_flag = True
                break
            else:
                bills.append(span.text)
    if not start_flag:
        print('Text not found. "FINAL PASSAGE OF BILLS" not found in the document.')
    elif not end_flag:
        print('Text not found. "RESOLUTIONS" not found in the document.')
    else:
        print('Bills extracted successfully from the document.')
    return bills
