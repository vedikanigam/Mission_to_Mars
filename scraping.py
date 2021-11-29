import pandas as pd
from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager
executable_path = {'executable_path': ChromeDriverManager().install()}

def scrape_all():
    
    browser = Browser('chrome', **executable_path, headless=False)
    data = {}
    title, paragraph = news(browser)
    data['title'] = title
    data['paragraph'] = paragraph
    data['image'] = image(browser)
    data['facts'] = facts()
    data['hemisphere'] = hemisphere_all(browser)
    browser.quit()
    return data

# ### Visit the NASA Mars News Site
def news(browser):
    browser = Browser('chrome', **executable_path, headless=False)
    browser.visit('https://redplanetscience.com/')
    return browser.find_by_css('div.content_title').text, browser.find_by_css('div.article_teaser_body').text

# ### JPL Space Images Featured Image
def image(browser):
    browser.visit('https://spaceimages-mars.com')
    browser.find_by_tag('button')[1].click()
    return browser.find_by_css('img.fancybox-image')['src']

# ### Mars Facts
def facts():
    df = pd.read_html('https://galaxyfacts-mars.com')[0]
    df.columns=['Description', 'Mars', 'Earth']
    df.set_index('Description', inplace=True)
    return df.to_html()


# # D1: Scrape High-Resolution Mars’ Hemisphere Images and Titles
def hemisphere_all(browser):
    browser.visit('https://marshemispheres.com/')
    hemispheres = []
    for i in range(4):
        hemisphere = {}
        hemisphere['title'] = browser.find_by_css('a.itemLink h3')[i].text
        browser.find_by_css('a.itemLink h3')[i].click()
        hemisphere['url'] = browser.find_by_text('Sample')['href']
        browser.back()
        hemispheres.append(hemisphere)
    return hemispheres
    
if __name__ == "__main__":
    # If running as script, print scraped data
    print(scrape_all())





