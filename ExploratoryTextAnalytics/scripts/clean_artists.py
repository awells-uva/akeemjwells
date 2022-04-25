##### Akeem Wells ( ajw3rg@virginia.edu )
##### DS 5001
##### 10 May 2021
# Script to view artistgenre.csv for duplicates in names and genres

import os
import csv
indir = "/Users/awells/UVA/DS5001/final/"
ref_data = {}
mylist = []
pc = 0
cc = 0
hc = 0
rc = 0

with open(indir + 'data/artists_genre_data/artistgenre.csv', mode='r') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    line_count = 0
    for row in csv_reader:
        if line_count == 0:
            print(f'Column names are {", ".join(row)}')
            line_count += 1
            continue
        #print(f'\t{row["name"]} {row["genre"]}.')
        
        if row["genre"] == 'pop' : pc += 1
        if row["genre"] == 'country' : cc += 1
        if row["genre"] == 'rnbhiphop' :  hc += 1
        if row["genre"] == 'rap' :  rc += 1
        
        if row["name"].lower() not in ref_data:
            ref_data[row["name"].lower()] = []
        
        if row["genre"] not in ref_data[row["name"].lower()]:
            ref_data[row["name"].lower()].append(row["genre"])
        line_count += 1
    print(f'Processed {line_count} lines.')



for key in ref_data.keys():
    if len(ref_data[key]) > 1:
        print(key, ref_data[key])
    
#print(pc,cc,hc,rc)
#print(mylist)
#import collections
#print([item for item, count in collections.Counter(mylist).items() if count > 1])
print(len(ref_data.keys()))
