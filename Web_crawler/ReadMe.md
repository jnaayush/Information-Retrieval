ReadMe

Dependencies:
1.BeautifulSoup
2.requests
3.time
4.sys


Task 1:

Files:
1. webCrawler.py

Usage : python webCrawler.py [article]
eg. 	python webCrawler.py Time_zone
	python webCrawler.py Electric_car
        python webCrawler.py Carbon_footprint
Result:
Output has 3 columns:

Depth	Source	url


2. DownloadHTML.py

Usage: python DownloadHTML.py [filename]
eg.    python DownloadHTML.py links_Time_zone.csv

It took way too long to fetch every link so I separated the get Links from the download html

Task 2:

File: mergeLinks.py

Usage: python mergeLinks.py [file1] [file2] [file3]
eg. python mergeLinks.py links_Time_zone.csv links_Electric_car.csv links_Carbon_footprint.csv

Task 3:
File: focusedCrawling.py

Usage: python focusedCrawling.py [article] [focustext]
eg.    python focusedCrawling.py Carbon_footprint green

Depth reached :

Task 1 : 3
Task 2 : 3
Task 3 : 6
