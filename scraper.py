'''
Rumaisa Abdulhai
Date: April 2020

Program that gets volunteer information
from the allforgood website.

Saves the data to the dataset directory. 
If the file name does not exist, creates a
new dataset.
'''

from bs4 import BeautifulSoup as soup
from selenium import webdriver
import time
from datetime import date
from csv import writer
import os

# Useful Links:
# Intro to Webscraping: https://www.youtube.com/watch?v=XQgXKtPSzUI
# Dynamic Scraping: https://www.youtube.com/watch?v=5cPOONZzflM
# Setup Chrome Driver with Selenium: https://www.edureka.co/community/52315/how-to-setup-chrome-driver-with-selenium-on-macos
# Latest Chrome Driver: https://chromedriver.storage.googleapis.com/index.html?path=80.0.3987.106/

URL = 'https://www.allforgood.org/search'
dir_path = os.path.dirname(os.path.realpath(__file__))
rel_path = '/Datasets/'
file_name = 'Dataset.csv'

def getContent(url):
    '''
    Returns the page as a BeautifulSoup.
    '''

    options = webdriver.chrome.options.Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(options=options, executable_path='/usr/local/bin/chromedriver')
    driver.get(url)

    time.sleep(5)
    content = driver.page_source.encode('utf-8').strip()
    page_soup = soup(content,"lxml")
    driver.quit()

    return page_soup

def getCards(url):
    '''
    Returns the volunteer cards.
    '''

    cards = []

    for card in getContent(url).findAll("article", {"class": "search-card search"}):

        # Title
        title = card.span.span.a.text

        # Description 
        description = []
        ext_url = card.span.span.a.get('href')
        ext_soup = getContent(ext_url)
        content = ext_soup.find("div", {"class": "sharp-c-volunteer-opportunity-details__body"})
        for text in content.findAll("p"):
            description.append(text.text)

        link = content.find('a', href=True, text='Click here')
        if link != None:
            link = link['href']
        else:
            link = ""
        cards.append([title,description,link])

    return cards

def formatCards(cards):
    '''
    Returns the formatted volunteer cards.
    '''
    
    new_cards = []
    for card in cards:

        # DATA, in order that they should appear
        title = ""
        description = ""
        skills = ""
        date_time = ""
        where = ""
        organizer = ""
        address = ""
        contact = ""
        more_info = ""
        upload_date = ""
        
        # TITLE
        title_label = "Title:"
        title = card[0]

        # MATCHING SKILLS
        skills_str = ""
        skills_label = "Matching Skills:"
        for line in card[1]:
            if line.startswith(skills_label):
                skills_str = line
        skills = skills_str.replace(skills_label, "")

        # WHERE
        where_str = ""
        where_label = "Where:"
        for line in card[1]:
            if line.find(where_label) != -1:
                where_str = line[line.find(where_label):len(line)]
        where = where_str.replace(where_label, "")

        # DATE TIME
        date_str = ""
        date_label = "Date:"
        for line in card[1]:
            if line.startswith(date_label):
                date_str = line
        date_time = date_str.replace(date_label, "").replace(where_str, "")

        # ORGANIZER
        organizer_str = ""
        organizer_label = "Organized By:"
        for line in card[1]:
            if line.startswith(organizer_label):
                organizer_str = line
        organizer = organizer_str.replace(organizer_label, "")

        # ADDRESS
        address_str = ""
        address_label = "Address:"
        for line in card[1]:
            if line.startswith(address_label):
                address_str = line
        address = address_str.replace(address_label, "")

        # CONTACT INFO
        contact_str = ""
        contact_label = "Contact:"
        for line in card[1]:
            if line.startswith(contact_label):
                contact_str = line
        contact = contact_str.replace(contact_label, "")

        # MORE INFO
        more_info_str = ""
        more_info_label = "More information:"
        for line in card[1]:
            if line.startswith(more_info_label):
                more_info_str = line
        more_info = card[2]

        # UPLOAD DATE
        upload_date_label = "Upload Date:"
        upload_date = date.today().strftime("%m/%d/%y")

        # DESCRIPTION
        description_label = "Description:"
        description = '\n'.join(card[1]).replace(skills_str, "").replace(date_str, "").replace(organizer_str, "").replace(address_str, "").replace(contact_str, "").replace(more_info_str, "").strip('\n')
        
        keys =  [   title_label,
                    description_label,
                    skills_label,
                    date_label,
                    where_label,
                    organizer_label,
                    address_label,
                    contact_label,
                    more_info_label,
                    upload_date_label  ]

        values = [  title,
                    description,
                    skills,
                    date_time,
                    where,
                    organizer,
                    address,
                    contact,
                    more_info,
                    upload_date ]

        # APPEND TO CSV
        append_to_csv(file_name, keys, values, rel_path)

        # MAKE FORMATTED VOLUNTEER CARD
        new_cards.append(values)

    return new_cards

def printCards(cards):
    '''
    Prints the unformatted volunteer cards.
    '''
    
    i=0
    for card in cards:
        i+=1
        print("Card " + str(i))
        print("\tTitle: " + card[0])
        print("\n\tDescription: ")
        for line in card[1]:
            print("\t\t" + line)
        print("\n\n")

def printFormattedCards(cards):
    '''
    Prints the formatted volunteer cards.
    '''

    cards = formatCards(cards)

    count = 0
    for card in cards:
        count+=1
        print("CARD: " + str(count))
        print()
        print("TITLE: " + str(card[0]))
        print()
        print("DESCRIPTION:\n" + str(card[1]))
        print()
        print("SKILLS:" + str(card[2]))
        print()
        print("DATE: " + str(card[3]))
        print()
        print("WHERE: " + str(card[4]))
        print()
        print("ORGANIZER: " + str(card[5]))
        print()
        print("ADDRESS: " + str(card[6]))
        print()
        print("CONTACT: " + str(card[7]))
        print()
        print("MORE INFO: " + str(card[8]))
        print()
        print("UPLOAD DATE: " + str(card[9]))
        print("------------------------------------\n")

def append_to_csv(file_name, keys, values, rel_path):
    '''
    Appends data to csv.
    '''

    path_file = dir_path + rel_path + file_name
    if os.path.exists(path_file):
        with open(path_file, 'a', newline='') as write_obj:
            csv_writer = writer(write_obj)
            csv_writer.writerow(values)
    else:
        with open(path_file, 'w', newline='') as write_obj:
            csv_writer = writer(write_obj)
            csv_writer.writerow([key.strip(':') for key in keys])
            csv_writer.writerow(values)

def main():
    '''
    Main function that starts the scraping.
    '''
    cards = getCards(URL)
    printFormattedCards(cards)

if __name__ == '__main__':
    main()