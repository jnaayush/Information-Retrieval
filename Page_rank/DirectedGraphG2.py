import os
from bs4 import BeautifulSoup

import csv

source_path = "HTMLPages_focused/"
destination_path = "DocIDs_focused/"


filename = "focused_Carbon_footprint_green.csv"

"""
gets the docId from the urls from each file and makes new file with just the DocIDs
"""
def getDocIDs():
    with open(filename,"r") as file:
        reader = csv.reader(file, delimiter=",")
        third_col = list(zip(*reader))[2]


    for linkName in third_col:
        seenList = []
        linkName = linkName.replace("|",",")
        linkName = linkName.replace("https://en.wikipedia.org/wiki/", "")
        doc_link = open(source_path + linkName +".txt", "r")
        docId = open(destination_path + linkName + ".txt","w")
        page_html = doc_link.read()
        page_soup = BeautifulSoup(page_html, "html.parser")
        linkList = page_soup.findAll('a')

        for link in linkList:

            class_name = link.get("class")
            url = link.get("href")
            if (type(class_name) is not list and type(url) is unicode):
                if (url[:6] == "/wiki/" and ':' not in url and '#' not in url and url != "/wiki/Main_Page"
                        and url not in seenList):
                    docId.write(url.replace("/wiki/","").encode('utf-8') + "\n")
                    seenList.append(url)

        docId.close()
        doc_link.close()
        file.close()
        print "success -> " + linkName

    file.close()

"""
Constructs the graphs with file containing the DocIds
"""
def constructGraph():
    graph = "G2.txt"
    fgraph = open(graph,"w")
    fileList = os.listdir("DocIDs_focused/")
    filename = "DocID_focused_Carbon_footPrint.csv"
    with open(filename,"r") as file:
        for line in file:
            line = line.replace("\n","")
            fgraph.write(line)
            print(line)
            for docID_file in fileList:
                docId_incoming = open("DocIDs_focused/" + docID_file,"r")
                docId_incoming_str = docId_incoming.read()
                if(line in docId_incoming_str and line != docID_file.replace(".txt","")):
                    print(" " + docID_file.replace(".txt",""))
                    fgraph.write(" " + docID_file.replace(".txt",""))

            fgraph.write("\n");

    file.close()
    fgraph.close()

"""
main function
"""
if __name__ == "__main__":
    getDocIDs()
    constructGraph()