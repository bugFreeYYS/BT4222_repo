import pickle
import json
import datetime
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

import time
output = dict()

base = datetime.datetime.today()
numdays = 3
date_list = [(base - datetime.timedelta(days=x)).strftime('%m/%d/%Y') for x in range(numdays)]
# print(date_list)
driver = webdriver.Chrome('/Users/bolin/Desktop/NUS Y4S2/BT4222/Bitcoin Scraper/chromedriver')

for date in date_list:
    driver.get('https://www.google.com/search?rlz=1C5CHFA_enSG857SG857&biw=1252&bih=1001&tbm=nws&sxsrf=ALeKk01WJ9KVpEaOLElQuoxvFIXyU0Ye_w%3A1612095496103&ei=CKAWYLrqBcj6rQGD4L6oBw&q=bitcoin&oq=bitcoin&gs_l=psy-ab.3...0.0.0.238750.0.0.0.0.0.0.0.0..0.0....0...1c..64.psy-ab..0.0.0....0.Ewp5Y2WlQvM')
    time.sleep(10)
    id_count = 0
    output[date] = dict()
    print('Processing date: {}'.format(date))
    driver.find_element_by_xpath('//*[@id="hdtb-tls"]').click()
    time.sleep(1)
    driver.find_element_by_xpath('//*[@id="hdtbMenus"]/div/span[1]').click()
    time.sleep(1)
    driver.find_element_by_xpath('//*[@id="lb"]/div/g-menu/g-menu-item[8]/div/div/span').click()

    start_date = driver.find_element_by_xpath('//*[@id="OouJcb"]').send_keys(date)
    end_date = driver.find_element_by_xpath('//*[@id="rzG2be"]').send_keys(date)
    driver.find_element_by_xpath('//*[@id="T3kYXe"]/g-button').click()
    time.sleep(3)
            
    main_section = driver.find_element_by_id('search')
    boxes = main_section.find_elements_by_class_name('dbsr')
    for box in boxes:
        id_count = id_count + 1
        output[date][id_count] = dict()
        contents = box.text.split('\n')
        news_agency = contents[0]
        title = contents[1]
        header = contents[2]
        output[date][id_count]['news_agency'] = news_agency
        output[date][id_count]['title'] = title
        output[date][id_count]['header'] = header



    hasNext = True
    while hasNext:
        try:
            driver.find_element_by_xpath('//*[@id="pnnext"]/span[2]').click()
            time.sleep(2)
            main_section = driver.find_element_by_id('search')
            boxes = main_section.find_elements_by_class_name('dbsr')
            for box in boxes:
                id_count = id_count + 1
                output[date][id_count] = dict()
                contents = box.text.split('\n')
                news_agency = contents[0]
                title = contents[1]
                header = contents[2]
                output[date][id_count]['news_agency'] = news_agency
                output[date][id_count]['title'] = title
                output[date][id_count]['header'] = header
        except:
            hasNext = False


with open('articles.json', 'w') as outfile:
    json.dump(output, outfile)