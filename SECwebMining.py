import requests
import urllib
import re
try:
    from BeautifulSoup import BeautifulSoup
except ImportError:
    from bs4 import BeautifulSoup


def constructURLfromCIKandDocType(CIK, DocType):
    urlPre = 'https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK='
    urlAfter = '&type=' + DocType + '&dateb=&owner=exclude&count=100'
    url = urlPre + CIK + urlAfter
    return url

def inputURLgetParsedHTML(url):
    response = requests.get(url)
    parsedHTML = BeautifulSoup(response.text, "html.parser")
    return parsedHTML

def findAllArchieveLink(parsedHTML):
    documentsLink = []

    for link in parsedHTML.findAll('a'):
        # print(link.get('href'))
        usefullLink = link.get('href')
        # print(usefullLink)
        p = re.compile("/Archives")
        m = p.match(usefullLink)
        # print(m)
        if m != None:
            documentsLink.append("".join(["https://www.sec.gov", usefullLink]))
    return documentsLink

def findAllRequiredFileType(parsedHTML, requiredFileType):
    documentsLink = []

    for link in parsedHTML.findAll('a'):
        # print(link.get('href'))
        usefullLink = link.get('href')
        # print(usefullLink)
        p = re.compile("/Archives")
        m = p.match(usefullLink)
        # print(m)
        if m != None and requiredFileType in usefullLink and (usefullLink[-5].isdigit()): # find all requiredFile type (.txt)
            documentsLink.append("".join(["https://www.sec.gov", usefullLink]))
    return documentsLink


# Main Program

DocType = '13F'
CIK = '0001166559'
requiredFileType = ".txt"

url = constructURLfromCIKandDocType(CIK, DocType)
parsedHTML = inputURLgetParsedHTML(url)
documentsLink = findAllArchieveLink(parsedHTML) # find all 13F link


for link in documentsLink:
    parsedHTML = inputURLgetParsedHTML(link)
    RequiredFilesOfIndividual13F = findAllRequiredFileType(parsedHTML, requiredFileType) # find requiredFileType of individual 13F
    print(RequiredFilesOfIndividual13F)

# print(RequiredFilesOfIndividual13F)
