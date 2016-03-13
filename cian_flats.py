# -*- coding: utf-8 -*-
"""
Created on Sun Jan 31 23:01:00 2016

@author: Dmitry Sergeyev
"""

import requests
import re
from bs4 import BeautifulSoup
import pandas as pd
import time

start = time.time()

allflats_stat = {a: {} for a in range(10000)}
allflats = {}
zero_km = [55.755831, 37.617673]


districts = ['http://www.cian.ru/cat.php?deal_type=sale&district%5B0%5D=13&district%5B1%5D=14&district%5B2%5D=15&district%5B3%5D=16&district%5B4%5D=17&district%5B5%5D=18&district%5B6%5D=19&district%5B7%5D=20&district%5B8%5D=21&district%5B9%5D=22&engine_version=2&offer_type=flat&p=', '&utm_expid=57940811-35.TtLzqtysSXetoMiJ4499HA.0&utm_referrer=http%3A%2F%2Fwww.cian.ru%2Fcat.php%3Fdeal_type%3Dsale%26district%255B0%255D%3D13%26district%255B1%255D%3D14%26district%255B2%255D%3D15%26district%255B3%255D%3D16%26district%255B4%255D%3D17%26district%255B5%255D%3D18%26district%255B6%255D%3D19%26district%255B7%255D%3D20%26district%255B8%255D%3D21%26district%255B9%255D%3D22%26engine_version%3D2%26offer_type%3Dflat',
             'http://www.cian.ru/cat.php?deal_type=sale&district%5B0%5D=23&district%5B1%5D=24&district%5B10%5D=33&district%5B11%5D=34&district%5B12%5D=35&district%5B13%5D=36&district%5B14%5D=37&district%5B15%5D=38&district%5B2%5D=25&district%5B3%5D=26&district%5B4%5D=27&district%5B5%5D=28&district%5B6%5D=29&district%5B7%5D=30&district%5B8%5D=31&district%5B9%5D=32&engine_version=2&offer_type=flat&p=', '&utm_expid=57940811-35.TtLzqtysSXetoMiJ4499HA.0&utm_referrer=http%3A%2F%2Fwww.cian.ru%2Fcat.php%3Fdeal_type%3Dsale%26district%255B0%255D%3D23%26district%255B10%255D%3D33%26district%255B11%255D%3D34%26district%255B12%255D%3D35%26district%255B13%255D%3D36%26district%255B14%255D%3D37%26district%255B15%255D%3D38%26district%255B1%255D%3D24%26district%255B2%255D%3D25%26district%255B3%255D%3D26%26district%255B4%255D%3D27%26district%255B5%255D%3D28%26district%255B6%255D%3D29%26district%255B7%255D%3D30%26district%255B8%255D%3D31%26district%255B9%255D%3D32%26engine_version%3D2%26offer_type%3Dflat',
             'http://www.cian.ru/cat.php?deal_type=sale&district%5B0%5D=39&district%5B1%5D=40&district%5B10%5D=49&district%5B11%5D=50&district%5B12%5D=51&district%5B13%5D=52&district%5B14%5D=53&district%5B15%5D=54&district%5B16%5D=55&district%5B2%5D=41&district%5B3%5D=42&district%5B4%5D=43&district%5B5%5D=44&district%5B6%5D=45&district%5B7%5D=46&district%5B8%5D=47&district%5B9%5D=48&engine_version=2&offer_type=flat&p=','&utm_expid=57940811-35.TtLzqtysSXetoMiJ4499HA.0&utm_referrer=http%3A%2F%2Fwww.cian.ru%2Fcat.php%3Fdeal_type%3Dsale%26district%255B0%255D%3D39%26district%255B10%255D%3D49%26district%255B11%255D%3D50%26district%255B12%255D%3D51%26district%255B13%255D%3D52%26district%255B14%255D%3D53%26district%255B15%255D%3D54%26district%255B16%255D%3D55%26district%255B1%255D%3D40%26district%255B2%255D%3D41%26district%255B3%255D%3D42%26district%255B4%255D%3D43%26district%255B5%255D%3D44%26district%255B6%255D%3D45%26district%255B7%255D%3D46%26district%255B8%255D%3D47%26district%255B9%255D%3D48%26engine_version%3D2%26offer_type%3Dflat',
             'http://www.cian.ru/cat.php?deal_type=sale&district%5B0%5D=56&district%5B1%5D=57&district%5B10%5D=66&district%5B11%5D=67&district%5B12%5D=68&district%5B13%5D=69&district%5B14%5D=70&district%5B15%5D=71&district%5B2%5D=58&district%5B3%5D=59&district%5B4%5D=60&district%5B5%5D=61&district%5B6%5D=62&district%5B7%5D=63&district%5B8%5D=64&district%5B9%5D=65&engine_version=2&offer_type=flat&p=','&utm_expid=57940811-35.TtLzqtysSXetoMiJ4499HA.0&utm_referrer=http%3A%2F%2Fwww.cian.ru%2Fcat.php%3Fdeal_type%3Dsale%26district%255B0%255D%3D56%26district%255B10%255D%3D66%26district%255B11%255D%3D67%26district%255B12%255D%3D68%26district%255B13%255D%3D69%26district%255B14%255D%3D70%26district%255B15%255D%3D71%26district%255B1%255D%3D57%26district%255B2%255D%3D58%26district%255B3%255D%3D59%26district%255B4%255D%3D60%26district%255B5%255D%3D61%26district%255B6%255D%3D62%26district%255B7%255D%3D63%26district%255B8%255D%3D64%26district%255B9%255D%3D65%26engine_version%3D2%26offer_type%3Dflat',
             'http://www.cian.ru/cat.php?deal_type=sale&district%5B0%5D=72&district%5B1%5D=73&district%5B10%5D=82&district%5B11%5D=83&district%5B2%5D=74&district%5B3%5D=75&district%5B4%5D=76&district%5B5%5D=77&district%5B6%5D=78&district%5B7%5D=79&district%5B8%5D=80&district%5B9%5D=81&engine_version=2&offer_type=flat&p=','&utm_expid=57940811-35.TtLzqtysSXetoMiJ4499HA.0&utm_referrer=http%3A%2F%2Fwww.cian.ru%2Fcat.php%3Fdeal_type%3Dsale%26district%255B0%255D%3D72%26district%255B10%255D%3D82%26district%255B11%255D%3D83%26district%255B1%255D%3D73%26district%255B2%255D%3D74%26district%255B3%255D%3D75%26district%255B4%255D%3D76%26district%255B5%255D%3D77%26district%255B6%255D%3D78%26district%255B7%255D%3D79%26district%255B8%255D%3D80%26district%255B9%255D%3D81%26engine_version%3D2%26offer_type%3Dflat',
             'http://www.cian.ru/cat.php?deal_type=sale&district%5B0%5D=84&district%5B1%5D=85&district%5B10%5D=94&district%5B11%5D=95&district%5B12%5D=96&district%5B13%5D=97&district%5B14%5D=98&district%5B15%5D=99&district%5B2%5D=86&district%5B3%5D=87&district%5B4%5D=88&district%5B5%5D=89&district%5B6%5D=90&district%5B7%5D=91&district%5B8%5D=92&district%5B9%5D=93&engine_version=2&offer_type=flat&p=','&utm_expid=57940811-35.TtLzqtysSXetoMiJ4499HA.0&utm_referrer=http%3A%2F%2Fwww.cian.ru%2Fcat.php%3Fdeal_type%3Dsale%26district%255B0%255D%3D84%26district%255B10%255D%3D94%26district%255B11%255D%3D95%26district%255B12%255D%3D96%26district%255B13%255D%3D97%26district%255B14%255D%3D98%26district%255B15%255D%3D99%26district%255B1%255D%3D85%26district%255B2%255D%3D86%26district%255B3%255D%3D87%26district%255B4%255D%3D88%26district%255B5%255D%3D89%26district%255B6%255D%3D90%26district%255B7%255D%3D91%26district%255B8%255D%3D92%26district%255B9%255D%3D93%26engine_version%3D2%26offer_type%3Dflat',
             'http://www.cian.ru/cat.php?deal_type=sale&district%5B0%5D=100&district%5B10%5D=110&district%5B11%5D=111&district%5B1%5D=101&district%5B2%5D=102&district%5B3%5D=103&district%5B4%5D=104&district%5B5%5D=105&district%5B6%5D=106&district%5B7%5D=107&district%5B8%5D=108&district%5B9%5D=109&engine_version=2&offer_type=flat&p=','&utm_expid=57940811-35.TtLzqtysSXetoMiJ4499HA.0&utm_referrer=http%3A%2F%2Fwww.cian.ru%2Fnd%2Fsearch%2F%3Fdeal_type%3Dsale%26district%255B0%255D%3D84%26district%255B1%255D%3D85%26district%255B10%255D%3D94%26district%255B11%255D%3D95%26district%255B12%255D%3D96%26district%255B13%255D%3D97%26district%255B14%255D%3D98%26district%255B15%255D%3D99%26district%255B2%255D%3D86%26district%255B3%255D%3D87%26district%255B4%255D%3D88%26district%255B5%255D%3D89%26district%255B6%255D%3D90%26district%255B7%255D%3D91%26district%255B8%255D%3D92%26district%255B9%255D%3D93%26engine_version%3D2%26offer_type%3Dflat%26p%3D2',
             'http://www.cian.ru/cat.php?deal_type=sale&district%5B0%5D=112&district%5B1%5D=113&district%5B10%5D=122&district%5B11%5D=123&district%5B12%5D=124&district%5B2%5D=114&district%5B3%5D=115&district%5B4%5D=116&district%5B5%5D=117&district%5B6%5D=118&district%5B7%5D=119&district%5B8%5D=120&district%5B9%5D=121&engine_version=2&offer_type=flat&p=','&utm_expid=57940811-35.TtLzqtysSXetoMiJ4499HA.0&utm_referrer=http%3A%2F%2Fwww.cian.ru%2Fcat.php%3Fdeal_type%3Dsale%26district%255B0%255D%3D112%26district%255B10%255D%3D122%26district%255B11%255D%3D123%26district%255B12%255D%3D124%26district%255B1%255D%3D113%26district%255B2%255D%3D114%26district%255B3%255D%3D115%26district%255B4%255D%3D116%26district%255B5%255D%3D117%26district%255B6%255D%3D118%26district%255B7%255D%3D119%26district%255B8%255D%3D120%26district%255B9%255D%3D121%26engine_version%3D2%26offer_type%3Dflat',
             'http://www.cian.ru/cat.php?deal_type=sale&district%5B0%5D=125&district%5B1%5D=126&district%5B2%5D=127&district%5B3%5D=128&district%5B4%5D=129&district%5B5%5D=130&district%5B6%5D=131&district%5B7%5D=132&engine_version=2&offer_type=flat&p=','&utm_expid=57940811-35.TtLzqtysSXetoMiJ4499HA.0&utm_referrer=http%3A%2F%2Fwww.cian.ru%2Fcat.php%3Fdeal_type%3Dsale%26district%255B0%255D%3D125%26district%255B1%255D%3D126%26district%255B2%255D%3D127%26district%255B3%255D%3D128%26district%255B4%255D%3D129%26district%255B5%255D%3D130%26district%255B6%255D%3D131%26district%255B7%255D%3D132%26engine_version%3D2%26offer_type%3Dflat']



link_part = 0
flat_id = 0
for a in range(9):
    links = []
    for page in range(1, 30):
        page_url =  districts[link_part+a]+str(page)+districts[link_part+1+a]    
        
        search_page = requests.get(page_url)
        search_page = search_page.content
        search_page = BeautifulSoup(search_page)
        
        flat_urls = search_page.findAll('div', attrs = {'ng-class':"{'serp-item_removed': offer.remove.state, 'serp-item_popup-opened': isPopupOpen}"})
        flat_urls = re.split('http://www.cian.ru/sale/flat/|/" ng-class="', str(flat_urls))
        
        for link in flat_urls:
            if link.isdigit():
                links.append(link)
    link_part+=1
    
    
    for link in range(0, len(links)):
        try:
            flat_url = 'http://www.cian.ru/sale/flat/' + str(links[link]) + '/'
            
            flat_page = requests.get(flat_url)
            flat_page = flat_page.content
            flat_page = BeautifulSoup(flat_page)
            
            flat_id += 1 
            
            allflats_stat[flat_id]['District'] = a
            
            # Метро и всё, что с ним связано
            metro = flat_page.find('div', attrs = {'class':'object_descr_metro'})
            metro = re.split('target="_blank">|</a>', str(metro))[1]
            allflats_stat[flat_id]['Metro'] = metro
            
            metro = flat_page.find('span', attrs = {'class':'object_item_metro_comment'})
            metro = re.split('\W', str(metro))
            
            allflats_stat[flat_id]['Walk'] = 0
            for p in metro:
                if p.isdigit():
                    allflats_stat[flat_id]['Metrdist'] = int(p)
                
                if 'пешк' in p:
                    allflats_stat[flat_id]['Walk'] = 1
                elif allflats_stat[flat_id]['Walk'] != 1:
                    allflats_stat[flat_id]['Walk'] = 0
                
            
            # Координаты 
            coords = flat_page.find('div', attrs={'class':'map_info_button_extend'}).contents[1]
            coords = re.split('&amp|center=|%2C', str(coords))
            #allflats_stat[flat_id]['coords'] = []
            coords_list = []
            for item in coords:
                if item[0].isdigit():
                    coords_list.append(item)
                    #allflats_stat[flat_id]['coords'].append(item)
            lat = abs(float(coords_list[0]) - float(zero_km[0])) * (40074/360)
            lon = abs(float(coords_list[1]) - float(zero_km[1])) * (40074/360) * 0.022126756261955736
            distance = (lat ** 2 + lon ** 2) ** 0.5
            allflats_stat[flat_id]['distance'] = distance
            # Цена
            price = flat_page.find('div', attrs={'class':'object_descr_price_box'})
            price = re.split('<div>|за м<sup>2</sup>|\n|руб|\W', str(price))
            price_fin = []
            for i in price:
                if i.isnumeric():
                    price_fin.append(i)
            allflats_stat[flat_id]['Price'] = int(str(price_fin[-2])+str(price_fin[-1]))
            
            # Число комнат Rooms
            rooms = flat_page.find('div', attrs={'class':'object_descr_title'})
            for j in str(rooms):
                if j.isnumeric():
                    allflats_stat[flat_id]['Rooms'] = int(j)
                    
            # Много всякого
            table = flat_page.find('table', attrs = {'class':'object_descr_props'})
            table = re.split(':|\xa0/\xa0|<i class="object_descr_details_color" style="background-color:#90C0C0"></i>|<i class="object_descr_details_color" style="background-color:#C0C0C0"></i>|<table>|</table>|<i class="object_descr_details_color" style="background-color:#C09090"></i>|<i class="object_descr_details_color" style="background-color:#90C090"></i>|\xa0м<sup>2</sup>|<i class="object_descr_details_color"></i>|\n|<i class="object_descr_details_color"></i>33\xa0м<sup>2</sup>|<td>|</td>|<th>|</th>|<tr>|</tr>', str(table))
            
            table = re.split('\xa0/|\xa0м|</sup>|<sup>|</i>|Общая информация:|style="background-color:|<th style="padding-top:5px;">|<th>|</th>|<td>|</td>|\n|<tr>|</tr>|<i class="object_descr_details_color"', str(table))
            table = re.split('\W', str(table))
            table_clean = []
            for item in range(1, len(table)):
                if len(table[item])!=0:
                    table_clean.append(table[item])
            
            for item in range(0, len(table_clean)):
                if table_clean[item] == 'Этаж':
                    allflats_stat[flat_id]['NFloor'] = int(table_clean[item+1])
                    allflats_stat[flat_id]['Floors'] = int(table_clean[item+2])
                    if int(table_clean[item+1]) == 1:
                        allflats_stat[flat_id]['floor1'] = 1
                    elif int(table_clean[item+1]) == int(table_clean[item+2]):
                        allflats_stat[flat_id]['floor2'] = 1
                        
                    if int(table_clean[item+1]) > 1 and int(table_clean[item+1]) < int(table_clean[item+2]):
                        allflats_stat[flat_id]['Floor'] = 1
                    else:
                        allflats_stat[flat_id]['Floor'] = 0
                        
                elif table_clean[item] == 'Тип' and table_clean[item+1] == 'дома':
                    if 'вторич' in table_clean[item+2]:
                        allflats_stat[flat_id]['New'] = 0
                    else:
                        allflats_stat[flat_id]['New'] = 1
                        
                    if 'кирпич' in table_clean[item+3] or 'монол' in table_clean[item+3] or 'желез' in table_clean[item+3] or 'ж/б' in table_clean[item+3]:
                        allflats_stat[flat_id]['Brick'] = 1
                    else:
                        allflats_stat[flat_id]['Brick'] = 0
                        
                elif table_clean[item] == 'Общая' and table_clean[item+1] == 'площадь':
                    allflats_stat[flat_id]['Totsp'] = int(table_clean[item+2])
                    
                elif table_clean[item] == 'Жилая' and table_clean[item+1] == 'площадь':
                    allflats_stat[flat_id]['Livesp'] = int(table_clean[item+2])
                    
                elif table_clean[item] == 'Площадь' and table_clean[item+1] == 'кухни':
                    allflats_stat[flat_id]['Kitsp'] = int(table_clean[item+2])
                    
                elif table_clean[item] == 'Телефон':
                    if table_clean[item+1].lower() == 'нет':
                        allflats_stat[flat_id]['Tel'] = 0
                    else:
                        allflats_stat[flat_id]['Tel'] = 1
                
                elif table_clean[item] == 'Балкон':
                    if table_clean[item+1].lower() == 'нет':
                        allflats_stat[flat_id]['Bal'] = 0
                    else:
                        allflats_stat[flat_id]['Bal'] = 1
                        
                elif table_clean[item] == 'Лифт':
                    if table_clean[item+1].lower() == 'нет':
                        allflats_stat[flat_id]['Elevat'] = 0
                    else:
                        allflats_stat[flat_id]['Elevat'] = 1
                        
        except:
            continue            

end = time.time()  
time_elapsed = end - start

for key in allflats_stat:
    if allflats_stat[key] != {}:
        allflats[key] = allflats_stat[key]

flats_frame = pd.DataFrame()
for key in allflats:
    flats_frame = flats_frame.append(allflats[key], ignore_index=True)
    
flats_frame.to_csv('C:\\Users\\Auditore\\Desktop\\flats.csv', sep=',', header=True)

from pylab import *
pylab.plot(flats_frame.Price)