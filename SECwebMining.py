import requests
import urllib
# from xml.dom import minidom
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
        usefullLink = link.get('href')
        p = re.compile("/Archives")
        m = p.match(usefullLink)
        if m != None:
            documentsLink.append("".join(["https://www.sec.gov", usefullLink]))
    return documentsLink

def findAllRequiredFileType(parsedHTML, requiredFileType):
    documentsLink = []

    for link in parsedHTML.findAll('a'):
        usefullLink = link.get('href')
        p = re.compile("/Archives")
        m = p.match(usefullLink)
        if m != None and requiredFileType in usefullLink and (usefullLink[-5].isdigit()): # find all requiredFile type (.txt)
            documentsLink.append("".join(["https://www.sec.gov", usefullLink]))
    return documentsLink


def parseXMLFromSoupObj(fileURL):
    parsedFile = inputURLgetParsedHTML(fileURL)
    if str(parsedFile)[0] == '<':
        parseMethod1_AllXML(parsedFile)
        print(parsedFile)
        return

    parseMethod2_Ready(parsedFile)
    print(parsedFile)
    return


def parseMethod1_AllXML(parsedFile):
    print("All_XML")


def parseMethod2_Ready(parsedFile):
    print("Partial ready")

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
    # print(RequiredFilesOfIndividual13F)
    # print(parseXMLinformationFromFile(RequiredFilesOfIndividual13F[0]))

    parseXMLFromSoupObj(RequiredFilesOfIndividual13F[0])

    # fileLink = RequiredFilesOfIndividual13F[0]
    # parsedFile = inputURLgetParsedHTML(fileLink)  # beautifulSoup obj
    # xmldoc = minidom.parseString(parsedFile)
    # print(xmldoc)

# print(RequiredFilesOfIndividual13F)
