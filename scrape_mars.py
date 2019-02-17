    #!/usr/bin/env python
# coding: utf-8

# # Mission to Mars 
# ## Web Scraping Assignment by John Zhao 

# In[1]:


# Import dependencies ('boilerplate')
import pandas as pd
import requests
from bs4 import BeautifulSoup as bs
from splinter import Browser
import time

# # Step 1: Scraping
# ## I. NASA Mars News

def scrape():

# In[2]:


    # URL
    url = 'https://mars.nasa.gov/news/'

    # Creating a response
    response = requests.get(url)

    # Create BeautifulSoup object, parsed to HTML
    soup = bs(response.text, "html.parser")

    # Results of scraping
    news_title = soup.find('div', class_='content_title').text
    news_content = soup.find('div', class_='rollover_description_inner').text
    print(news_title,
          news_content)


    # ## II. JPL Mars Space Images - Featured Image

    # In[3]:


    # Setup for Splinter
    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    browser = Browser('chrome', **executable_path, headless=False)

    # Target URL
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)

    # BS object
    html = browser.html
    soup = bs(html, 'html.parser')

    # Click through to image
    browser.click_link_by_partial_text('FULL IMAGE')
    time.sleep(3)
    browser.click_link_by_partial_text('more info')
    time.sleep(3)
    browser.click_link_by_partial_text('.jpg')
    time.sleep(3)


    # In[4]:


    # Save image link using BS object
    html2 = browser.html
    soup2 = bs(html2, 'html.parser')
    featured_image_url = soup2.find('img').get('src')
    print(f'The featured image URL is {featured_image_url}')


    # ## III. Mars Weather

    # In[5]:


    # Scrape data from Twitter handle
    tw_rs = requests.get('https://twitter.com/marswxreport?lang=en')
    tw_soup = bs(tw_rs.text, 'html.parser')

    # Find text
    mars_weather = tw_soup.find('p', class_='TweetTextSize TweetTextSize--normal js-tweet-text tweet-text').text
    print(mars_weather)


    # ## IV. Mars Facts

    # In[6]:


    # Use Pandas to read HTML from specified URL
    mars_table = pd.read_html('http://space-facts.com/mars/')
    mars_table


    # In[7]:


    # Find table's type
    print(type(mars_table))

    # Use first table
    mars_df = mars_table[0]

    # Set column names and then set index to 'Data Type'
    mars_df.columns = ['Data Type', 'Information']
    mars_df.set_index('Data Type', inplace=True)

    # Convert table to HTML
    mars_html = mars_df.to_html()


    # In[8]:


    # Replace '\n' for a cleaner string
    mars_html = mars_html.replace('\n', '')
    mars_html

    # Optional step to open HTML file in browser
    # mars_df.to_html('mars_info.html')
    # ! open mars_info.html


    # ## V. Mars Hemispheres

    # In[10]:


    # Target URL
    tgt_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'

    # Creating a response
    hemi_response = requests.get(tgt_url)

    # Create BeautifulSoup object, parsed to HTML
    hemi_soup = bs(hemi_response.text, "html.parser")

    # Find all instances of the hemispheres
    hemi_attrs = hemi_soup.find_all('a', class_='itemLink product-item')
    print(hemi_attrs)


    # In[11]:


    # Create 'for loop' to retrieve title and image's URL
    # Put items into empty list
    hemi_info = []
    for x in hemi_attrs:
        # Title's text in <h3>
        title = x.find('h3').text
        # Image's link
        img_link = 'https://astrogeology.usgs.gov/' + x['href']
        # Getting a response
        img_request = requests.get(img_link)
        # Setup BS object
        img_soup = bs(img_request.text, 'html.parser')
        # Find URL
        img_hres = img_soup.find('div', class_='downloads')
        img_url = img_hres.find('a')['href']
        # Append all info
        hemi_info.append({'Title': title, 'Image URL': img_url})


    # In[12]:

    print(hemi_info)

    mars_info = {'News Title': news_title,
                'News Content': news_content,
                'Most Recent Image': featured_image_url,
                'Mars Weather': mars_weather,
                'Hemisphere Info': hemi_info}

    return mars_info



