import time
import warnings
from selenium import webdriver
from selenium.webdriver.support.ui import Select
import pandas as pd

warnings.simplefilter("ignore")
options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--disable-extensions')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--disable-gpu')
options.add_argument('--blink-settings=imagesEnabled=false')
options.add_argument('--no-sandbox')
options.add_argument('--log-level=3')
options.page_load_strategy = 'eager' #https://www.selenium.dev/ja/documentation/webdriver/capabilities/shared/

def scrapeing_HFT(y,m):
    global HFT_data
    global reference
    global date
    global cryptocurrency
    global trading_pair_text

    for d in range(1):
        
        d = int(d) + 1

        driver = webdriver.Chrome('./chromedriver.exe', options=options)
        driver.implicitly_wait(5)
        driver.get("https://coincheck.com/ja/exchange/rates")

        for h in range(24): #set hour 00:mm ~ 23:mm
            for min in range(12): # set time hh:00~hh:55
                min = int(min * 5)
                    
                #adjustment date format
                if len(str(m)) == 1:
                    m = str("0" + str(m))
                if len(str(d)) == 1:
                    d = str("0" + str(d))
                if len(str(h)) == 1:
                    h = str("0" + str(h))
                if len(str(min)) == 1:
                    min = str("0" + str(min))
                
                #check output_1
                #print(str(y) + "-" + str(m) + "-" + str(d) + " " + str(h) + ":" + str(min))

                #select one trading pair option
                trading_pair = driver.find_element_by_xpath("//div[@class = 'rates-inner']/div[@class = 'row']/div[@class = 'pairs']/span[@class = 'select-box']/select")
                Select(trading_pair).select_by_value(str(cryptocurrency))   #https://qiita.com/oh_rusty_nail/items/9afb124e423e9e12c020
                trading_pair_text = Select(trading_pair).options[cryptocurrency].text
                trading_pair_text = trading_pair_text.replace("/","")
                print(trading_pair_text)

                #select date_year_month_day input option
                y_m_d = driver.find_element_by_xpath("//div[@class = 'rates-inner']/div[@class = 'row']/div[@class = 'datetime']/input[@ng-model = 'datetime']")
                y_m_d.send_keys('00'+ str(y) + '-' + str(m) + '-' + str(d))   #https://qiita.com/oh_rusty_nail/items/9afb124e423e9e12c020

                #select date_time input option
                h_m = driver.find_element_by_xpath("//div[@class = 'rates-inner']/div[@class = 'row']/div[@class = 'datetime']/input[@ng-model = 'time']")
                h_m.send_keys(str(h) + ':' + str(min))   #https://tech-joho.info/typeerror-unsupported-operand-types-for-int-and-str/

                #click search button
                search = driver.find_element_by_xpath("//div[@class = 'rates-inner']/div[@class = 'row']/button")
                driver.execute_script("arguments[0].click();", search) #search this clause
                time.sleep(1)

                #get date and price values
                date_element = driver.find_elements_by_xpath("//div[@class = 'rates-inner']/div[@ng-if = 'result']/div[@class = 'datetime ng-binding']")
                
                if len(date_element) == 0:
                    print("No data but continuing scraping")
                    pass
                else:
                    if  (str(h) + ":" + str(min)) == "00:00":
                        date = date_element[0].text   #https://syachiku.net/selenimumattributeerror-list-object-has-no-attribute-text/

                        price_element = driver.find_elements_by_xpath("//div[@class = 'rates-inner']/div[@ng-if = 'result']/div[@class = 'result-data']/div[@class = 'rate']/span[@class = 'num ng-binding']")
                        price = price_element[0].text

                        day_data = pd.DataFrame([[date, price]])
                        HFT_data = pd.DataFrame(pd.concat([HFT_data, day_data], axis=0, ignore_index = True))
                        
                        #check output_2
                        print(day_data)
                        reference == date

                    else:
                        date = date_element[0].text   #https://syachiku.net/selenimumattributeerror-list-object-has-no-attribute-text/

                        if len(date) == 0:
                            pass
                        else:
                            while date == reference:
                                date_element = driver.find_elements_by_xpath("//div[@class = 'rates-inner']/div[@ng-if = 'result']/div[@class = 'datetime ng-binding']")
                                date = date_element[0].text   #https://syachiku.net/selenimumattributeerror-list-object-has-no-attribute-text/
                                date = reference
                                print(date)
                            else:
                                price_element = driver.find_elements_by_xpath("//div[@class = 'rates-inner']/div[@ng-if = 'result']/div[@class = 'result-data']/div[@class = 'rate']/span[@class = 'num ng-binding']")
                                price = price_element[0].text

                                day_data = pd.DataFrame([[date, price]])
                                HFT_data = pd.DataFrame(pd.concat([HFT_data, day_data], axis=0, ignore_index = True))
                                
                                #check output_2
                                print(day_data) 

        driver.quit()        

#Run
HFT_data = pd.DataFrame()
reference = None
date = None

y = 2021
m = 11
cryptocurrency = 0

scrapeing_HFT(y,m)
HFT_data.to_csv("D:\coincheck_HFT_data_" + str(trading_pair_text) +"\\" + str(y) + "-" + str(m) + ".csv")

#cryptocurrency option number
# BTC/JPY  --- 0
# ETH/JPY  --- 1
# ETC/JPY  --- 2
# LSK/JPY  --- 3
# XRP/JPY  --- 4
# XEM/JPY  --- 5
# LTC/JPY  --- 6
# BCH/JPY  --- 7
# MONA/JPY --- 8
# XLM/JPY  --- 9
# QTUM/JPY --- 10
# BAT/JPY  --- 11
# IOST/JPY --- 12
# ENJ/JPY  --- 13
# OMG/JPY  --- 14
# XYM/JPY  --- 15
# SAND/JPY --- 16
# DOT/JPY  --- 17
# PLT/JPY  --- 18