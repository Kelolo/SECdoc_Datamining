import requests
import urllib
import xml.etree.cElementTree as et
from tabulate import tabulate
# from xml.dom import minidom
import re
try:
    from BeautifulSoup import BeautifulSoup
except ImportError:
    from bs4 import BeautifulSoup
# https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0001166559&type=13F&dateb=&owner=exclude&count=100

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
        return
    parseMethod2_Ready(parsedFile)

def parseMethod1_AllXML(parsedFile):
    print("**************** All_XML **********************")
    # print(len(parsedFile.findAll('xml')))
    # print(parsedFile)
    isFirstPart = True
    allRecords = []
    if "xml" not in str(parsedFile):
        parseMethod2_Ready(parsedFile)
        return

    for xml in parsedFile.find_all(re.compile("xml")):
        if (isFirstPart):
            header = ["Submission Type", "Live Test Flag", "CIK", "ccc", "Period Of Report",
                      "Report Calendar Or Quarter", "Is Amendment?", "Company Name", "Company Address: Street",
                      "Company Address: City", "Company Address: State", "Company Address: Zipcode", "Report Type",
                      "Form 13F file Number", "Provide Info for Instruction 5", "Name",
                      "Title", "Phone", "Sigature", "City", "State of Country", "Signature Date", "Other included managers count",
                      "Table Entry total", "Table Value Total", "Is Confidential Omitted"]

            # allRecords.append(header)
            for child in xml.find_all(True, recursive=False):
                subR = []
                for info in child.text.split('\n'):
                    # subR = []
                    if info != '':
                        subR.append(info)
                        # if isFirst:
                        #     oneRecord += info + "\t\t\t\t"
                        # else:
                        #     oneRecord += info + "\t\t\t"
                        #     isFirst = False
                # print(subR)
                # allRecords.append(subR)
                # print(child.name + ":" +child.text)
            for i in range (len(header)):
                print(header[i] + ": " + subR[i])
            print("\n$$$$$$$$$$$$$$$$$$$$$\n")
            isFirstPart = False
        else:
            # print("NAME OF ISSUER" + "\t\t\t\t" + "TITLE OF CLASS" + "\t\t\t" + "CUSIP" + "\t\t\t" + "VALUE(X1000)" + "\t\t\t" + "SHARES/PRN AMOUNT" + "\t\t\t" + "SH/PRN" + "\t\t\t" + "INVESTMENT DISCRETION" + "\t\t\t" + "OTHER MANAGERS" + "\t\t\t" + "SOLE" + "\t\t\t" + "SHARED" + "\t\t\t" + "NONE" + "\t\t\t")
            header = ["NAME OF ISSUER", "TITLE OF CLASS", "CUSIP", "VALUE(X1000)",
                      "SHARES/PRN AMOUNT", "SH/PRN", "INVESTMENT DISCRETION", "OTHER MANAGERS", "SOLE", "SHARED", "NONE"]
            allRecords.append(header)
            for information in parsedFile.find_all(re.compile("infotable")):
                # oneRecord = ""
                # isFirst = True
                # print(information.text.split('\n'))
                subR = []
                for info in information.text.split('\n'):
                    # subR = []
                    if info != '':
                        subR.append(info)
                        # if isFirst:
                        #     oneRecord += info + "\t\t\t\t"
                        # else:
                        #     oneRecord += info + "\t\t\t"
                        #     isFirst = False
                # print(subR)
                allRecords.append(subR)
            # print(allRecords)
            print(tabulate(allRecords))

    print("\n\n**********************************************************")
    print("************************* END OF *************************")
    print("**********************************************************\n\n")

def parseMethod2_Ready(parsedFile):
    print("***************** Partial ready ******************")
    for child in parsedFile.find_all(True, recursive=False):
        print(child.text)


# Main Program
DocType = '13F'
CIK = '0001166559'
requiredFileType = ".txt"

url = constructURLfromCIKandDocType(CIK, DocType)
parsedHTML = inputURLgetParsedHTML(url)
documentsLink = findAllArchieveLink(parsedHTML) # find all 13F link

# Note for no 13F found
if len(documentsLink) == 0:
    print("Warning: No 13F filing found for \n\tCIK/TICKER:" + str(CIK) + " \nYou can search another Ticker/CIK")

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
