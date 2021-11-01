"""
Does everything related to queries
1. identifying
2. pre-processing
"""
import re
import string
from nltk.stem import PorterStemmer

def extractFile(path):
    """
    Opening the document and giving us a generator object.
    """
    with open(path, 'rt') as f:
        for rows in open(path, "r"):
            yield rows

def identifyQuery(generator):
    """
    1. Identify each query and store them
    """
    querydict = {} #query dictonary
    qno = re.compile(r"<num> Number: ([\S]+)")#re for query number
    query = re.compile(r"<title> Topic: ([\S ]+)")#re for query
    #Iterate through the document through Generator
    for row in generator:
        nmatch = qno.search(row) #check query number
        qmatch = query.search(row) #check query
        if nmatch:
            number = nmatch.group(1) #extracting the number
        elif qmatch:
            query1 = qmatch.group(1) #extracting the query
            querydict[number] = query1

    #Query dictonary
    return querydict



def getStopWords():
    """
    Reading the stop words:
    returns a dictonary of stopWords
    """
    stopWords = {}
    with open("P2files/stops.txt") as f:
        for line in f:
            val = line.split()
            stopWords[val[0]] = 1
    return stopWords

def checkTokenType(row):
    # All the Regex
    a = []

    emailcheck = re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b")
    l = [x.group() for x in re.finditer(emailcheck, row)]
    row = re.sub(emailcheck, '', row)
    for i in l:
        a.append(i)

    dateword = re.compile(r"([a-z]+) ([\d]{1,2}), ([\d]+)")
    l = [x.group() for x in re.finditer(dateword, row)]
    row = re.sub(dateword, '', row)
    for i in l:
        months = {'january': '1', 'february': '2', 'march': '3', 'april': '4', 'may': '5', 'june': '6', 'july': '7',
                  'august': '8', 'september': '9', 'october': '10', 'november': '11', 'december': '12'}
        month = dateword.search(i).group(1)
        date = dateword.search(i).group(2)
        year = dateword.search(i).group(3)
        if month in months:
            a.append(months[month] + "/" + date + "/" + year)

    dateformat = re.compile(r"([0-9]{1,2})[\/-]([[0-9]{1,2})[\/-]([0-9]{4})")
    l = [x.group() for x in re.finditer(dateformat, row)]
    row = re.sub(dateformat, '', row)
    for i in l:
        month = dateformat.search(i).group(1)
        date = dateformat.search(i).group(2)
        year = dateformat.search(i).group(3)
        if int(month) > 0 and int(month) < 13 and int(date) > 0 and int(date) < 32 and int(year) > 1920 and int(
                year) < 2122:
            a.append(month + "/" + date + "/" + year)

    URLcheck = re.compile(r'[a-z]{3,4}[\.][\w]+[\.][a-z]{2,3}')
    l = [x.group() for x in re.finditer(URLcheck, row)]
    row = re.sub(URLcheck, '', row)
    for i in l:
        a.append(i)

    ipcheck = re.compile(r"((25[0-5]|(2[0-4]|1[0-9]|[1-9]|)[0-9])(\.(?!$)|$)){4}")
    l = [x.group() for x in re.finditer(ipcheck, row)]
    row = re.sub(ipcheck, '', row)
    for i in l:
        a.append(i)

    abbrevations = re.compile(r"((?:[a-zA-Z]+\.){2,})")  ### u.s.a
    l = [x.group() for x in re.finditer(r"((?:[a-zA-Z]+\.){2,})", row)]
    row = re.sub(abbrevations, '', row)
    for i in l:
        a.append(i.replace(".", ""))

    monetory = re.compile(r"[$]([\d,]+)")
    l = [x.group() for x in re.finditer(monetory, row)]
    row = re.sub(monetory, '', row)
    for i in l:
        a.append(i.replace("$", ""))

    digalpha = re.compile(r"[0-9]+[-][a-z]+")
    l = [x.group() for x in re.finditer(digalpha, row)]
    row = re.sub(digalpha, '', row)
    for i in l:
        b = i.split("-")
        for j in range(len(b)):
            if j % 2 == 1:
                a.append(b[j])
        a.append(i.replace("-", ""))

    alphdig = re.compile(r"([a-z]+)(-)([0-9]+)")
    l = [x.group() for x in re.finditer(alphdig, row)]
    row = re.sub(alphdig, '', row)
    for i in l:
        a.append(i.replace("-", ""))

    hyph = re.compile(r"(?=\S*[-])([a-zA-Z-]+)")
    l = [x.group() for x in re.finditer(hyph, row)]
    row = re.sub(hyph, '', row)
    for i in l:
        b = i.split("-")
        for j in b:
            a.append(j)
        a.append(i.replace("-", ""))

    fileextension = re.compile(r"(\w+)\.([a-z]{2,4})")
    l = [x.group() for x in re.finditer(fileextension, row)]
    row = re.sub(fileextension, '', row)
    for i in l:
        a.append(i.replace(".", ""))


    return row, " ".join(a)

def removePunctuations(row):
    """
    removing punctuations from the string
    """
    punc = "!()-[]{};:'""\``,<>./?@#$%^&*_~"
    for ele in row:
        if ele in punc:
            row = row.replace(ele, " ")
    return row

def singleindexQuery(queryDict):
    """
    pre process for single index search
    """
    #Getting the stopwords
    stopwords = getStopWords()
    for number,query in queryDict.items():

        #lowering the text
        text = query.lower()

        #removing stopwords
        text = " ".join(x for x in text.split(' ') if x not in stopwords)

        #removing regex
        doct,docregex = checkTokenType(text)

        #removing punctuations
        doc1 = removePunctuations(doct)

         #adding up everything
        doc1+=docregex

        #replacing the query with pre processed one
        queryDict[number] = [x for x in doc1.split(' ') if x != '']

    #return dictonary of preprocessed queries
    return queryDict

def posindexQuery(queryDict):
    """
    pre processing the queries according to pos index
    """
    for number,query in queryDict.items():

        #lowering the text
        query = query.lower()

        #removing punctuations
        query = removePunctuations(query)

        #replacing the query with pre processed one
        queryDict[number] = [x for x in query.split(' ') if x != '']

    return queryDict

def stemindexQuery(queryDict):
    """
    pre processing the queries according to stem index
    """
    ps = PorterStemmer()
    for number,query in queryDict.items():

        #lowering the text
        query = query.lower()

        #removing punctuations
        query = removePunctuations(query)

        #replacing the query with stem word
        queryDict[number] = [ps.stem(x) for x in query.split(' ') if x != '']

    return queryDict


def phraseindexQuery(queryDict):
    """
    pre processing the queries according to pos index
    """
    for number,query in queryDict.items():

        #lowering the text
        query = query.lower()

        #removing punctuations
        query = removePunctuations(query)

        phrases = query.split(' ')
        #replacing the query with phrases one
        queryDict[number] = [phrases[x]+" "+phrases[x+1] for x in range(len(phrases)-1) if phrases[x] != '' and phrases[x+1]!='']

        #if only one word in query
        if not queryDict[number]:
            queryDict[number] = phrases

    return queryDict







def main():
    #Path for the query file
    path = "/Users/varunuppala/Desktop/searchEngine/PART-2/P2files/queryfile.txt"

    #Open the Query file
    gen = extractFile(path)

    #Find each query
    querydict = identifyQuery(gen)

    return querydict
