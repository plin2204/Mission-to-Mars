# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd # to use .read.html() method
import datetime as dt 
#import traceback # for line 110 to find specific error

# Update the data stored in Mongo each time it's run
def scrape_all():
    
    # Initiate headless driver for deployment
    executable_path = {'executable_path': 'chromedriver'}
    browser = Browser('chrome', **executable_path)
    # Use the following code to avoid auto browsing at chrome
    #browser = Browser("chrome", executable_path="chromedriver", headless=True)

    # Set our news title and paragraph variables
    news_title, news_paragraph = mars_news(browser)
    
    # Run all scraping functions and store results in dictionary
    data = {
          "news_title": news_title,
          "news_paragraph": news_paragraph,
          "featured_image": featured_image(browser),
          "facts": mars_facts(),
          "last_modified": dt.datetime.now()}

    # end auto browsering
    #browser.quit()
    return data

# Set the executable path and initialize the chrome browser in splinter
#executable_path = {'executable_path': 'chromedriver'} 
#browser = Browser('chrome', **executable_path)

def mars_news(browser):

    # Visit the mars nasa news site
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    # Optional delay for loading the page
    browser.is_element_present_by_css("ul.item_list li.slide", wait_time=1)

    # Set up HTML parser
    html = browser.html
    news_soup = BeautifulSoup(html, 'html.parser')
    
    # Add try/except for error handling
    try:
        slide_elem = news_soup.select_one('ul.item_list li.slide')

        # Assign the title n summary text to variables we'll reference later
        #slide_elem.find("div", class_='content_title')

        # Use the parent element to find the first 'a' tag and save it as 'news_title'
        news_title = slide_elem.find("div", class_='content_title').get_text()

        # Use the parent element to find the paragraph text
        news_p = slide_elem.find("div", class_="article_teaser_body").get_text()
    
    except AttributeError:
        
        return None, None
    
    return news_title, news_p

## 10.3.4: Scrape Mars Data: Featured Image
## Featured Images
def featured_image(browser):
    
    # Visit URL
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)

    # Find and click the full image button
    full_image_elem = browser.find_by_id('full_image')
    full_image_elem.click()

    # Find the more info button and click that
    browser.is_element_present_by_text('more info', wait_time=1)

    more_info_elem = browser.find_link_by_partial_text('more info')
    more_info_elem.click()

    # Parse the resulting html with soup
    html = browser.html
    img_soup = BeautifulSoup(html, 'html.parser')

    # try-except for error handling
    try:        
        # Find the relative image url
        img_url_rel = img_soup.select_one('figure.lede a img').get("src")

    except AttributeError:
        return None
    
    # Use the base URL to create an absolute URL
    img_url = f'https://www.jpl.nasa.gov{img_url_rel}'

    return img_url
    
## 10.3.5: Scrape Mars Data: Mars Facts
def mars_facts():
    
    try:
        # Scrape the first table [1]
        df = pd.read_html('http://space-facts.com/mars/')[1]

    except BaseException:
        return None
    #except BaseException as e:
        #return print(str(e))
        #traceback.print_exc()
    
    # Assign columns and set index of dataframe
    df.columns=['Description', 'Mars', 'Earth']
    #df.columns=['Description', 'Mars']
    df.set_index('Description', inplace=True)

    # convert df to html
    return df.to_html()

# end auto browsering
#browser.quit()
# Tells Flask that our script is complete and ready for action
if __name__ == "__main__":
    # If running as script, print scraped data
    print(scrape_all())

