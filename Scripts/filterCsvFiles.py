import csv
from os import walk

INPUT_FOLDER_PATH = "./weather/2020/"

PRECIPITACAO_INDEX = 2
TEMPERATURA_INDEX = 7
UMIDADE_INDEX = 15
VENTO_INDEX = 18


files = []
for (dirpath, dirnames, filenames) in walk(INPUT_FOLDER_PATH):
    files = filenames
    # break

print("FILES:", files)

for file in files:

    INPUT_FILE = INPUT_FOLDER_PATH+"/"+str(file)
    OUTPUT_FILE_PATH = INPUT_FOLDER_PATH+"/filtered_"+str(file)

    with open(OUTPUT_FILE_PATH, "w") as csv_out_file:
        csv_out = csv.writer(csv_out_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

        with open(INPUT_FILE) as csv_in_file:

            print("\nReading file", file)

            csv_reader = csv.reader(csv_in_file, delimiter=',')
            line_count = 0
            day_line_count = 0.0
            last_day = 0
            last_day_aux = "0"
            mean_precipitacao = 0
            mean_temp = 0
            mean_umidade = 0
            mean_vento = 0


            for row in csv_reader:
                row_string = ""
                for s in row:
                    row_string += "."+ s
                splited_row = row_string.split(";")
                day = splited_row[0][1:]

                print()
                print(row)
                print(row_string)
                if line_count >= 9:
                    print(str(splited_row[PRECIPITACAO_INDEX]) + ", " + str(splited_row[TEMPERATURA_INDEX])+ ", " + str(splited_row[UMIDADE_INDEX]))

                    if (day > last_day and line_count != 9):
                        print("CONT,", day_line_count)
                        mean_precipitacao /= day_line_count
                        mean_temp /= day_line_count
                        mean_umidade /= day_line_count
                        mean_vento /= day_line_count

                        mean_precipitacao = round(mean_precipitacao, 2)
                        mean_temp = round(mean_temp, 2)
                        mean_umidade = round(mean_umidade, 2)
                        mean_vento = round(mean_vento, 2)

                        csv_out.writerow([last_day_aux, mean_precipitacao, mean_temp, mean_umidade, mean_vento])

                        mean_precipitacao = 0
                        mean_temp = 0
                        mean_umidade = 0
                        mean_vento = 0
                        day_line_count = 0


                    if (day == last_day):
                        try:
                            last_day_aux = day
                            prec = float(splited_row[PRECIPITACAO_INDEX])
                            temp =  float(splited_row[TEMPERATURA_INDEX])
                            umid = float(splited_row[UMIDADE_INDEX])
                            vent = float(splited_row[VENTO_INDEX])
                        except:
                            continue                        

                        if (prec < 0 or temp < 0 or umid < 0 or vent < 0):
                            continue

                        mean_precipitacao += prec
                        mean_temp += temp
                        mean_umidade += umid
                        mean_vento += vent

                    day_line_count += 1
                    last_day = day
                    

                elif line_count == 8:
                    csv_out.writerow(["Data", "Precipitacao", "Temperatura", "Umidade", "Vento"])
                else:
                    csv_out.writerow(row)

                # if (line_count == 40):
                #     break
                line_count += 1

            print('Processed '+ str(line_count) +' lines.')