import re
import json
import singleword as sw
import os
import pandas as pd
import statistics

phrase_index_2 = {}
lexicon = {}
fileno = []

def readDirectory(directory):
    files = os.listdir(directory)
    files = [directory+"/"+s for s in files]
    return files


def readFile(files):
    for i in files:
        with open(i, 'rt') as f:
            for rows in open(i, "r"):
                yield rows


def validateLine(directory, documentnumber,m):
    documentnumber = 1
    comment = re.compile(r"^<!--[ a-zA-Z0-9 =\/]*-->$")
    stack = []
    string = ''
    files = readDirectory(directory)
    rows = readFile(files)

    for i in rows:
        match = comment.search(i)  # Checking commments
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
    # Removing all the new text except for ones between texts
    # Removing additional tags also
    # print('Hello World')
    doc_re = re.compile(r'<DOCNO>.([A-Za-z_-][A-Za-z0-9_-]*).<\/DOCNO>')
    tags = re.compile(r"<[a-zA-Z\/]+>")
    start = s.find("<TEXT>") + len("<TEXT>")
    end = s.find("<\TEXT>") - len("<\TEXT>")
    text = s[start:end].lower()
    new = []
    for i in text.split("\n"):
        match = tags.search(i)
        if not match and i != "":
            new.append(sw.htmlentities(i))

    tokenize(' '.join(new), documentnumber,m)



def tokenize(doc, docno,m):
    """
    Tokenizing the document
    """

    finaltokens = doc.split(' ')
    for j in range(len(finaltokens)-1):
        if finaltokens[j]!= " " and finaltokens[j+1]!=" ":
            s = finaltokens[j]+" "+finaltokens[j+1]

        if s not in phrase_index_2:
            phrase_index_2[s]={}
            phrase_index_2[s][docno]=1
            if len(phrase_index_2)==m:
                to_json(phrase_index_2)


                phrase_index_2.clear()

        else:
            if docno not in phrase_index_2[s]:
                phrase_index_2[s][docno]=1
            else:
                phrase_index_2[s][docno]+=1
            if len(phrase_index_2)==m:
                #print("hi")
                to_json(phrase_index_2)

                phrase_index_2.clear()




def combine_json(output):
    files = readDirectory(output)
    for i,file in enumerate(files):
        print(i)
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
    print("LOADING....")
    with open("output/%s.json" %fileno[len(fileno)-1], "w") as outfile:
        json.dump(dict, outfile)


def describefile():
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
        print("# size of lexicon : ",len(frequency_list))
        print("size of file in bytes : ",os.path.getsize("output/final.json"))
        print("Maximum document frequency : ",max(frequency_list))
        print("Minimum document frequency : ",min(frequency_list))
        print("Mean document frequency : ",statistics.mean(frequency_list))
        print("Median document frequency : ",statistics.median(frequency_list))





def main(directory,m,output):
    documentnumber = 1
    validateLine(directory, documentnumber,m)
    to_json(phrase_index_2)
    if m!=0:
        combine_json(output)
    describefile()
