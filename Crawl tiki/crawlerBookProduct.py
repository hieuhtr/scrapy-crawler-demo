# -*- coding: utf-8 -*-

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from pyvirtualdisplay import Display

import pymongo
from pymongo import MongoClient

def correct_url(url):
    if not url.startswith("http://") and not url.startswith("https://"):
        url = "http://" + url
    return url


def scrollDown(browser, numberOfScrollDowns):
    body = browser.find_element_by_tag_name("body")
    while numberOfScrollDowns >= 0:
        body.send_keys(Keys.PAGE_DOWN)
        numberOfScrollDowns -= 1
    return browser


def crawl_url(url, db):
    
    url = correct_url(url)
    browser = webdriver.Chrome()
    browser.get(url)
    browser = scrollDown(browser, 10)

    hover_element = browser.find_element_by_class_name("special-price-item")

        
    product_price = hover_element.get_attribute("data-value")
    print product_price
        # add_tikilink(db, product_link)



    browser.quit()

def get_db():
    from pymongo import MongoClient
    client = MongoClient('localhost:27017')
    db = client.tiki10000
    return db

def add_tikilink(db, product_link):
    db.tikilink10000.insert({"name" : product_link})
    
def get_country(db):
    return db.tikilink10000.find_one()

if __name__ == '__main__':
    db = get_db()
    url = "http://tiki.vn/muu-tri-xu-the-nguoi-xua-theo-binh-phap-va-cuoc-song-p135076.html"
    crawl_url(url, db)
