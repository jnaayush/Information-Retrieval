from bs4 import BeautifulSoup
import requests
import time
import sys
reload(sys)
sys.setdefaultencoding('utf8')


"""global variable for list of url and seen list"""
urlList = []
seenUrl = []

"""
A class which is hold data and attributes for a url
url -> the url itself
depth -> depth of the url
source -> the source page which lead to this url
text -> the anchor text of the url

"""
class urlItem:
    def __init__(self,url,depth,source,text):
        self.depth = depth
        self.url = url
        self.source = source
        self.text = text

"""
checks for the focus text in the url and anchor text,
every word that begins with focus text or is a focus text is considered to be the target,
this checks url and text in a case-insensitive manner  
"""
def checkFocusText(splitText,splitUrl,focusText):
    result = False
    textListWithGreen = filter(lambda x: focusText in x, splitText)
    for word in textListWithGreen:
        if(word.startswith(focusText)):
            result = result or True
    urlListWithGreen = filter(lambda x: focusText in x, splitUrl)
    for word in urlListWithGreen:
        if (word.startswith(focusText)):
            result = result or True
    return result

"""
this function does the crawling.
It maintains a url List containing the urls and a seen list which has contains urls which have been seen.
only the wiki article (url begining with /wiki/)are recorded. The re-directions, administrative links, side links
wiki main page are not recorded.  
"""
def crawl(listUrlItem,depth,focusText):

    for url_item in listUrlItem:
        if(url_item.url in seenUrl):
            return
        if (len(urlList) >= 1000):
            return
        if (url_item.depth >= 6):
            return

        time.sleep(1)
        try:
            uClient = requests.get('https://en.wikipedia.org' + url_item.url)
            #print url_item.url
        except requests.exceptions.RequestException as e:  # This is the correct syntax
            print e

        page_html = uClient.text
        uClient.close()
        page_soup = BeautifulSoup(page_html,"html.parser")
        linkList = page_soup.findAll('a')
        seenUrl.append(url_item.url)

        for link in linkList:
            class_name = link.get("class")
            url = link.get("href")
            if (type(class_name) is not list and type(url) is unicode):
                if(url[:6] == "/wiki/" and ':' not in url and '#' not in url and url != "/wiki/Main_Page"):
                    if(url not in urlList and len(urlList) < 1000):
                        urlLower = url.lower()
                        textLower = link.text.lower()
                        splitUrl = urlLower.split("_-")
                        splitText = textLower.split(" ")
                        if (checkFocusText(splitText,splitUrl,focusText)):
                            print(url_item.url + "\t" + str(url_item.depth+1) +  "\t " + url + "\t")
                            url_new = urlItem(url,url_item.depth+1,url_item.url,link.text)
                            listUrlItem.append(url_new)
                            urlList.append(url)


    crawl(listUrlItem, depth + 1,focusText)


""" main function
    entry point of the crawler, initializes the lists, fires the crawling functions and populates the file
"""
def main():

    article = sys.argv[1]
    focusText = sys.argv[2]
    filename = "focused_" + article + "_" + focusText + ".csv";
    f = open(filename, "w")
    url = "/wiki/" + article;
    listUrlItem = []
    seed = urlItem(url,1,url,"none")
    urlList.append(url)
    listUrlItem.append(seed)

    crawl(listUrlItem,1,focusText)

    i = 0
    for url_item in listUrlItem:
        print(str(i) + "\t" + str(url_item.depth) + "\t" + 'https://en.wikipedia.org' +  url_item.url)
        f.write(str(url_item.depth) + ","+ url_item.source + "," + 'https://en.wikipedia.org' +
                url_item.url.replace(",", "|").encode('utf-8') + "," + url_item.text.replace(",","|").encode('utf-8')
                +"\n")
        i = i + 1

    f.close()

"""fires the main function"""
if __name__ == "__main__":
    main()