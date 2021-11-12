import re
import json
import singleword as sw
import os
import pandas as pd
import statistics
import string
from nltk.stem import PorterStemmer
import time
start_time = time.time()

stem_index = {}
fileno = []
doclist = {}

def readDirectory(directory):
    """
    Reads the files in the directory
    """
    files = os.listdir(directory)
    files = [directory+"/"+s for s in files]
    return files


def readFile(files):
    """
    Yields generators
    """
    for i in files:
        with open(i, 'rt') as f:
            for rows in open(i, "r"):
                yield rows


def validateLine(directory, documentnumber,m):
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
            #for document number and length
            l = []
            l.append(docmatch.group(1))
            doclist[documentnumber] = l
        if i == "<DOC>\n":
            stack.append("1")  # appending in stack
        elif i == "</DOC>\n" and stack:
            stack.pop()
            nextString(string, documentnumber,m)
            string = ""
            documentnumber += 1

        elif not match:
            # Checking if match or not for comment lines and appending if required only
            string += i


def nextString(s, documentnumber,m):
    """
    Removing all the new text except for ones between texts
    Removing additional tags also
    """
    doc_re = re.compile(r'<DOCNO>.([A-Za-z_-][A-Za-z0-9_-]*).<\/DOCNO>')
    tags = re.compile(r"<[a-zA-Z\/]+>")
    start = s.find("<TEXT>") + len("<TEXT>")
    end = s.find("<\TEXT>") - len("<\TEXT>")
    text = s[start:end].lower()
    doclist[documentnumber].append(len(text.split())) 
    new = []
    for i in text.split("\n"):
        match = tags.search(i)
        if not match and i != "":
            new.append(sw.htmlentities(i))

    tokenize(' '.join(new), documentnumber,m)

def removePunctuations(row):
    """
    removing punctuations from the string
    """
    punc = "!()-[]{};:'""\,<>./?@#$%^&*_~"
    for ele in row:
        if ele in punc:
            row = row.replace(ele, " ")
    return row


def tokenize(doc, docno,m):
    """
    Tokenizing the document
    """
    ps = PorterStemmer()
    doc1 = removePunctuations(doc)
    finaltokens = doc1.split(' ')
    for j in range(len(finaltokens)-1):
        if finaltokens[j] and finaltokens[j]!= " " :
            s = ps.stem(finaltokens[j])


            if s not in stem_index:
                stem_index[s]={}
                stem_index[s][docno]=1
                if len(stem_index)==m:
                    # Saving the file if it hits the memory constraint
                    to_json(stem_index)
                    stem_index.clear()

            else:
                if docno not in stem_index[s]:
                    stem_index[s][docno]=1
                else:
                    stem_index[s][docno]+=1
                    if len(stem_index)==m:
                        # Saving the file if it hits the memory constraint
                        to_json(stem_index)
                        stem_index.clear()




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
            with open("output/stem/final.json","w") as final:
                json.dump(present,final)
        else:
            with open("output/stem/final.json") as df1:
                dicto = json.load(df1)

            for term,pl in present.items():
                if term in dicto:
                    for docid in pl:
                        temp = pl
                        dicto[term].update(temp)
                else:
                    dicto[term] = pl

            with open("output/stem/final.json","w") as df2:
                json.dump(dicto,df2)



def to_json(dict):
    fileno.append(len(fileno)+1)
    print("Loading"+"."*((len(fileno)%10)+1))
    with open("output/stem/%s.json" %fileno[len(fileno)-1], "w") as outfile:
        json.dump(dict, outfile)


def describefile():
        """
        Describes the file with max mean min document frequency
        """
        with open("output/stem/final.json") as final:
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
        with open("output/stem/lexicon.json","w") as out:
            json.dump(lexicon,out)

        print("# size of lexicon : ",len(dict))
        print("\n")
        print("size of file in bytes : ",os.path.getsize("output/stem/final.json")+os.path.getsize("output/stem/lexicon.json"))
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



def main(directory,m,output):
    documentnumber = 1
    validateLine(directory, documentnumber,m)
    to_json(stem_index)
    loading = (time.time() - start_time)*1000
    combine_json(output)
    describefile()
    final = (time.time() - start_time)*1000
    merging = (final - loading)
    doclist_json(doclist)
    print("--- %s seconds ---LOADING---" % loading)
    print("--- %s seconds ---MERGING---" % merging)
    print("--- %s seconds ---TOTAL---" % final)
