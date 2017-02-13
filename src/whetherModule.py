# -*- coding: utf-8 -*-
# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.
import requests
from datetime import datetime, timedelta

class Whether:
    
    
    def __init__(self):
        self.city_id = 1486209
        self.appid = "1f064fd0ea3e01b8af5b756becae4005"
        self.lastUpdateTime = datetime(2010, 12, 12)
        self.lastWhetherData = None
    
    def GetCities(self, s_city="Yekaterinburg,RU"):
        try:
            res = requests.get("http://api.openweathermap.org/data/2.5/find",
                         params={'q': s_city, 'type': 'like', 'units': 'metric', 'APPID': self.appid})
            data = res.json()
            cities = ["{} ({})".format(d['name'], d['sys']['country'])
                      for d in data['list']]
            #print("city:", cities)
            self.city_id = data['list'][0]['id']
            return data['list']
            #print('city_id=', self.city_id)
        except Exception as e:
            print("Exception (find):", e)
            pass
    
    def GetNowWheather(self):
        try:
            res = requests.get("http://api.openweathermap.org/data/2.5/weather",
                         params={'id': self.city_id, 'units': 'metric', 'lang': 'ru', 'APPID': self.appid})
            data = res.json()
            #print("conditions:", data['weather'][0]['description'])
            #print("temp:", data['main']['temp'])
            #print("temp_min:", data['main']['temp_min'])
            #print("temp_max:", data['main']['temp_max'])
            self.lastUpdateTime = datetime.now()
            self.lastWhetherData = data
            return data
        except Exception as e:
            print("Exception (weather):", e)
            pass  
    
    def PrepareValueToSpeach(self, value):
        if (value < 0):
            value = 'minus ' + str(abs(value))
        return value
    
    def GetStringForSpeach(self):
        delta = timedelta(hours=1)
        if (self.lastUpdateTime+delta < datetime.now()):
            self.GetNowWheather()
        minTemperature = self.PrepareValueToSpeach(self.lastWhetherData['main']['temp_min'])
        
        maxTemperature = self.PrepareValueToSpeach(self.lastWhetherData['main']['temp_max'])
        
        nowTemp = self.PrepareValueToSpeach(self.lastWhetherData['main']['temp'])
        
        conditions = self.lastWhetherData['weather'][0]['description'].encode('utf8')
        return "Сейчас на улице {now} градусов, {conditions}. Минимальная {minimum}. Максимальная {maximum}".format(now=nowTemp,
            conditions = conditions, minimum = minTemperature, maximum =  maxTemperature)
        



w = Whether()
a = w.GetNowWheather()
#data = a['weather'][0]['description']
#print data.encode('utf8')
print w.GetStringForSpeach()