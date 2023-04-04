from bs4 import BeautifulSoup
import requests

def PERFECTBILLLGRAB(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    spans = soup.find_all('span')
    start_flag = False
    end_flag = False

    with open("bills.txt", "w", encoding="utf8") as file:
        for span in spans:
            if not start_flag:
                if span.text == 'PERFECTION OF BILLS':
                    start_flag = True
            else:
                if span.text == 'FINAL PASSAGE OF BILLS':
                    end_flag = True
                    break
                else:
                    file.write(span.text + "\n") # write span text to file

    if not start_flag:
        print('Text not found. "FINAL PASSAGE OF BILLS" not found in the document.')
    elif not end_flag:
        print('Text not found. "RESOLUTIONS" not found in the document.')
    else:
        print('Spans written to perfectionbills.txt')

def FINALBILLGRAB(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    spans = soup.find_all('span')
    start_flag = False
    end_flag = False

    with open("bills.txt", "a", encoding="utf8") as file:
        for span in spans:
            if not start_flag:
                if span.text == 'FINAL PASSAGE OF BILLS':
                    start_flag = True
            else:
                if span.text == 'RESOLUTIONS':
                    end_flag = True
                    break
                else:
                    file.write(span.text + "\n") # write span text to file

    if not start_flag:
        print('Text not found. "FINAL PASSAGE OF BILLS" not found in the document.')
    elif not end_flag:
        print('Text not found. "RESOLUTIONS" not found in the document.')
    else:
        print('Spans written to finalbills.txt')
