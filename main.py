'''
This program will scrape a page from the website cheap digital download, to find potentially profiatble games.
Started on 6/9/21
'''
#import dependencies
from selenium import webdriver
import os
from datetime import date

test_urls2 = ["https://cheapdigitaldownload.com/days-gone-digital-download-price-comparison/", "https://cheapdigitaldownload.com/minecraft-digital-download-price-comparison/", "https://cheapdigitaldownload.com/resident-evil-village-editions-a-2021-04/", "https://cheapdigitaldownload.com/battlefield-5-digital-download-price-comparison/"]
test_urls = ["https://cheapdigitaldownload.com/days-gone-digital-download-price-comparison/"]
row_xpath = '//*[@id="offer_offer"]'
HOME_STORE = 'G2A'
WORKING_DIRECTORY = 'c://Users//18022//Desktop//Python//CDD//reports'
MIN_PROFIT = 1.5 #the minimum value for profit_margin to put a report in the flagged folder

def main ():
    #move to wd
    '''
    os.chdir(WORKING_DIRECTORY)
    #create a folder for the date, and within that have two folders, one called flagged to hold listing_pages with a value >= MIN_PROFIT and one for all other reports
    os.mkdir(str(date.today()))
    #move to new directory
    os.chdir(str(date.today()))
    print(os.getcwd())
   #make new folders
    os.mkdir("flagged")
    os.mkdir("all")
'''

    #iterate through all urls 
    for url in test_urls:
    #use get content to get a list of lists comtaining links and web elements
        content = get_content(url, row_xpath)
        game_name = url[33:-1] #will be used for making folder
        
        #get price info
        info = get_price_info(content[0])
        print(info)

        
    
'''
    content = get_content(test_urls, row_xpath)[0][1]
    price_info = get_price_info(content)
    lp = Listing_Page(create_listing_list(price_info))
    print(lp.get_profit_margin())
'''

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

def create_listing_list(listing_info_list):
    loop_control = 0
    listings = []
    for listing in listing_info_list[0]:
        store = listing_info_list[0][loop_control]
        region = listing_info_list[1][loop_control]
        version = listing_info_list[2][loop_control]
        price = listing_info_list[3][loop_control]
        listings.append(Listing(store, region, version, price))
        loop_control += 1
    
    return listings
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

class Listing_Page():

    #This class takes a list of listings that make up a whole page, and will contain metrics for determining if it is a good deal
    def __init__(self, listings):
        self.listings = listings
        for listing in self.listings:
            if listing.get_store() == HOME_STORE:
                self.home_listing = listing

        #Go through each listing to see find the lowest
        self.cheapest_listing = self.home_listing
        for listing in self.listings:
            if listing.get_price() < self.cheapest_listing.get_price():
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
    

main()