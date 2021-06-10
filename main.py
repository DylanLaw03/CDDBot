'''
This program will scrape a page from the website cheap digital download, to find potentially profiatble games.
Started on 6/9/21
'''
#import dependencies
from selenium import webdriver

#Define x_path variables. These are the names of the x_paths that contain the information needed
test_urls = ["https://cheapdigitaldownload.com/gta-5-digital-download-price-comparison/", "https://cheapdigitaldownload.com/rust-digital-download-price-comparison/"]
row_xpath = '//*[@id="offer_offer"]'


def main ():
    print(get_content(test_urls, row_xpath))

def get_content(urls, x_path):
    webelements = []

    driver = webdriver.Firefox()

    for url in urls:
        print(url)
        url_info = [] #index 0 holds url, 1 holds the list of web elements
        driver.get(url)
        listings = driver.find_elements_by_xpath(x_path)

        url_info.append(url)
        url_info.append(listings)
        webelements.append(url_info)

    return webelements

    '''
    This function opens the given url with webdriver, and gets the class content for the specified id
    @param url to open, and class_id to look for
    @returns a list of WebElement object lists where index 0 is the link
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
                    price.append(item)
        
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

        
        


main()
