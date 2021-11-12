import requests
from bs4 import BeautifulSoup
import csv 
import json 


URL = "https://housing.uga.edu/explore-options/"
page = requests.get(URL)



# exploreHall hosts name 
#explorePhoto hosts photo 

soup = BeautifulSoup(page.content, "html.parser")



hallList=[]
for item in soup.find_all('div', id='exploreHall'):
    item = item.get_text()
    item = str(item)
    hallList.append(item)


# multiple hall names, internal text. 
URL_INTERNAL=[]

for i in range(len(hallList)):
    URL_INTERNAL.append("https://housing.uga.edu/explore-options/"+hallList[i].strip().replace(' ', '-')+ "/")    

spans=[]
for i in range(len(URL_INTERNAL)):
    page_inside = requests.get(URL_INTERNAL[i])
    soup_inside = BeautifulSoup(page_inside.content, "html.parser")
    spans.append(soup_inside.find_all('span', {'class' : 'nearby-right'}))

# TODO: needs some scraping and cleaning and other shit like that... 


#break computer ✅
for i in range(len(spans)):
    print(spans[i])


#don't touch under, all of these work already. 

substring = "/sa_images/featured/"
photoList =[]
# ,id="explorePhoto"
for picture in soup.find_all("img"):
    #picture = str(picture)
    if substring in str(picture):
        picture = picture['src']
        photoList.append(picture)




res = {}
for key in hallList:
    for value in photoList:
        res[key] = value
        photoList.remove(value)
        break  


with open('some.csv', 'w') as csv_file:  
    writer = csv.writer(csv_file)
    for key, value in res.items():
       writer.writerow([key, value])


csvfile = open('some.csv', 'r')
jsonfile = open('file.json', 'w')

fieldnames = ("Name of Hall ", "Photo of Hall ")
reader = csv.DictReader( csvfile, fieldnames)
for row in reader:
    json.dump(row, jsonfile)
    jsonfile.write('\n')
