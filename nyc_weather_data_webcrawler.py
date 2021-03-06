# -*- coding: utf-8 -*-
"""NYC Weather Data WebCrawler.ipynb

Automatically generated by Colaboratory.


## NYC Weather Data WebCrawler
"""

from selenium import webdriver
from bs4 import BeautifulSoup
import time

dict1 = {}

year_list=['2010', '2011', '2012', '2013', '2014',
            '2015', '2016', '2017', '2018', '2019']
month_list = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
              'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

def getDatas():
    

    driver = webdriver.Chrome()
    for y in range(len(year_list)):
        dict1[year_list[y]] = {}
        for o in range(12):
            
            url = "https://www.wunderground.com/history/monthly/KLGA/date/201{}-{}".format(y, o+1)

            driver.get(url)
            time.sleep(3)
            res = driver.page_source

            response = BeautifulSoup(res, 'html.parser')

            datas = response.find_all('table', class_="days ng-star-inserted")

            columns_name = ['Temperature_Max', 'Temperature_Avg', 'Temperature_Min',
                           'Dew_Point_Max', 'Dew_Point_Avg', 'Dew_Point_Min', 
                           'Humidity_Max', 'Humidity_Avg', 'Humidity_Min', 
                           'Wind_Speed_Max', 'Wind_Speed_Avg', 'Wind_Speed_Min', 
                           'Pressure_Max', 'Pressure_Avg', 'Pressure_Min']

            dict1[year_list[y]][month_list[o]] = {}
            dict1[year_list[y]][month_list[o]]['Date'] = {}

            dict1[year_list[y]][month_list[o]]['Temperature_Max'] = {}
            dict1[year_list[y]][month_list[o]]['Temperature_Avg'] = {}
            dict1[year_list[y]][month_list[o]]['Temperature_Min'] = {}

            dict1[year_list[y]][month_list[o]]['Dew_Point_Max'] = {}
            dict1[year_list[y]][month_list[o]]['Dew_Point_Avg'] = {}
            dict1[year_list[y]][month_list[o]]['Dew_Point_Min'] = {}

            dict1[year_list[y]][month_list[o]]['Humidity_Max'] = {}
            dict1[year_list[y]][month_list[o]]['Humidity_Avg'] = {}
            dict1[year_list[y]][month_list[o]]['Humidity_Min'] = {}

            dict1[year_list[y]][month_list[o]]['Wind_Speed_Max'] = {}
            dict1[year_list[y]][month_list[o]]['Wind_Speed_Avg'] = {}
            dict1[year_list[y]][month_list[o]]['Wind_Speed_Min'] = {}

            dict1[year_list[y]][month_list[o]]['Pressure_Max'] = {}
            dict1[year_list[y]][month_list[o]]['Pressure_Avg'] = {}
            dict1[year_list[y]][month_list[o]]['Pressure_Min'] = {}
            dict1[year_list[y]][month_list[o]]['Precipitation'] = {}


            print('loading {}-{} file'.format(year_list[y], month_list[o]))

            # Stracture of table tag:
            # <tbody>
            #   <tr>
            #     <td>
            #       <table>
            #         <tr>
            #           <td>
            #           <td>
            #           <td>
            k = 0
            for k in range(7):
                if k == 0:
                    for text in datas:
                        table = text.find('tbody').find_all('table')[k]
                        j = 0
                        i = 0
                        for item in table:
                            if j > 1:
                                dict1[year_list[y]][month_list[o]]['Date'][i] = item.find('td').get_text().replace(' ','')
                                i += 1
                            j += 1
                elif k == 6:
                    for text in datas:
                        table = text.find('tbody').find_all('table')[k]
                        j = 0
                        i = 0
                        for item in table:
                            if j > 1:
                                dict1[year_list[y]][month_list[o]]['Precipitation'][i] = item.find('td').get_text().replace(' ','')
                                i += 1
                            j += 1
                else:
                    n = (k - 1) * 3
                    for text in datas:
                        temp = text.find('tbody').find_all('table')[k]
                        j = 0
                        i = 0
                        for item in temp:
                            if j != 0:
                                element = item.find_all('td')[0]
                                for e in element:
                                    if i != 0:
                                        dict1[year_list[y]][month_list[o]][columns_name[n]][i-1] = e.replace(' ','')
                                        n += 1
                                element = item.find_all('td')[1]
                                for e in element:
                                    if i != 0:
                                        dict1[year_list[y]][month_list[o]][columns_name[n]][i-1] = e.replace(' ','')
                                        n += 1
                                element = item.find_all('td')[2]
                                for e in element:
                                    if i != 0:
                                        dict1[year_list[y]][month_list[o]][columns_name[n]][i-1] = e.replace(' ','')
                                        n -= 2
                                    i += 1

                            j += 1



    driver.close()
    print('Finished, data saved in dict1.')


getDatas()

import pandas as pd
df = pd.DataFrame()
for y in range(len(year_list)):
    for i in range(len(month_list)):
        df = pd.concat([df, pd.DataFrame(dict1[year_list[i]][month_list[i]])])
    
df = df.reset_index(drop=True).drop(columns=['Date'])
df['Date'] = pd.date_range(start='1/1/2010', end='12/31/2019')
df = df.set_index('Date')
df.to_csv('NYC_weather.csv')