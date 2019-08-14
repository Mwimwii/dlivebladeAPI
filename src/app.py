import os, sys

sys.path.append("/opt")
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

from lxml import html
import time
import csv
from datetime import datetime

url = "https://dlive.tv/s/browse"
SCROLL_PAGE_TIME = 3


def handler(event, context):
    # Setup web driver and chrome binary
    options = Options()
    options.binary_location = '/opt/bin/headless-chromium'
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--single-process')
    options.add_argument('--disable-gpu')
    options.add_argument('--window-size=1280x1696')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36')
    print(sys.path)
    driver = webdriver.Chrome('/opt/bin/chromedriver', chrome_options=options)
    print(os.listdir('/opt'))

    print("SCRAPE STARTED")
    # get the epoch time from the 1970.
    now = datetime.utcnow()
    driver.get(url)

    try:
        myElem = WebDriverWait(driver, SCROLL_PAGE_TIME).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.category-card.margintb-4')))
        print ("Page is ready!")
    except TimeoutException:
        print ("Loading took too much time!")

    new_length = driver.execute_script(
        "return (document.getElementsByClassName('category-card margintb-4')).length") - 1
    time.sleep(SCROLL_PAGE_TIME)
    print ("Length: {}".format(new_length))
    last_length = 0
    try:
        while last_length != new_length:
            # Scroll down to bottom
            last_length = new_length
            driver.execute_script(
                "(document.getElementsByClassName('category-card margintb-4')[{}]).scrollIntoView()".format(
                    new_length - 2))
            print(new_length)
            # Wait to load page
            time.sleep(SCROLL_PAGE_TIME)
            # Calculate new scroll height and compare with last scroll height
            new_length = driver.execute_script(
                "return (document.getElementsByClassName('category-card margintb-4')).length") - 1
    except:
        driver.close()
        driver.quit()

    #parse
    dlive_page_content = driver.execute_script("return document.body.innerHTML")
    tree = html.fromstring(dlive_page_content)

    titles = tree.xpath("//div[@class='text-12-medium text-white overflow-ellipsis']/text()")
    image_urls = tree.xpath("//img[@class='category-image position-absolute width-100 height-100']/@src")[1:]
    viewer_count = tree.xpath("//span[@place='Num']/text()")
    parsed_d = lambda unparsed: ([i.split("\n")[1].strip(" ") for i in unparsed])
    titles_parsed = ([i.split("\n")[1].strip(" ") for i in titles])[1:]
    viewer_count_parsed = ([int(i.split("\n")[1].strip(" ").replace(",", "")) for i in viewer_count])
    list_now = [now] * len(titles_parsed)
    collection = list(zip(list_now, titles_parsed, viewer_count_parsed))
    print(collection)
    # print(viewer_count)
    # print(image_urls)
    driver.close()
    driver.quit()

    # response = {
    #     "statusCode": 200,
    #     "body": body
    # }
    # print (body)
