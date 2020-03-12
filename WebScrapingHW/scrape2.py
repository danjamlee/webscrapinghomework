import pandas as pd
import time
from splinter import Browser
from bs4 import BeautifulSoup


def scrape():
    browser = Browser("chrome", executable_path="chromedriver", headless=False)
    newstitle, newsparagraph = news(browser)

#list what you have
    data = {
        "title": newstitle,
        "paragraph": newsparagraph,
        "image": image(browser),
        "hemisphere": hemisphere(browser),
        "facts": facts()
    }
    browser.quit()
    return data


def news(browser):
    url = 'https://mars.nasa.gov/news'
    browser.visit(url)
    time.sleep(1)
    browser.is_element_present_by_css("ul.item_list li.slide", wait_time=1)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    elements = soup.select_one('ul.item_list li.slide')
    
    newstitle = elements.find('div', class_ = 'content_title').get_text()
    newsparagraph = elements.find("div", class_="article_teaser_body").get_text()

    return newstitle, newsparagraph


def image(browser):
    url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url)

    finalimage = browser.find_by_id("full_image")
    finalimage.click()

    browser.is_element_present_by_text("more info", wait_time=0.5)
    more_info_elem = browser.find_link_by_partial_text("more info")
    more_info_elem.click()


    html = browser.html
    soup = BeautifulSoup(html, "html.parser")

    # print(f"\n\n{soup.find('figure')}\n\n")
    
    # relative image
    imgurl = soup.select_one('figure.lede a').get('href')
    # print(soup.select_one('figure.lede a')) 

    # try:
    #     img_url_rel = imgurl

    # except AttributeError:
    #     return None


    images = f"https://www.jpl.nasa.gov{imgurl}"

    return images


def hemisphere(browser):

    url = ("https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars")
    browser.visit(url)
    time.sleep(1)
    img_url = []
    links = browser.find_by_css("a.product-item h3")

    for i in range(len(links)):
        #url items
        items = {}
        browser.find_by_css("a.product-item h3")[i].click()
        
        #url from what you clicked
        sample_elem = browser.find_link_by_text('Sample').first
        items['img_url'] = sample_elem['href']
        items['title'] = browser.find_by_css("h2.title").text
        
        #append
        img_url.append(items)
        browser.back()

    return(img_url)

# def scrapehemi(html_text):
#     soup = BeautifulSoup(html_text, "html.parser")

#         title = soup.find("h2", class_="title").get_text()
#         sample = soup.find("a", text="Sample").get("href")

#     img_url = {
#         "title": title,
#         "img_url": sample
#     }

#     return img_url


def facts():
    df = pd.read_html("http://space-facts.com/mars/")[0]

    df.columns = ["description", "value"]
    df.set_index("description", inplace=True)

    return df.to_html(classes="table table-striped")


if __name__ == "__main__":

    # If running as script, print scraped data
    print(scrape())
