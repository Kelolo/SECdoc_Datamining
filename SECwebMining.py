import requests
import sys
from tabulate import tabulate
import re
try:
    from BeautifulSoup import BeautifulSoup
except ImportError:
    from bs4 import BeautifulSoup


# Use different CIK/Ticker to construct the initial searching link
def constructURLfromCIKandDocType(CIK, DocType):
    urlPre = 'https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK='
    urlAfter = '&type=' + DocType + '&dateb=&owner=exclude&count=100'
    url = urlPre + CIK + urlAfter
    return url

# input an URL and return a parsed HTML as a BeautifulSoup object
def inputURLgetParsedHTML(url):
    response = requests.get(url)
    parsedHTML = BeautifulSoup(response.text, "html.parser")
    return parsedHTML

# this function will return all 13F links as list
def findAllArchieveLink(parsedHTML):
    documentsLink = []

    for link in parsedHTML.findAll('a'):
        usefullLink = link.get('href')
        p = re.compile("/Archives")
        m = p.match(usefullLink)
        if m != None:
            documentsLink.append("".join(["https://www.sec.gov", usefullLink]))
    return documentsLink

# this function will return a list of targeted txt file link. eg. https://www.sec.gov/Archives/edgar/data/1166559/000110465914039387/0001104659-14-039387.txt
def findAllRequiredFileType(parsedHTML, requiredFileType):
    documentsLink = []

    for link in parsedHTML.findAll('a'):
        usefullLink = link.get('href')
        p = re.compile("/Archives")
        m = p.match(usefullLink)
        if m != None and requiredFileType in usefullLink and (usefullLink[-5].isdigit()): # illiminate txt file with char name
            documentsLink.append("".join(["https://www.sec.gov", usefullLink]))
    return documentsLink

# this function will parse the file Data with two methods
def parseXMLFromSoupObj(fileURL):
    parsedFile = inputURLgetParsedHTML(fileURL)
    txtFile = str(parsedFile)
    if txtFile[0] == '<':
        parseMethod1_AllXML(parsedFile, txtFile)
        return
    parseMethod2_Ready(parsedFile)

# This is method 1, which will parse files where all holdings are wraped inside xml
def parseMethod1_AllXML(parsedFile, txtFile):
    print("\n**********************************************************")
    print("********************** Start OF 13F **********************")
    print("**********************************************************\n\n")

    isFirstPart = True
    allRecords = []
    if "xml" not in txtFile:
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

            for child in xml.find_all(True, recursive=False):
                subR = []
                for info in child.text.split('\n'):

                    if info != '':
                        subR.append(info)

            for i in range (len(header)):
                print(header[i] + ": " + subR[i])
            isFirstPart = False

        else:
            print("\n*********************************  FORM 13F INFORMATION TABLE  *********************************")
            header = ["NAME OF ISSUER", "TITLE OF CLASS", "CUSIP", "VALUE(X1000)",
                      "SHARES/PRN AMOUNT", "SH/PRN", "INVESTMENT DISCRETION", "OTHER MANAGERS", "SOLE", "SHARED", "NONE"]
            allRecords.append(header)
            for information in parsedFile.find_all(re.compile("infotable")):
                subR = []
                for info in information.text.split('\n'):
                    if info != '':
                        subR.append(info)
                allRecords.append(subR)
            print(tabulate(allRecords))

    print("\n**********************************************************")
    print("*********************** END OF 13F ***********************")
    print("**********************************************************\n\n")


# This is method 2, which will parse files with pre-parsed data
def parseMethod2_Ready(parsedFile):
    print("\n**********************************************************")
    print("********************** Start OF 13F **********************")
    print("**********************************************************\n\n")
    for child in parsedFile.find_all(True, recursive=False):
        print(child.text)
    print("\n**********************************************************")
    print("*********************** END OF 13F ***********************")
    print("**********************************************************\n\n")



########################################
####                                ####
####           Main Program         ####
####                                ####
###$$###################################

############################################################################################
#####                                                                                  #####
#####  1. Construct URL(L1) based on CIK/Ticker (optional: can also include data type) #####
#####  2. Parse the data in L1 (D1)                                                    #####
#####  3. Get all 13F links from D1 (L2)                                               #####
#####  4. Return warning if the CIK don't have any 13F filing                          #####
#####  5. For data in each link L2, parse the data and output newly construct table    #####
#####                                                                                  #####
############################################################################################

# CIK = input("Please Enter CIK/Ticker: ")
if len(sys.argv) == 1:
    CIK = input("Please Enter CIK/Ticker (eg. 0001166559): ")
else:
    CIK = sys.argv[1]

DocType = '13F'
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
    parseXMLFromSoupObj(RequiredFilesOfIndividual13F[0])

