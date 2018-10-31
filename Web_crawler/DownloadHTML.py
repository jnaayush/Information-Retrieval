import csv
import requests
import time
import sys

"""reads the file to test the links"""
filename = sys.argv[1]
with open(filename) as file:
    reader = csv.reader(file, delimiter=",")
    third_col = list(zip(*reader))[2]

"""tests all the links"""
for link in third_col:
    try:
        time.sleep(1)
        url = link.replace("|",",")
        uClient = requests.get(url)
        page_content = uClient.content
        uClient.close()
        print url + "  ->  success"
        filename = "HtmlPages/"+ url.split("/wiki/")[1] + ".txt"
        f = open(filename,"w")
        f.write(str(page_content))
        f.close
    except requests.exceptions.RequestException as e:
        print e
        print url + "  ->  fail"