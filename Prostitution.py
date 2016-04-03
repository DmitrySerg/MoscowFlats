# -*- coding: utf-8 -*-
"""
Created on Wed Jan 27 13:09:39 2016

@author: Dmitry Sergeyev
"""

import requests
import re
from bs4 import BeautifulSoup
import pandas as pd

prostitutes = {a: {} for a in range(1800)}

for page in range(1, 59):
    
    url = 'http://www.intimgarem.net/prostitutki/'+str(page)
    response = requests.get(url)
    html = response.content
    soup = BeautifulSoup(html)
    
    # Для скачивания станции метро и имени
    prostitute_id = (page - 1) * 30 # для каждой страницы обновляем начальный id
    station = soup.findAll('a', attrs={'class':'post_thumb'})
    for j in station:
        j = re.split(" ", str(j.contents[1]))
        for item in j:
            prostitutes[prostitute_id]["metro"] = item  
        prostitutes[prostitute_id]["name"] = re.split('\W', j[1])[2]
        prostitute_id += 1
        
    # Параметры    
    prostitute_id = (page - 1) * 30 
    parameters = soup.findAll('div', attrs={'class':'har_gar'})
    for param in parameters:
        param = re.split("<li>|</li>|<ul>|</ul>|\n|<span>|</span>", str(param.contents[1]))
        for i in range(1,len(param)):
            if param[i] == "Возраст:":
                prostitutes[prostitute_id]["age"] = int(param[i+1])
            elif param[i] =="Рост:":
                prostitutes[prostitute_id]["height"] = int(param[i+1])
            elif param[i] =="Вес:":
                prostitutes[prostitute_id]["weight"] = int(param[i+1])
            elif param[i] =="Грудь:":
                prostitutes[prostitute_id]["breast"] = int(param[i+1])
            else:
                continue
        prostitute_id += 1
        
    # Цена
    prostitute_id = (page - 1) * 30   
    priceAll = soup.findAll('span', attrs={'class':'cena'})
    for price in priceAll:
        price = re.split(">|<", str(price))
        for i in price:
            if i.isnumeric():
                prostitutes[prostitute_id]["price"] = int(i)
        prostitute_id += 1

prostitutes_frame = pd.DataFrame()
for key in prostitutes:
    prostitutes_frame = prostitutes_frame.append(prostitutes[key], ignore_index=True)

prostitutes_frame.to_csv('C:\\Users\\Auditore\\Desktop\\whores.csv', sep=',', header=True)
