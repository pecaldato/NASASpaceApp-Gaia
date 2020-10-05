import csv
from os import walk

INPUT_FOLDER_PATH = "./filtered_weather/"

folders = []
files = []
for (dirpath, dirnames, filenames) in walk(INPUT_FOLDER_PATH):
    folders.append(dirnames)
    files.append(filenames)


OUTPUT_FILE_PATH = "./cityindex.csv"
cities_list = []
with open(OUTPUT_FILE_PATH, "w") as csv_out_file:
    csv_out = csv.writer(csv_out_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    csv_out.writerow(["REGIAO", "UF", "CIDADE", "LATITUDE", "LONGITUDE"])

    count = 0
    for folder in folders[0]:
        count += 1

        for file in files[count]:
            INPUT_FILE = INPUT_FOLDER_PATH + "/" + folder + "/" + file

            info = []
            with open(INPUT_FILE) as csv_in_file:

                print()
                print("Reading file", INPUT_FILE)

                csv_reader = csv.reader(csv_in_file, delimiter=';')

                i = -1
                controler = True
                for row in csv_reader:
                    i += 1
                    print(row)
                    if i == 2:
                        if row[1] in cities_list:
                            controler = False
                            break
                        cities_list.append(row[1])
                    elif (i == 3):
                        continue
                    elif i == 6:
                        break
                    cities_list.pop
                    info.append(row[1].replace(',', '.'))

                if controler:
                    csv_out.writerow(info)
