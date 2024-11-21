import csv
import sys
import json
# open the file in read mode
sys.stdout = open('./output_data.txt', 'w')
filename = open('./YelpScraping/data.csv', 'r')
# creating dictreader object
file = csv.DictReader(filename)
for row in file:
    print('{ "index": {} }')
    d = {"RestaurantID": str(row['id']), "Cuisine": str(row['cuisine'])}
    print(json.dumps(d))
    