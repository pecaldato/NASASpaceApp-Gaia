import csv
from os import walk
import json

WILD_FIRE_SPOT_PRECISION = 0.15 # the max threashold for the fire spot using the latitude and longitude values
class FileHandler(object):


    def __init__(self, folder_path, citie_index_file, wildFire_json):
        
        self.folder_path = folder_path
        self.index = citie_index_file
        self.wildFireJson = wildFire_json

    def _get_files_and_folders(self):
        folders = []
        files = []
        for (dirpath, dirnames, filenames) in walk(self.folder_path):
            folders.append(dirnames)
            files.append(filenames)
        
        return folders, files

    def _get_closer_city_info(self, latitude, longitude):
        with open(self.index) as csv_in_file:
            csv_reader = csv.reader(csv_in_file, delimiter=',')

            small_distance = float("inf")
            small_lat = 0
            small_lon = 0
            city_region = ""
            city_uf = ""
            city_name = ""

            for row in csv_reader:
                if (row[0] == "REGIAO"):
                    continue
                lat = float(row[3])
                lon = float(row[4])

                dist = pow((pow((latitude-lat), 2) + pow((longitude-lon), 2)), 0.5)
                if (dist < small_distance):
                    small_lat = lat
                    small_lon = lon
                    city_region = row[0]
                    city_uf = row[1]
                    city_name = row[2]
                    small_distance = dist

        return {"lat":small_lat, "lon":small_lon, "region":city_region, "uf":city_uf, "name": city_name}

    
    
    def _get_closer_fire_info(self, latitude, longitude):
        global WILD_FIRE_SPOT_PRECISION
        with open(self.wildFireJson, 'r') as handle:
            parsed = json.load(handle)

            fires_spot = []
            for p in parsed:
                lat = float(p['latitude'])
                lon = float(p['longitude'])

                # dist = pow((pow((latitude-lat), 2) + pow((lon-lon), 2)), 0.5)
                dist = abs(latitude-lat) + abs(longitude-lon)
                if (dist < WILD_FIRE_SPOT_PRECISION):

                    fires_spot.append(p)

            return fires_spot
    
    
    def _get_city_weater_from_date(self, date, file_pat):
        with open(file_pat) as csv_in_file:
            csv_reader = csv.reader(csv_in_file, delimiter=',')
            
            count = -1
            for row in csv_reader:
                count += 1
                if count < 9:
                    continue

                if row[0].replace('/', '-') == date:
                    row[0] = row[0].replace('/', '-')
                    return row




    def get_firespots_and_weather_history(self, latitude, longitude):

        folders, files = self._get_files_and_folders()
        city_infos = self._get_closer_city_info(latitude, longitude)

        fires_spot = self._get_closer_fire_info(latitude, longitude)

        # for f in fires_spot:
            # print(json.dumps(f, indent=4, sort_keys=True))

        fires_and_weather = []
        for fire in fires_spot:
            # print(json.dumps(fire, indent=4, sort_keys=True))

            fire_date = fire['acq_date']
            year, month, day = fire_date.split('-')
            for files_folders in files[1:]:
                if year in files_folders[0]:
                    
                    for file in files_folders:
                        if city_infos["name"] in file:
                            
                            file_path = self.folder_path+"/"+year+"/"+file
                            row = self._get_city_weater_from_date(fire_date, file_path)                            
                            
                            if not row == None:
                                f_and_we = {"fireSpot": fire, "weather": row, "cityInfo": city_infos}
                                fires_and_weather.append(f_and_we)

        return fires_and_weather




