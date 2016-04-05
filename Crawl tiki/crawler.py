# -*- coding: utf8 -*-
import sys
reload(sys)  
sys.setdefaultencoding('UTF-8')

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from pyvirtualdisplay import Display

from Queue import Queue
from time import time

import pymongo
from pymongo import MongoClient

queue_book_link = Queue()

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


def get_url(url):
    
    url = correct_url(url)
    browser = webdriver.Chrome()
    browser.get(url)
    browser = scrollDown(browser, 10)

    all_hover_elements = browser.find_elements_by_class_name("product-item")

    for hover_element in all_hover_elements:
        a_element = hover_element.find_element_by_tag_name("a")
        # product_title = a_element.get_attribute("title").encode('utf-8')
        product_link = a_element.get_attribute("href")
        # print product_link

        queue_book_link.put(product_link)
        # Add to store-link database
        # add_tikilink(db, product_link)

    browser.close()
    browser.quit()

def crawl_product_data(url):
    url = correct_url(url)
    browser = webdriver.Chrome()
    browser.get(url)
    browser = scrollDown(browser, 10)

    item_box = browser.find_element_by_class_name("item-box")

    title = item_box.find_element_by_tag_name("h1").text.encode('UTF-8')
    #print title

    original_price = item_box.find_element_by_class_name("old-price-item").get_attribute("data-value")
    #print original_price

    special_price = item_box.find_element_by_class_name("special-price-item").get_attribute("data-value")
    #print special_price

    try:
        rating = browser.find_element_by_class_name("total-review-point").text.encode('UTF-8')
        #print rating
    except Exception:
        rating = ""
        #print rating
    
    try:
        number_of_rating = browser.find_element_by_class_name("comments-count").find_element_by_tag_name("a").text.encode('UTF-8')
        #print number_of_rating
    except Exception:
        number_of_rating = "" 
        #print number_of_rating
    
    try:
        description_all = browser.find_element_by_id("gioi-thieu").find_elements_by_tag_name("p")[1].text.encode('UTF-8')
        #print number_of_rating
    except Exception:
        description_all = "" 
        #print description_all

    info = (url, title, original_price, special_price, rating, number_of_rating, description_all)

    # Add to store-link database
    add_product_info(db, info)
    
    browser.close()
    browser.quit()

def get_db():
    from pymongo import MongoClient
    client = MongoClient('localhost:27017')
    db = client.tikiBook1000_version3
    return db

def add_product_info(db, info):

    url, title, original_price, special_price, rating, number_of_rating, description_all = info
    db.product_info.insert(
        {"url" : url, "title" :title, "original_price" : original_price, "special_price" : special_price, "rating" : rating, "number_of_rating" : number_of_rating, "description_all" : description_all})
    
if __name__ == '__main__':
    db = get_db()
    
    start_time = time()

    url = "http://tiki.vn/sach-truyen-tieng-viet/c316/?order=name%2Casc&limit=1000"
    get_url(url)

    while not queue_book_link.empty():
        try:
            crawl_product_data(queue_book_link.get())
        except Exception:
            pass

    end_time = time()
    estimated_time = end_time - start_time
    print estimated_time