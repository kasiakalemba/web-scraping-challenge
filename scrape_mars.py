from bs4 import BeautifulSoup
from splinter import Browser
import requests
import pandas as pd
import os
import time


# Browser init Function
def init_browser():
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    return(Browser("chrome", **executable_path, headless=True))

# Windows Users
# executable_path = {'executable_path': 'chromedriver.exe'}
# browser = Browser('chrome', **executable_path, headless=False)

# Scrape Mars Function

def scrape():
    browser = init_browser()

    # Create a Mars Dictionary
    mars_dict = {}
    
# # Mars News
    #Visit Mars News
    url_mars = "https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"
    
    browser.visit(url_mars)
    time.sleep(5)

    # Scrape page into Soup
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")

    # Mars news title
    news_title = soup.find(class_="list_text").find_all(target="_self")[0].text

    # Mars paragraph content
    news_paragraph = soup.find(class_="list_text").find_all(class_="article_teaser_body")[0].text

    # Mars dictionary
    mars_dict['title'] = news_title
    mars_dict['paragraph'] = news_paragraph


# # JPL Featured Space Image
    # Visit Space Picture
    url_nasa = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    base_nasa = "https://www.jpl.nasa.gov/"
    
    browser.visit(url_nasa)
    time.sleep(5)
    
    # Scrape page into Soup
    html = browser.html
    soup = BeautifulSoup(html,"html.parser")

    # Find Image
    mars_img =soup.find('a', class_="button fancybox").get('data-fancybox-href')
    featured_image_url_2 = base_nasa + mars_img
    
    # Mars picture dictionary
    mars_dict['featured_img'] = featured_image_url_2


# # # Mars Weather
#     # Visit Mars Twitter
#     url_twitter = "https://twitter.com/marswxreport?lang=en"
#     result = requests.get(url_twitter)
#     time.sleep(5)

    
#     html = result.text
#     soup = BeautifulSoup(html, 'html.parser')
    

#     # Find First Tweet
#     mars_weather = soup.find(class_='tweet-text').get_text()

#     # Mars picture dictionary
#     mars_dict['mars_weather'] = mars_weather


# # Mars Facts
    # Visit Mars Facts
    url_space = "https://space-facts.com/mars/"
    
    browser.visit(url_space)
    time.sleep(5)

    # Read HTML
    space = pd.read_html(url_space)
    
    # Make dataframe
    space_df = space[0]
    space_df.set_index(0, inplace=True)
    space_df.index.names = [None]
    space_df.columns = ['Specifics']
    
    # Convert to HTML
    html = space_df.to_html()
    html_clean = html.replace('\n', '')
    
    # Append the table to the dictionary
    mars_dict['table'] = html_clean

# # Mars Hemispheres
    
    hemispheres_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(hemispheres_url)
    time.sleep(5)

    html = browser.html
    soup = BeautifulSoup(html, "html.parser")

    items = soup.find_all('div', class_="item")
    hemis_urls = []

    for item in items:
        title = (item.find('h3').text).replace(' Enhanced', '')
        browser.click_link_by_partial_text(title)
        soup = BeautifulSoup(browser.html, 'html.parser')
        
        full = soup.find('a', text='Sample')
        img_url = full['href']
        
        hemis_urls.append({'title': title, 'img_url': img_url})
        browser.back()

    #close browser
    browser.quit()

    mars_dict['hemis_urls'] = hemis_urls

    return mars_dict
    
#print(scrape())
