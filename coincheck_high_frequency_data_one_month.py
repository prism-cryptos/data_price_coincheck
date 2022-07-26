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

    for d in range(31):
        d = int(d) + 1

        for h in range(24): #set hour 00:mm ~ 23:mm
            for min in range(12): # set time hh:00~hh:55
                min = int(min * 5)
                
                time.sleep(1)
                driver = webdriver.Chrome('./chromedriver.exe', options=options)
                driver.implicitly_wait(10)
                driver.get("https://coincheck.com/ja/exchange/rates")
                    
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

                #select date_year_month_day input option
                y_m_d = driver.find_element_by_xpath("//div[@class = 'rates-inner']/div[@class = 'row']/div[@class = 'datetime']/input[@ng-model = 'datetime']")
                y_m_d.send_keys('00'+ str(y) + '-' + str(m) + '-' + str(d))   #https://qiita.com/oh_rusty_nail/items/9afb124e423e9e12c020

                #select date_time input option
                h_m = driver.find_element_by_xpath("//div[@class = 'rates-inner']/div[@class = 'row']/div[@class = 'datetime']/input[@ng-model = 'time']")
                h_m.send_keys(str(h) + ':' + str(min))   #https://tech-joho.info/typeerror-unsupported-operand-types-for-int-and-str/

                #click search button
                search = driver.find_element_by_xpath("//div[@class = 'rates-inner']/div[@class = 'row']/button")
                search.click()

                try:
                    #get date and price values
                    date_element = driver.find_elements_by_xpath("//div[@class = 'rates-inner']/div[@ng-if = 'result']/div[@class = 'datetime ng-binding']")
                    date = date_element[0].text   #https://syachiku.net/selenimumattributeerror-list-object-has-no-attribute-text/

                    price_element = driver.find_elements_by_xpath("//div[@class = 'rates-inner']/div[@ng-if = 'result']/div[@class = 'result-data']/div[@class = 'rate']/span[@class = 'num ng-binding']")
                    price = price_element[0].text

                    day_data = pd.DataFrame([[date, price]])
                    HFT_data = pd.DataFrame(pd.concat([HFT_data, day_data], axis=0, ignore_index = True))

                    #check output_2
                    print(day_data) 
                except:
                    pass

                driver.quit()               

#Run
HFT_data = pd.DataFrame()
y = 2020
m = 2
scrapeing_HFT(y,m)
HFT_data.to_csv("D:\coincheck_HFT_data_BTCJPY\\" + str(y) + "-" + str(m) + ".csv")