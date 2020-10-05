from FileHandler import FileHandler
import requests
import json

import matplotlib.pyplot as plt
from matplotlib.dates import (YEARLY, DateFormatter,
                              rrulewrapper, RRuleLocator, drange)
import matplotlib.dates as mdates
import numpy as np
import datetime

class FireSpotDigger(object):

    def __init__(self, fireSpot_api_link):
        self.fire_api = fireSpot_api_link
        self.lastFireDate = ""
        self.get_newst_fire_info()
        self.API_KEY = "57610b7195f94882bbc174f9222dde7e"


    def _filter_info(self):

        new_json = []
        count = 0
        for i in self.lastJsonFireSpot:
            if i["properties"]["risco_fogo"] != None:
                if float(i["properties"]["risco_fogo"]) >= 0.8:
                    count += 1
                    new_json.append(i)

            if (str(i["properties"]["data_hora_gmt"]) <= self.lastFireDate):
                # print("ENTROU")
                break


        self.lastFireDate = str(self.lastJsonFireSpot[0]["properties"]["data_hora_gmt"])
        self.lastJsonFireSpot = new_json
        print(str(count) + " NEW DATA HAS BEEN RECEIVED\n\n")
        
    def get_newst_fire_info(self):

        print("\n\nSENDING REQUEST...")
        print("Downloading new data")
        print("Filtering new data")
        print(self.fire_api)
        self.lastJsonFireSpot = requests.get(self.fire_api).json()
        self._filter_info()

    def get_last_fires_spot(self):
        return self.lastJsonFireSpot

    def get_curr_weather(self, latitude, longitude):
        url = "http://api.openweathermap.org/data/2.5/weather?lat="+str(latitude)+"&lon="+str(longitude)+"&appid="+self.API_KEY
        curr_weather = requests.get(url).json()
        return curr_weather




# ============================================================================

# def plotMat(dates, heat, umit):
    
#     print(heat)
#     rule = rrulewrapper(YEARLY, byeaster=1, interval=5)
#     loc = RRuleLocator(rule)
#     formatter = DateFormatter('%m/%d/%y')
#     new = []
#     for d in dates:
#         splited = d.split('-')
#         splited = splited[1]+"/"+splited[2]+"/"+splited[0]
#         new.append(splited)
#         print(splited)

#     dates = new

#     dates = [datetime.datetime.strptime(d,"%m/%d/%Y").date() for d in dates]

#     fig, ax = plt.subplots(2, sharex=True)
#     ax[0].plot_date(dates, heat)
#     ax[0].xaxis.set_major_locator(loc)
#     ax[0].xaxis.set_major_formatter(formatter)
#     ax[0].set(xlabel="Date",
#        ylabel="Heat (C)",
#        title="Local heat when fires were spotted")
    
    
#     ax[1].plot_date(dates, umit)
#     ax[1].xaxis.set_major_locator(loc)
#     ax[1].xaxis.set_major_formatter(formatter)
#     ax[1].set(xlabel="Date",
#        ylabel="Umidity",
#        title="Local humidity when fires were spotted")    

#     plt.show()

# def printJson(jsoon):
#     return json.dumps(jsoon, indent=4, sort_keys=True)

# ============================================================================



handler = FileHandler("./datasets/filtered_weather/", "./datasets/cityindex.csv", "./datasets/high_confidence_wildfire_filtered_large_dataset.json")

fire_digger = FireSpotDigger("http://queimadas.dgi.inpe.br/queimadas/dados-abertos/api/focos/?pais_id=33&estado_id=50")
fire_spots = fire_digger.get_last_fires_spot()


all_fires = []

print("\nSEARCHING FOR FIRE SPOTTS HISTORY...")
x = 0
for spots in fire_spots:
    
    data_fires = {}
    data_fires['current_fire'] = []
    data_fires["current_fire"].append(spots)

    lat = float(spots["properties"]["latitude"])
    lon = float(spots["properties"]["longitude"])

    data_fires["current_weather"] = []
    data_fires["current_weather"].append(fire_digger.get_curr_weather(lat, lon))

    data_fires["history"] = []

    fires = handler.get_firespots_and_weather_history(lat, lon)
    # print(fires)

    for f in fires:
        data_history = {}
        data_history["weather"] = []
        data_history["weather"].append(f['weather'])
        data_history["fireSpot"] = []
        data_history["fireSpot"].append(f['fireSpot'])
        data_history["cityInfo"] = []
        data_history["cityInfo"].append(f['cityInfo'])
        data_fires["history"].append(data_history)
    
    print(str(len(fires))+" fires were founded for the local ("+str(lat)+", "+str(lon)+")")

    # printJson(data_fires)
    all_fires.append(data_fires)

    # x += 1
    # if x == 5:
    #     break

print("\n\nSAVIND DATA...")
with open('FIRE_SPOTT_HISTORY.json', 'w') as outfile:
    json.dump(all_fires, outfile, indent=4)
print("DATA SAVED AT FIRE_SPOTT_HISTORY.json")



