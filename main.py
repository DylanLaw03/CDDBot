'''
This program will scrape a page from the website cheap digital download, to find potentially profiatble games.
Started on 6/9/21
'''
#import dependencies
from selenium import webdriver
import os
from datetime import date


row_xpath = '//*[@id="offer_offer"]'
HOME_STORE = 'G2A'
WORKING_DIRECTORY = 'c://Users//18022//Desktop//Python//CDD'
MIN_PROFIT = 1.7 #the minimum value for profit_margin to put a report in the flagged folder
BANNED_STORES = ['Microsoft', 'Epic Games', 'Steam', 'Gog.com', 'Kinguin', 'G2A']
def main ():
    os.chdir(WORKING_DIRECTORY)

    #open link_getter file, and append that to urls
    urls = []
    link_getter_file_name = 'link_getter - ' + str(date.today()) + '.txt'
    with open(link_getter_file_name, 'r') as link_file:
        Lines = link_file.readlines()
        for line in Lines:
            urls.append(line)

    os.chdir('./reports')

    #create a folder for the date, and within that have two folders, one called flagged to hold listing_pages with a value >= MIN_PROFIT and one for all other reports
    os.mkdir(str(date.today()))
    #move to new directory
    os.chdir(str(date.today()))
   #make new folders
    os.mkdir("flagged")
    os.mkdir("all")


    #iterate through all urls 
    for url in urls:
        url = url[:-2]
        dir_control = 0 #if set to 1, do not go back one directory at the end of the loop

    #use get content to get a list of lists comtaining links and web elements
        content = get_content(url, row_xpath)
        game_name = url[33:] #will be used for making folder
        text_doc_name = game_name + ".txt"
        
        #get price info
        price_info = get_price_info(content[0][1]) #first return item, second item in that list. 
        #close web driver
        content[1].close()
        #verify that HOME_STORE in price_info[0]
        if HOME_STORE in price_info[0]:
            #create listing page
            listing_page = create_listing_page(price_info)
            #If profit margin > min profit, move to flagged, if not move to all.
            if listing_page.profit_margin > MIN_PROFIT:
                os.chdir('flagged')
            else:
                os.chdir('all')
        
        #now create a text document with game_name as the name
            
        else:
            print(f'{HOME_STORE} listing was not found for {game_name}')
            dir_control = 1
            continue
        #open file and print info

        text_document = open(text_doc_name, 'w+')
        text_document.write(f'Report for {game_name}, created on {date.today()}\n\n\n')
        text_document.write(f'Profit Margin: {round(listing_page.get_profit_margin(), 2)}\n\n')

        #print info for home listing
        text_document.write('Home Store: \n')
        text_document.write('Store: ')
        text_document.write(listing_page.get_home_listing().get_store())
        text_document.write('\nVersion: ')
        text_document.write(listing_page.get_home_listing().get_version())
        text_document.write('\nRegion: ')
        text_document.write(listing_page.get_home_listing().get_region())
        text_document.write('\nPrice: ')
        text_document.write(str(listing_page.get_home_listing().get_price()))

        #print info for cheapest listing
        text_document.write('\n\nCheapest Store: \n')
        text_document.write('Store: ')
        text_document.write(listing_page.get_cheapest_listing().get_store())
        text_document.write('\nVersion: ')
        text_document.write(listing_page.get_cheapest_listing().get_version())
        text_document.write('\nRegion: ')
        text_document.write(listing_page.get_cheapest_listing().get_region())
        text_document.write('\nPrice: ')
        text_document.write(str(listing_page.get_cheapest_listing().get_price()))

        #Create header for all listings
        text_document.write('\n\n\nListings:\n\n')
        text_document.write(format('Store', '<20'))
        text_document.write(format('Version', '<20'))
        text_document.write(format('Region', '<20'))
        text_document.write(format('Price', '<20'))
        text_document.write(format('Profit Ratio', '<20'))
        text_document.write(format('\n'))

        for listing in listing_page.get_listings():
            text_document.write(format(listing.get_store(), '<20'))
            text_document.write(format(listing.get_version(), '<20'))
            text_document.write(format(listing.get_region(), '<20'))
            text_document.write('$')
            text_document.write(format(listing.get_price(), '<19'))
            text_document.write(format(round(listing_page.get_home_listing().get_price() / listing.get_price(), 2), '<15'))
            text_document.write('\n')
        text_document.close()
                
        
        #go back to dir for the day

        if dir_control == 0:
            os.chdir('..')

        print(f'Process Completed for {game_name}! The profit ratio was {round(listing_page.get_profit_margin(), 2)}')



def get_content(url, x_path):

    driver = webdriver.Firefox()


    url_info = [] #index 0 holds url, 1 holds the list of web elements
    driver.get(url)
    listings = driver.find_elements_by_xpath(x_path)

    url_info.append(url)
    url_info.append(listings)

    
    return url_info, driver

    '''
    This function opens the given url with webdriver, and gets the class content for the specified id
    @param url to open, and class_id to look for
    @returns a list of WebElement object lists where index 0 is the link, and driver in index one, so that it can be closed
    '''

def get_price_info(web_element_list):
    return_list = []
    store = []
    region = []
    version = []
    price = []
    for listing in web_element_list:
        loop_control = 0 #set to 1 when the price is found
        listing_text = listing.text
        listing_text = listing_text.split('\n')
        #append store, region, and version to their respective lists. located at index 0, 3, and 4.
        store.append(listing_text[0])
        region.append(listing_text[3])
        version.append(listing_text[4])
        
        for item in listing_text[5:]:
                if item[0] == '$' and loop_control == 0:
                    loop_control = 1
                    price.append(item[1:])
        
    return_list.append(store)
    return_list.append(region)
    return_list.append(version)
    return_list.append(price)

    return return_list

    '''
    This function takes a list of WebElements and parses their .text to find the store, region, version, and price
    @param a list of WebElements
    @return a list where index 0 is store, 1 is region, 2 is version, and 3 is price
    '''

def create_listing_page(listing_info_list):
    loop_control = 0
    listings = []
    for listing in listing_info_list[0]:
        store = listing_info_list[0][loop_control]
        region = listing_info_list[1][loop_control]
        version = listing_info_list[2][loop_control]
        price = listing_info_list[3][loop_control]
        listings.append(Listing(store, region, version, price))
        loop_control += 1
    
    return Listing_Page(listings)
    '''
    This function creates a Listing_Page object
    @param it takes a list from get_price_info where index 0 is store, 1 is region, 2 is version, and 3 is price
    @return Listing_Page class
    '''

class Listing():
    #The listing class will be used to make up the listing_page class. It contains price, store, region, and version for each listing.

    def __init__ (self, store, region, version, price):
        self.store = store
        self.region = region
        self.version = version
        self.price = float(price)
    
    def get_store(self):
        return self.store
    
    def get_region (self):
        return self.region
    
    def get_version (self):
        return self.version
    
    def get_price (self):
        return self.price
    
    def equals (self, object2):
        if object2.get_region() == self.region and object2.get_version() == self.version:
            return True
        return False

class Listing_Page():

    #This class takes a list of listings that make up a whole page, and will contain metrics for determining if it is a good deal
    def __init__(self, listings):
        self.home_listing = None
        self.listings = listings

        for listing in self.listings:
            if listing.get_store() == HOME_STORE and self.home_listing == None:
                self.home_listing = listing

        #Go through each listing to see find the lowest
        if self.home_listing != None:
            self.cheapest_listing = self.home_listing
            for listing in self.listings:
                #verify that price is lower than current cheapest, that store is not banned, and that the listing is equal to home store.
                if listing.get_price() < self.cheapest_listing.get_price() and listing.get_store() not in BANNED_STORES and listing.equals(self.home_listing):
                    self.cheapest_listing = listing

            self.profit_margin = self.home_listing.get_price() / self.cheapest_listing.get_price()
        #Find the listing that matches the name for HOME_STORE. Set it equal to self.home_store
    

    def get_home_listing (self):
        return self.home_listing
    
    def get_home_price(self):
        return self.home_price
    
    def get_cheapest_listing(self):
        return self.cheapest_listing

    def get_profit_margin (self):
        return self.profit_margin
    
    def get_listings (self):
        return self.listings
    

main()