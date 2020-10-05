import json

TOP = -17.526380
BOT = -24.075901
RIGHT = -50.917960
LEFT = -58.245706
CONFIDENCE = 80

filtered = []
with open('/home/pedro/Downloads/Nasa data/DL_FIRE_M6_157626/fire_archive_M6_157626.json', 'r') as handle:
    parsed = json.load(handle)
    for p in parsed:
        lat = float(p['latitude'])
        lon = float(p['longitude'])
        conf = int(p['confidence'])

        if (lat > BOT and lat < TOP and
            lon > LEFT and lon < RIGHT and
            conf >= CONFIDENCE):
            print(str(lat) + ", " + str(lon) + "   " + str(conf))
            print(type(conf))


print("SIZE: ", len(filtered))

with open('/home/pedro/Downloads/Nasa data/high_confidence_wildfire_filtered_large_dataset.json', 'w') as outfile:
    # json.dump(filtered, outfile)
    json.dump(filtered, outfile, indent=4)