'''
This program will scrape a page from the website cheap digital download, to find potentially profiatble games.
Started on 6/9/21
'''
#import dependencies
from selenium import webdriver

#Define x_path variables. These are the names of the x_paths that contain the information needed
x_path_price = '//*[@id="offer_has_coupon"]/div[2]/span[2]'



def main ():
    pass

def get_content(url, class_id):
    driver = webdriver.Firefox()
    driver.get(url)
    listings = driver.find_elements_by_class_name(class_id)

    for listing in listings:
        price = listing.find_element_by_class_name('x-offer-price')
        print(price)
        print('iteration complete')

    print("test")
    '''
    This function opens the given url with webdriver, and gets the class content for the specified id
    @param url to open, and class_id to look for
    '''

get_content("https://cheapdigitaldownload.com/gta-5-digital-download-price-comparison/","offers-table-row x-offer")

