'''
Rumaisa Abdulhai
Created: April 2020
Modified: May 2020

Program that gets volunteer information
from the allforgood website.

Saves the data to the dataset directory. 
If the file name does not exist, creates a
new dataset.
'''

# Useful Links:
# Intro to Webscraping: https://www.youtube.com/watch?v=XQgXKtPSzUI
# Dynamic Scraping: https://www.youtube.com/watch?v=5cPOONZzflM
# Setup Chrome Driver with Selenium: https://www.edureka.co/community/52315/how-to-setup-chrome-driver-with-selenium-on-macos
# Latest Chrome Driver: https://chromedriver.storage.googleapis.com/index.html?path=80.0.3987.106/

###########
# IMPORTS #
###########
from bs4 import BeautifulSoup as soup
from selenium import webdriver
import time
from datetime import date
from csv import writer
import os
import geopy as gp
from selenium.webdriver.support.wait import WebDriverWait

# URL of the Website being Scraped
URL = 'https://www.allforgood.org/search'

# Specifies the # of times "See More Projects" is clicked
NUM_CLICKED = 30

# Specifies the # of seconds to wait
SLEEP_TIME = 5

#  Paths
dir_path = os.path.dirname(os.path.realpath(__file__))
rel_path = '/Datasets/'
file_name = 'Dataset.csv'

###############
# GET CONTENT #
###############
def getContent(url):
    '''
    Returns the webpage as a BeautifulSoup.

    Parameters:
    -----------
    url (str): The url of the webpage.
    '''

    # Settings for the Chrome Driver
    options = webdriver.chrome.options.Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(options=options, executable_path='/usr/local/bin/chromedriver')
    
    # Waits for 10 seconds
    wait = WebDriverWait(driver, 10)

    # Pass in URL to Driver
    driver.get(url)

    # For the number of times the "See More Projects" is clicked
    for i in range(NUM_CLICKED):
        try:
            loadMoreLink = driver.find_element_by_link_text("See More Projects"); # Try to find link element by text
            time.sleep(SLEEP_TIME)
            loadMoreLink.click() # Click the link
            time.sleep(SLEEP_TIME)
            print("Clicked")
        except Exception:
            break
        
    time.sleep(SLEEP_TIME)
    content = driver.page_source.encode('utf-8').strip()
    page_soup = soup(content,"lxml") # Capture the live HTML code
    driver.quit() # Quit driver

    return page_soup

#############
# GET CARDS #
#############
def getCards(url):
    '''
    Returns the volunteer cards.

    Parameters:
    -----------
    url (str): The url of the webpage.
    '''

    cards = [] # Initializing the list of volunteer cards

    # For each volunteer card, get soup (HTML) with method defined earlier.
    for card in getContent(url).findAll("article", {"class": "search-card search"}):

        # Get Title of Volunteer Card
        title = card.span.span.a.text

        # Initializing all other info list in Colunteer Card
        description = []

        # Gets link associated with each opportunity
        ext_url = card.span.span.a.get('href')
        
        # Looking for a specific website to scrape from 
        # because code was written to scrape from one specific website only
        if "createthegood.aarp.org" in ext_url:
            
            # Gets HTML code from the external url that 
            # contains all other info (description, contact info, location, etc)
            # of the opportunity.
            ext_soup = getContent(ext_url)

            # Only gets the neccessary content for each opportunity
            content = ext_soup.find("div", {"class": "sharp-c-volunteer-opportunity-details__body"})

            # Looks for all <p> tags in content
            for text in content.findAll("p"):
                description.append(text.text) # Appends to the description list

            # Gets "More info" Link
            link = content.find('a', href=True, text='Click here')
            if link != None:
                link = link['href']
            else:
                link = ""

            # Append each volunteer card as a list of information that contains 
            # the title, all other info, and the more info link.
            cards.append([title,description,link])
            print("Appending " + title + "\n")

    return cards # Return the list of volunteer cards

################
# FORMAT CARDS #
################
def formatCards(cards):
    '''
    Returns the formatted volunteer cards.

    Parameters:
    -----------
    cards (list): The list of unformatted cards.
    '''
    
    # Initializing list of formatted volunteer cards
    new_cards = []

    # For each unformatted card
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
        longitude_id = ""
        latitude_id = ""
        
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

        # LATITUDE AND LONGITUDE
        latitude_label = "Latitude:"
        longitude_label = "Longitude:"
        locator = gp.Nominatim(user_agent="myGeocoder", timeout=10) # Initializes Nominatim Geolocation Service
        if locator.geocode(address) != None:
            # Geolocate a query to an address and coordinates
            location = locator.geocode(address)
            latitude_id = location.latitude
            longitude_id = location.longitude

        # DESCRIPTION
        description_label = "Description:"
        description = '\n'.join(card[1]).replace(skills_str, "").replace(date_str, "").replace(organizer_str, "").replace(address_str, "").replace(contact_str, "").replace(more_info_str, "").strip('\n')
        
        # All the Labels
        keys =  [   title_label,
                    description_label,
                    skills_label,
                    date_label,
                    where_label,
                    organizer_label,
                    address_label,
                    contact_label,
                    more_info_label,
                    upload_date_label,
                    latitude_label,
                    longitude_label  ]

        # Corresponding values
        values = [  title,
                    description,
                    skills,
                    date_time,
                    where,
                    organizer,
                    address,
                    contact,
                    more_info,
                    upload_date,
                    latitude_id,
                    longitude_id  ]

        # APPEND TO CSV
        append_to_csv(file_name, keys, values, rel_path)

        # MAKE FORMATTED VOLUNTEER CARD
        new_cards.append(values)

    return new_cards

####################
# PRINT BASE CARDS #
####################
def printCards(cards):
    '''
    Prints the unformatted volunteer cards.

    Parameters:
    -----------
    cards (list): The list of unformatted cards.
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

#####################
# PRINT FINAL CARDS #
#####################
def printFormattedCards(cards):
    '''
    Prints the formatted volunteer cards.

    Parameters:
    -----------
    cards (list): The list of formatted cards.
    '''

    # Call formatCards method
    cards = formatCards(cards)

    count = 0
    for card in cards:
        count+=1
        print("CARD: " + str(count) + '\n')
        print("TITLE: " + str(card[0]) + '\n')
        print("DESCRIPTION:\n" + str(card[1]) + '\n')
        print("SKILLS:" + str(card[2]) + '\n')
        print("DATE: " + str(card[3]) + '\n')
        print("WHERE: " + str(card[4]) + '\n')
        print("ORGANIZER: " + str(card[5]) + '\n')
        print("ADDRESS: " + str(card[6]) + '\n')
        print("CONTACT: " + str(card[7]) + '\n')
        print("MORE INFO: " + str(card[8]) + '\n')
        print("UPLOAD DATE: " + str(card[9]) + '\n')
        print("LATITUDE: " + str(card[10]) + '\n')
        print("LONGITUDE: " + str(card[11]) + '\n')
        print("------------------------------------\n")

#################
# APPEND TO CSV #
#################
def append_to_csv(file_name, keys, values, rel_path):
    '''
    Appends data to csv.

    Parameters:
    -----------
    file_name (str): The desired file name for the data file.
    keys (list): The labels for the opportunity information.
    values (list): The actual opportunity information.
    rel_path (str): The relative path of the current directory.
    '''

    path_file = dir_path + rel_path + file_name # Gets absolute path

    # If directory already exists, then append to file
    if os.path.exists(path_file):
        with open(path_file, 'a', newline='') as write_obj:
            csv_writer = writer(write_obj)
            csv_writer.writerow(values)

    # Else create and make a new file
    else:
        with open(path_file, 'w', newline='') as write_obj:
            csv_writer = writer(write_obj)
            csv_writer.writerow([key.strip(':') for key in keys])
            csv_writer.writerow(values)

########
# MAIN #
########
def main():
    '''
    Main function that starts the scraping.
    '''
    cards = getCards(URL) # Gets formatted Cards
    printFormattedCards(cards) # Prints Formatted Cards

if __name__ == '__main__':
    main()