##### Akeem Wells ( ajw3rg@virginia.edu )
##### DS 5001
##### 10 May 2021
# Script to parse billboard information, to generate artistgenre.csv ( a file that contains Artist - Genre metadata
import requests
from bs4 import BeautifulSoup
import os
import sys

def get_artist_genre(url,genre):

    page =requests.get(url)
    soup = BeautifulSoup(requests.get(url).content, 'html.parser')
    artists_genre = []
    artists = soup.find_all("div", {"class": "ye-chart-item__title"})
    for artist in artists:
        #print(artist)
        artists_genre.append((artist.find('a').contents[0].replace("\n",""),genre))
    return artists_genre

def write_to_csv(array):
    for line in list(array):
        file.write("{},{}\n".format(line[0].replace(",",""),line[1]))
        
artists_genre_rnb = []
artists_genre_country = []
artists_genre_pop = []
artists_genre_rap = []

for year in range(2009,2021):
    print("Gathering: RnB / HipHop, {}".format(year))
    artists_genre_rnb += get_artist_genre("https://www.billboard.com/charts/year-end/{}/top-r-and-b-hip-hop-artists".format(year),"rnbhiphop")

for year in range(2009,2021):
    print("Gathering: RnB / HipHop, {}".format(year))
    artists_genre_rnb += get_artist_genre("https://www.billboard.com/charts/year-end/{}/hot-r-and-b-hip-hop-songs-artists".format(year),"rnbhiphop")


for year in range(2009,2021):
    print("Gathering: Country, {}".format(year))
    artists_genre_country += get_artist_genre("https://www.billboard.com/charts/year-end/{}/top-country-artists".format(year),"country")

for year in range(2009,2021):
    print("Gathering: Country, {}".format(year))
    artists_genre_country += get_artist_genre("https://www.billboard.com/charts/year-end/{}/top-country-albums-artists".format(year),"country")
    
for year in range(2009,2021):
    print("Gathering: Pop, {}".format(year))
    artists_genre_pop += get_artist_genre("https://www.billboard.com/charts/year-end/{}/pop-songs-artists".format(year),"pop")

for year in range(2009,2021):

    print("Gathering: Rap, {}".format(year))
    artists_genre_rap += get_artist_genre("https://www.billboard.com/charts/year-end/{}/rap-albums-artists".format(year),"rap")

for year in range(2009,2021):
    print("Gathering: Rap, {}".format(year))
    artists_genre_rap += get_artist_genre("https://www.billboard.com/charts/year-end/{}/hot-rap-songs-artists".format(year),"rap")

    #print(artists_genre_rnb)
    #sys.exit()
#print(artists_genre_rnb)
#print(artists_genre_rap)

print("Writing File")
if not os.path.exists('./data/artists_genre_data/'):
    os.makedirs('./data/artists_genre_data/')
file = open("/Users/awells/UVA/DS5001/final/data/artists_genre_data/artistgenre.csv", "w")
file.write("name,genre\n")

write_to_csv(artists_genre_rnb)
write_to_csv(artists_genre_country)
write_to_csv(artists_genre_pop)
write_to_csv(artists_genre_rap)
file.close()
