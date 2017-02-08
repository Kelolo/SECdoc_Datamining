import requests
import urllib
import re
try:
    from BeautifulSoup import BeautifulSoup
except ImportError:
    from bs4 import BeautifulSoup


# 1. Get response from URL
DocType = '13F'
CIK = '0001166559'

urlPre = 'https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK='
urlAfter = '&type=' + DocType + '&dateb=&owner=exclude&count=100'
url = urlPre + CIK + urlAfter

response = requests.get(url)

# print(response.text)

# 2. Parse HTML file
parsedHTML = BeautifulSoup(response.text, "html.parser")
# print(parsedHTML)

# 3. Find the required Link from parsed HTML and store them in a List
documentsLink = []

for link in parsedHTML.findAll('a'):
    # print(link.get('href'))
    usefullLink = link.get('href')
    p = re.compile("/Archives")
    m = p.match(usefullLink)
    # print(m)
    if m != None:
        documentsLink.append("".join(["https://www.sec.gov", usefullLink]))

# print(documentsLink)

# 4. For each link in the list, get required files (txt)

for url in documentsLink:
    subresponse = requests.get(url)
    subparsedHTML = BeautifulSoup(subresponse.text, "html.parser")
    print(subparsedHTML)

