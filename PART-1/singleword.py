import argparse
import os
import sys
import re
import string
import json
import statistics
import warnings
import time

start_time = time.time()

warnings.filterwarnings('ignore')

single_index = {}
fileno = []
doclist = {}


def htmlentities(row):
    row = row.replace("&blank;", ' ')
    row = row.replace("&hyph;", ' ')
    row = row.replace("sect;", ' ')
    row = row.replace("&times;", ' ')
    row = row.replace("&para;", ' ')
    return row


def readDirectory(directory):
    """
    Reads the files in the directory
    """
    files = os.listdir(directory)
    files = [directory + "/" + s for s in files]
    return files


def readFile(files):
    """
    Yields generators
    """
    for i in files:
        with open(i, 'rt') as f:
            for rows in open(i, "r"):
                yield rows


def validateLine(directory, documentnumber, m):
    """
    Reads line by line, sums up a document and passes it for tokenizing
    """
    documentnumber = 1
    comment = re.compile(r"^<!--[ a-zA-Z0-9 =\/]*-->$")
    docno = re.compile(r"<DOCNO> ([A-Z0-9\-]+) <\/DOCNO>")
    stack = []
    string = ''
    files = readDirectory(directory)
    rows = readFile(files)

    for i in rows:
        match = comment.search(i)  # Checking commments
        docmatch = docno.search(i)
        if docmatch:
            doclist[documentnumber] = docmatch.group(1)
        if i == "<DOC>\n":
            stack.append("1")  # appending in stack
        elif i == "</DOC>\n" and stack:
            stack.pop()
            nextString(string, documentnumber, m)
            string = ""
            documentnumber += 1

        elif not match:
            # Checking if match or not for comment lines and appending if required only
            string += i



def nextString(s, documentnumber, m):
    """
    Removing all the new text except for ones between texts
    Removing additional tags also
    """
    doc_re = re.compile(r'<DOCNO>.([A-Za-z_-][A-Za-z0-9_-]*).<\/DOCNO>')
    tags = re.compile(r"<[a-zA-Z\/]+>")
    start = s.find("<TEXT>") + len("<TEXT>")
    end = s.find("<\TEXT>") - len("<\TEXT>")
    text = s[start:end].lower()
    new = []
    for i in text.split("\n"):
        match = tags.search(i)
        if not match and i != "":
            new.append(htmlentities(i))

    tokenize(' '.join(new), documentnumber, m)


def removePunctuations(row):
    """
    removing punctuations from the string
    """
    punc = "!()-[]{};:'""\``,<>./?@#$%^&*_~"
    for ele in row:
        if ele in punc:
            row = row.replace(ele, " ")
    return row


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



def getStopWords():
    """
    Reading the stop words:
    returns a dictonary of stopWords
    """
    stopWords = {}
    with open("stops.txt") as f:
        for line in f:
            val = line.split()
            stopWords[val[0]] = 1
    return stopWords



def tokenize(doc, docno, m):
    """
    tokenizing positional index
    """

    doct,docregex = checkTokenType(doc)
    doc1 = removePunctuations(doct)
    doc1+=docregex
    finaltokens = doc1.split(' ')
    stopwords = getStopWords()
    for j in range(len(finaltokens)-1):
        if finaltokens[j] and finaltokens[j]!= " " and finaltokens[j] not in stopwords:
            s=finaltokens[j]


            if s not in single_index:
                single_index[s]={}
                single_index[s][docno]=1
                if len(single_index)==m:
                    # Saving the file if it hits the memory constraint
                    to_json(single_index)
                    single_index.clear()

            else:
                if docno not in single_index[s]:
                    single_index[s][docno]=1
                else:
                    single_index[s][docno]+=1
                    if len(single_index)==m:
                        # Saving the file if it hits the memory constraint
                        to_json(single_index)
                        single_index.clear()




def combine_json(output):
    """
    Merging all the indexes
    """
    files = readDirectory(output)
    for i,file in enumerate(files):
        print("Merging"+"."*((i%10)+1))
        with open(file) as json_file:
            present = json.load(json_file)

        os.remove(file)

        if i == 0:
            with open("output/final.json","w") as final:
                json.dump(present,final)
        else:
            with open("output/final.json") as df1:
                dicto = json.load(df1)

            for term,pl in present.items():
                if term in dicto:
                    for docid in pl:
                        temp = pl
                        dicto[term].update(temp)
                else:
                    dicto[term] = pl

            with open("output/final.json","w") as df2:
                json.dump(dicto,df2)



def to_json(dict):
    fileno.append(len(fileno)+1)
    print("Loading"+"."*((len(fileno)%10)+1))
    with open("output/%s.json" %fileno[len(fileno)-1], "w") as outfile:
        json.dump(dict, outfile)


def describefile():
        """
        Describes the file with max mean min document frequency
        """
        with open("output/final.json") as final:
            dict = json.load(final)
        filenos = {}
        for term,pl in dict.items():
            for doc,freq in pl.items():
                if doc in filenos:
                    filenos[doc]+=1
                else:
                    filenos[doc]=1
        frequency_list=list(filenos.values())

        lexicon = {}
        for i,j in dict.items():
            if i not in lexicon:
                lexicon[i]=len(j)
            else:
                lexicon[i]+=len(j)
        with open("output/lexicon.json","w") as out:
            json.dump(lexicon,out)

        print("# size of lexicon : ",len(dict))
        print("\n")
        print("size of file in bytes : ",os.path.getsize("output/final.json")+os.path.getsize("output/lexicon.json"))
        print("\n")
        print("Maximum document frequency : ",max(frequency_list))
        print("\n")
        print("Minimum document frequency : ",min(frequency_list))
        print("\n")
        print("Mean document frequency : ",statistics.mean(frequency_list))
        print("\n")
        print("Median document frequency : ",statistics.median(frequency_list))
        print("\n")

def doclist_json(doclist):
    f = open("Output/documentlist.json", "w")
    json.dump(doclist, f)
    f.close()


def main(directory, m, output):
    documentnumber = 1
    validateLine(directory, documentnumber, m)
    to_json(single_index)
    loading = (time.time() - start_time)*1000
    combine_json(output)
    describefile()
    final = (time.time() - start_time)*1000
    merging = (final - loading)
    doclist_json(doclist)
    print("--- %s seconds ---LOADING---" % loading)
    print("--- %s seconds ---MERGING---" % merging)
    print("--- %s seconds ---TOTAL---" % final)
