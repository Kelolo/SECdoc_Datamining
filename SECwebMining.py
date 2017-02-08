import requests
import urllib
import re
try:
    from BeautifulSoup import BeautifulSoup
except ImportError:
    from bs4 import BeautifulSoup


# 1. Get response from URL
url = 'https://www.sec.gov/cgi-bin/browse-edgar?CIK=0001166559&owner=exclude&action=getcompany&Find=Search'
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
    print(m)
    if m != None:
        documentsLink.append("".join(["https://www.sec.gov", usefullLink]))

print(documentsLink)

# 4. For each link in the list, download required files into dir
