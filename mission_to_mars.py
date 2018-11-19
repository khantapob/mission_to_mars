# Dependencies
from splinter import Browser
from bs4 import BeautifulSoup as bs
import time
import requests
import pandas as pd

def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "chromedriver"}
    return Browser("chrome", **executable_path, headless=False)

def scrape_info():

    mars_data = {}
    browser = init_browser()

# NASA Mars News

    url = 'https://mars.nasa.gov/news'

    # Retrieve page with the requests module
    response = requests.get(url)

    # Create BeautifulSoup object; parse with 'html.parser'
    soup = bs(response.text, 'html.parser')

    # Latest News Title from NASA Mars News Site
    news_title = soup.find('div', class_='content_title').text
    news_p = soup.find('div', class_='rollover_description_inner').text
    print(news_title)
    print(news_p)

    # JPL Mars Space Images
    nasa_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(nasa_url)

    nasa_html = browser.html
    nasa_soup = bs(nasa_html, "lxml")

    image_url = "https://www.jpl.nasa.gov/"
    featured = nasa_soup.find_all('img')[9]["src"]

    featured_image_url = image_url + featured
    print(featured_image_url)

    #Mars Weather

    url_weather = "https://twitter.com/marswxreport?lang=en"
    browser.visit(url_weather)

    weather_html = browser.html
    soup = bs(weather_html, "lxml")

    weather = soup.find('p', class_="tweet-text").text

    print(weather)

    #Mars Fact
    url_facts = "https://space-facts.com/mars/"
    table = pd.read_html(url_facts)
    table

    mars_facts = table[0]
    mars_facts.columns = ['Description', 'Value']
    mars_facts.head()

    # Reset index 
    mars_facts = mars_facts.set_index('Description')
    mars_facts.head()

    mars_facts.to_html('mars_facts.html')

    # Mars Hemispheres

    executable_path = {'executable_path': 'chromedriver'}
    browser = Browser('chrome', **executable_path, headless=False)

    # Scrape astrogeology.usgs.gov 
    hemisphere_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(hemisphere_url)

    hemisphere_html = browser.html
    hemisphere_soup = bs(hemisphere_html, 'lxml')
    base_url ="https://astrogeology.usgs.gov"

    images = hemisphere_soup.find_all('div', class_='item')


    hemisphere_image_urls = []

    for image in images:
    
        hemisphere_dict = {}
        
        href = image.find('a', class_='itemLink product-item')
        link = base_url + href['href']
        browser.visit(link)
        
        time.sleep(1)
        
        hemisphere_html2 = browser.html
        hemisphere_soup2 = bs(hemisphere_html2, 'lxml')
        
        title = hemisphere_soup2.find('div', class_='content').find('h2', class_='title').text
        hemisphere_dict['title'] = title
        
        img_url = hemisphere_soup2.find('div', class_='downloads').find('a')['href']
        hemisphere_dict['url_img'] = img_url
    
        hemisphere_image_urls.append(hemisphere_dict)
      
    # Store data in a dictionary
    mars_data = {
        "news_title": news_title,
        "news_p": news_p,
        "featured_image_url": featured_image_url,
        "weather": weather,
        # "mars_facts": mars_facts,
        "hemisphere_image_urls": hemisphere_image_urls
    }

    # Close the browser after scraping
    browser.quit()

    # Return results
    return mars_data