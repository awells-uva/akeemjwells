##### Akeem Wells ( ajw3rg@virginia.edu )
##### DS 5001
##### 10 May 2021
# Script to read artistgenre.csv, matches artist to bilboard song, downloads lyrics, saves to .txt
# Download may not always be correct due to the Api, each file needs to be visually confirmed.

import lyricsgenius as lg
import os
import sys
import requests
from bs4 import BeautifulSoup

indir = '/Users/awells/UVA/DS5001/final/'


import csv
ref_data = {}
with open(indir + 'data/artists_genre_data/artistgenre.csv', mode='r') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    line_count = 0
    for row in csv_reader:
        if line_count == 0:
            print(f'Column names are {", ".join(row)}')
            line_count += 1
            continue
        #print(f'\t{row["name"]} {row["genre"]}.')
        if row["name"].lower().strip() not in ref_data:
            ref_data[row["name"].lower().strip()] = row["genre"]
        line_count += 1
    print(f'Processed {line_count} lines.')

#print(ref_data)
#sys.exit()
#for year in range(2015,2021):
for year in range(2020,2021):

    year = str(year)
    print(">>>>>>>>>>>> {} <<<<<<<<<<<<<<<<<<".format(year))
    if not os.path.exists('{}/data/{}'.format(indir,year)):
        os.makedirs('{}/data/{}'.format(indir,year))

    url = "https://www.billboard.com/charts/year-end/{}/hot-100-songs".format(year)
    page =requests.get(url)
    soup = BeautifulSoup(requests.get(url).content, 'html.parser')
    songs = soup.find_all("div", {"class": "ye-chart-item__title"})
    artists = soup.find_all("div", {"class": "ye-chart-item__artist"})

    song_titles = []
    artist_names = []
    for song in songs:
        song_titles.append(song.text.replace("\n",""))
        #print(song.text)
        
    for artist in artists:
        artist_names.append(artist.text.replace("\n",""))

    #print("Zipping")
    zipped = zip(song_titles, artist_names)

    zipped = list(zipped)

    mapped = []
    unknown = []
    #print(mapped)
    for item in zipped:
        if item[1].lower().strip() in ref_data.keys():
            #print(item,ref_data[item[1].lower()] )
            mapped.append([item[0],item[1],ref_data[item[1].lower().strip()]] )
            pass
        else:
            if "Featuring" in item[1]:
                name = item[1].split("Featuring")[0].rstrip().lower().strip()
                if name in ref_data.keys():
                    mapped.append([item[0],item[1],ref_data[name]])
                    pass
            elif "With" in item[1]:
                name = item[1].split("With")[0].rstrip().lower().strip()
                if name in ref_data.keys():
                    mapped.append([item[0],item[1],ref_data[name]] )
                    pass
            elif "&" in item[1]:
                name = item[1].split("&")[0].rstrip().lower().strip()
                if name in ref_data.keys():
                    mapped.append([item[0],item[1],ref_data[name]] )
                    pass
            elif "X" in item[1]:
                name = item[1].split("X")[0].rstrip().lower().strip()
                if name in ref_data.keys():
                    mapped.append([item[0],item[1],ref_data[name]] )
                    pass
            elif "x" in item[1]:
                name = item[1].split("x")[0].rstrip().lower().strip()
                if name in ref_data.keys():
                    mapped.append([item[0],item[1],ref_data[name]] )
            else:
                print("Unknown: {}".format(item))
                #unknown.append(item[1].strip() +',')
                #unknown.append([item[0],item[1],'unknown'])
    #print(mapped)
    #print()
    #for item in list(set(unknown)):
    #    print(item)
    #continue
    for i in range(len(mapped)):
        artist_data = mapped[i]
        genre = artist_data[2]
        print()
        print(artist_data)

        artist_save_name =artist_data[1].replace(" ","_")
        if "Featuring" in artist_save_name:
            artist_save_name = artist_save_name.split("Featuring")[0].rstrip().lower()

        elif "With" in artist_save_name:
            artist_save_name = artist_save_name.split("With")[0].rstrip().lower()

        elif "&" in artist_save_name:
            artist_save_name = artist_save_name.split("&")[0].rstrip().lower()

        elif "X" in artist_save_name:
            artist_save_name = artist_save_name.split("X")[0].rstrip().lower()

        elif "x" in artist_save_name:
            artist_save_name = artist_save_name.split("x")[0].rstrip().lower()

        #print("Save File: {}".format("{}/data/{}/{}/{}---{}.txt".format(indir,year,genre,
        #                        artist_data[0].replace(" ","_").replace("'",""),artist_save_name.lower()
        #                                                                      )))
        if not os.path.exists('{}/data/{}/{}'.format(indir,year, genre)):
            os.makedirs('{}/data/{}/{}'.format(indir,year,genre))

        genius = lg.Genius('3uJm4IxVnXyyxxOdalox_SvIkIgtaY45cjL-yNOtvgadeWPOvEKd6kNE46Pw-yUG',  # Client access token from Genius Client API page
                                     skip_non_songs=True, excluded_terms=["(Remix)", "(Live)"],
                                     remove_section_headers=True)
        try:
            song = genius.search_song(title=artist_data[0], artist = artist_data[1])
            file = open("{}/data/{}/{}/{}---{}.txt".format(indir,year,genre,
                artist_data[0].replace(" ","_").replace("'",""),artist_save_name.lower()),"w")  # File to write lyrics to
            #s = [song.lyrics for song in songs]
            file.write(song.lyrics)  # Deliminator
            file.close()
        except:
            print("Cannot Write Song: {} by {}".format(artist_data[0],artist_data[1]))

    pass
