# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager

import pandas as pd
import numpy as np
import requests
import re

#Set executable path
executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)


# Visit the mars nasa news site
url = 'https://redplanetscience.com'
browser.visit(url)
# Optional delay for loading page
browser.is_element_present_by_css('div.list_text', wait_time=1)


#Setup HTML parser
html = browser.html
news_soup = soup(html, 'html.parser')
slide_elem = news_soup.select_one('div.list_text')

slide_elem.find('div', class_='content_title')


# Use the parent element to find the first `a` tag and same it as `news_title`
news_title = slide_elem.find('div', class_='content_title').get_text()
news_title


# Use the parent element to find the paragraph text
news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
news_p


# ### Featured Images


# Visit URL
url = 'https://spaceimages-mars.com'
browser.visit(url)


# Find and click the Full Image button
full_image_elem = browser.find_by_tag('button')[1]
full_image_elem.click()


#Parse the restuling html with soup
html = browser.html
img_soup = soup(html, 'html.parser')


#Find the realtive impage url
img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
img_url_rel


#Use the base URL to create an absolute URL
img_url = f'https://spaceimages-mars.com/{img_url_rel}'
img_url


# Visit Mars Facts URL
url = 'https://galaxyfacts-mars.com'
browser.visit(url)


df = pd.read_html('https://galaxyfacts-mars.com')[0]
df.columns = ['description', 'Mars', 'Earth']
df.set_index('description', inplace=True)
df


df.to_html()


# # D1: Scrape High-Resolution Mars’ Hemisphere Images and Titles\


# 1. Use browser to visit the URL 
executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)
url = 'https://marshemispheres.com/'

browser.visit(url)


# 2. Create a list to hold the images and titles.
hemisphere_image_urls = []

# 3. Write code to retrieve the image urls and titles for each hemisphere.
html = browser.html
image_soup = soup(html, 'html.parser')

# thumbs = browser.find_by_tag('img')
image_div = image_soup.find_all('div', class_="description")

for div in image_div:
    hemispheres = {}
    image_page = div.find('a', class_="itemLink").get('href')

    new_url = f'https://marshemispheres.com/{image_page}'
    browser.visit(new_url)

    # Save page html to parse
    html = browser.html
    page_soup = soup(html, 'html.parser')

    # Save Image .jpg
    div_down = page_soup.find('div', class_='downloads')

    img_url_rel = div_down.find('a', target="_blank").get('href')

    img_url = f'https://marshemispheres.com/{img_url_rel}'

    # Find and save Hemisphere title
    title = page_soup.find('h2', class_='title').text

    hemispheres["title"]=(title)
    hemispheres["image url"]=(img_url)
    # Nav back to original page
    browser.visit(url)
    hemisphere_image_urls.append(hemispheres)


# 4. Print the list that holds the dictionary of each image url and title.
hemisphere_image_urls


# 5. Quit the browser
browser.quit()

