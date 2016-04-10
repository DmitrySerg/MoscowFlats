# -*- coding: utf-8 -*-
"""
Created on Thu Jan 28 22:59:52 2016

@author: Dmitry Sergeyev
"""

import requests
import re
from bs4 import BeautifulSoup

allflats = {a: {} for a in range(500)}
allflats_stat = {a: {} for a in range(500)}
url = 'https://realty.yandex.ru/search?type=SELL&category=APARTMENT&rgid=587795&page=0'

link_beg = 'https://realty.yandex.ru'
response = requests.get(url)
html = response.content
soup = BeautifulSoup(html)

#flat_id = (page - 1) * 25

flats_links = soup.findAll('a', attrs = {'class':'link stat__click space-offer-opener i-bem'})
for flat_link_number in range(0, 2):
    flat = flats_links[flat_link_number]
    

    for i in re.split(" ", str(flat)):
        if "href" in i:
            link_end = re.split('"', str(i))[1]
            
    link = link_beg+link_end
    flat_page = requests.get(link)
    flat_page = flat_page.content
    flat_page = BeautifulSoup(flat_page)
    
    # Выкачиваем данные из table
    item = flat_page.findAll('span', attrs = {'class':'offer-data__item-left-span'})   
    value = flat_page.findAll('td', attrs = {'class':'offer-data__item-right offer-data__item-td'})
    
    for i in range(0, len(item)):
        key = re.split('<span class="offer-data__item-left-span">|</span>', str(item[i]))[1]
        allflats[flat_link_number][key] = re.split('<td class="offer-data__item-right offer-data__item-td">|</td>', str(value[i]))[1]
         
    # Цена
    
    price = flat_page.find('div', attrs = {'class':'seller__price-note'})
    price = re.split('<div class="seller__price-note">| <span class="i-font_face_rub-arial-regular">Р</span> за м²</div>', str(price))[1]
    Price = ''
    for p in price:
        if p.isdigit():
            Price+=p
    allflats_stat[flat_link_number]['Price'] = int(Price)

    
    # Адрес
    address = flat_page.find('div', attrs = {'class':'offer-map__street'})
    address = re.split('<div class="offer-map__street">|</div>', str(address))[1]
    allflats_stat[flat_link_number]['Адрес'] = address
    
    # Метро
    metro = flat_page.find('div', attrs = {'class':'offer-map__metro'})
    metro = re.split('<div class="offer-map__metro">м. |, <span class="link link_pseudo_yes offer-map__metro-time binder i-bem"', str(metro))[1]
    allflats_stat[flat_link_number]['metro'] = metro
    
    # Расстрояние до метро в метрах
    metro_dist = flat_page.find('div', attrs = {'class':'offer-map__metro'})
    metro_dist = re.split('<span class="link__inner">|</span>', str(metro_dist))[1]
    Metrdist = re.split(' ', metro_dist)[0]
    allflats_stat[flat_link_number]['Metrdist'] = int(Metrdist)
    
    # Идём или едем до метро
    if re.split(' ', metro_dist)[-1] == "пешком":
        Walk = 1
    elif re.split(' ', metro_dist) == "транспорте":
        Walk = 0
    else:
        Walk = "NA"
    allflats_stat[flat_link_number]['Walk'] = Walk
    
    # Координаты МЭЙСОН ЧИСЛА ЧТО ОЗНАЧАЮТ ЭТИ ЧИСЛА
    coords = re.split('"lat"|"lon"|"disabled"', str(flat_page))
    latitude = coords[1][1:-1]
    longtitude = coords[2][1:-1]
    allflats_stat[flat_link_number]['coords_lat_long'] = [float(latitude), float(longtitude)]
    
    # Первичка или вторичка
    first_second = flat_page.find('a', attrs = {'class':'link link_nav_yes type-switcher__link type-switcher__link_type_resale type-switcher__link_active_yes i-bem'})
    if 'Первичка' in  re.split('\W', str(first_second)):
        allflats_stat[flat_link_number]['New'] = 1
    elif 'Вторичка' in  re.split('\W', str(first_second)):
        allflats_stat[flat_link_number]['New'] = 0
        
   
    # Заполняем необходимые поля 
    for key in allflats[flat_link_number].keys():
        # Если это этаж, то создаем внутри словарь, содержащий ключи Floor, Floorsи т.д.
        if key.lower() =='этаж':
            allflats[flat_link_number][key] = {'NFloor':int(re.split(' ', allflats[flat_link_number][key])[0]), 'Floors':int(re.split(' ', allflats[flat_link_number][key])[2])}  
            allflats_stat[flat_link_number][key] = {'NFloor':int(re.split(' ', allflats[flat_link_number][key])[0]), 'Floors':int(re.split(' ', allflats[flat_link_number][key])[2])}
            if allflats[flat_link_number][key]['NFloor'] == 1:
                allflats_stat[flat_link_number][key]['floor1'] = 1
                allflats_stat[flat_link_number][key]['Floor'] = 0
            elif allflats[flat_link_number][key]['NFloor'] == allflats[flat_link_number][key]['Floors']:
                allflats_stat[flat_link_number][key]['floor2'] = 1            
                allflats_stat[flat_link_number][key]['Floor'] = 0
            else:
                allflats_stat[flat_link_number][key]['Floor'] = 1
            
        # Заполняем переменную Rooms и удаляем имевшийся ключ "Количество комнат"
        if key.lower() == 'количество комнат':
            allflats_stat[flat_link_number]['Rooms'] = int(allflats[flat_link_number][key])
        # Переменная Bal + удаляем Балкон
        if key.lower() == 'балкон' or key.lower() == 'лоджия':
            allflats_stat[flat_link_number]['Bal'] = 1

        
        # Переменная Totsp, Livesp, Kitsp
        if key.lower() == 'общая площадь':
            allflats_stat[flat_link_number]['Totsp'] = re.split(' ', allflats[flat_link_number][key])[0]
        if key.lower() == 'жилая':
            allflats_stat[flat_link_number]['Livesq'] = re.split(' ', allflats[flat_link_number][key])[0]
        if key.lower() == 'кухня':
            allflats_stat[flat_link_number]['Kitsp'] = re.split(' ', allflats[flat_link_number][key])[0]

        
        # Телефон
        if key.lower() == 'телефон':
            if allflats[flat_link_number][key] == 'да' or allflats[flat_link_number][key] == 'есть':
                allflats_stat[flat_link_number]['Tel'] = 1
            else:
                allflats_stat[flat_link_number]['Tel'] = 0
            
        # Переменная Brick
        if key.lower() == 'тип стен':
            if allflats[flat_link_number][key] in ['кирпич', 'монолит', 'ж/б', 'железобетон']:
                allflats_stat[flat_link_number]['Brick'] = 1
            else:
                allflats_stat[flat_link_number]['Brick'] = 0