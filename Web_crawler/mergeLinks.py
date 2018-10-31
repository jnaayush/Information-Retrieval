import csv
import sys

i = 0

"""opens file 'links_Time_zone.csv' """
files = [sys.argv[1],sys.argv[2],sys.argv[3]]
urls = []
for filename in files:
    print filename
    with open(filename) as file:
        reader = csv.reader(file, delimiter=",")
        urls.append(list(zip(*reader))[2])

"""opens file 'links_Electric_car.csv'
with open('links_Electric_car.csv') as file:
    reader = csv.reader(file, delimiter=",")
    eCUrl = list(zip(*reader))[2]

opens file 'links_Carbon_footprint.csv' 
with open('links_Carbon_footprint.csv') as file:
    reader = csv.reader(file, delimiter=",")
    cFUrl = list(zip(*reader))[2]
"""

filename = "mergedLinks.csv"
finalList = []
f = open(filename, "w")

"""the urls in the files are sorted by depth so fetches first 333 links from each of the file to maintain closeness 
to the frontier"""
for url in urls:
    for link in url:
        if (i == 333):
            i = 0
            break
        else:
            print str(i) + "\t" + link
            if (link not in finalList):
                finalList.append(link)
                i = i + 1
                
for link in finalList:
    f.write(link + "\n")

f.close()