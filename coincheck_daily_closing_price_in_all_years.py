import time
from selenium import webdriver
from selenium.webdriver.support.ui import Select
import pandas as pd

options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--disable-extensions')
options.add_argument('--blink-settings=imagesEnabled=false')
options.add_argument('--no-sandbox')
options.add_argument('--log-level=3')
options.page_load_strategy = 'eager' #https://www.selenium.dev/ja/documentation/webdriver/capabilities/shared/


def scrape_closing_price(coin_param): 
    all_year_data = pd.DataFrame()

    for y in range(9): #When I wrote this script, 9 is a good parameter(the number of showed years(2014~2022) on the Coincheck website, which is 9) to get BTC price.

        for m in range (12):

            time.sleep(1)
            driver = webdriver.Chrome('./chromedriver.exe', options=options)
            driver.implicitly_wait(5)
            driver.get("https://coincheck.com/ja/exchange/closing_prices")

            #select year pulldown option and get label text which correspond to value
            y_pd = driver.find_element_by_xpath("//div[@class = 'table-top']/div/select[@class = 'year ng-pristine ng-untouched ng-valid']")
            y_pd_select = Select(y_pd)
            y_pd_select.select_by_value(str(y))
            time.sleep(2)

            option_element = driver.find_element_by_xpath("//div[@class = 'table-top']/div/select/option[@value = '" + str(y+3) + "']")
            label_year = option_element.text

            #select month pulldown option
            m_pd = driver.find_element_by_xpath("//div[@class = 'table-top']/div/select[@class = 'month ng-pristine ng-untouched ng-valid']")
            m_pd_select = Select(m_pd)
            m_pd_select.select_by_value(str(m))
            time.sleep(2)

            #get date values
            date_values = driver.find_elements_by_xpath("//tbody/tr/th[@class = 'fixed ng-binding']")
            date = [str(label_year) + "/" + s.text for s in date_values]   #https://qiita.com/waterada/items/2aa4aa14140a8d0542f3
            date = pd.DataFrame(date) 

            #get price values
            price_values = driver.find_elements_by_xpath("//tbody/tr/td[@class = 'ng-binding ng-scope']")
            prices = [s.text for s in price_values]

            #retreive only btc price(needs adjustment later)
            closing_price = []
            for n in range(date.size): 
                
                hoge = (n * 23) + coin_param
                closing_price.append(prices[hoge])
                    
            closing_price = pd.DataFrame(closing_price)
            print(closing_price)

            for_append = pd.DataFrame(pd.concat([date, closing_price], axis=1, ignore_index = True))
            all_year_data = pd.DataFrame(pd.concat([all_year_data, for_append], axis=0, ignore_index = True))
            driver.quit()

    all_year_data.to_csv("coincheck_daily_closing_price.csv")


scrape_closing_price(3)
# please set parameter following the information below. 
#0--BTC, 1--ETH, 2--ETC, 3--LSK, 4--XRP, 5--XEM, 6--LTC, 7--BCH, ... 