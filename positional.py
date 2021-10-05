import re
import json
import singleword as sw
import os
import statistics
import string
import time
start_time = time.time()

pos_index = {}

fileno = []

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
            new.append(sw.htmlentities(i))

    tokenize(' '.join(new), documentnumber,m)


def removePunctuations(row):
    """
    removing punctuations from the string
    """
    punc = "!()-[]{};:'""\,<>``./?@#$%^&*_~"
    for ele in row:
        if ele in punc:
            row = row.replace(ele, " ")
    return row


def tokenize(doc, docno,m):
    """
    tokenizing positional index
    """
    doc1 = removePunctuations(doc)
    finaltokens = doc1.split(' ')


    for pos, term in enumerate(finaltokens):
        if term and term!=" ":
            if term in pos_index:
                pos_index[term][0] = pos_index[term][0] + 1
                if docno in pos_index[term][1]:
                    pos_index[term][1][docno].append(pos + 1)
                    if len(pos_index)==m:
                        # Saving the file if it hits the memory constraint
                        to_json(pos_index)
                        pos_index.clear()
                else:
                    pos_index[term][1][docno] = [pos + 1]
                    if len(pos_index)==m:
                        # Saving the file if it hits the memory constraint
                        to_json(pos_index)
                        pos_index.clear()
            else:
                pos_index[term] = []

                pos_index[term].append(1)

                pos_index[term].append({})

                pos_index[term][1][docno] = [pos + 1]
                if len(pos_index)==m:
                    # Saving the file if it hits the memory constraint
                    to_json(pos_index)
                    pos_index.clear()





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
                    dicto[term][0]+=pl[0]
                    for docid in pl[1]:
                        if docid in dicto[term][1]:
                            temp = pl[1][docid]
                            dicto[term][1][docid] += temp

                        else:
                            temp = pl[1]
                            dicto[term][1].update(temp)
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
    with open("output/final.json") as final:
        dict = json.load(final)
    filenos = {}
    for term,pl in dict.items():
        for doc,freq in pl[1].items():
            if doc in filenos:
                filenos[doc]+=1
            else:
                filenos[doc]=1

    frequency_list=list(filenos.values())

    lexicon = {}
    for i,j in dict.items():
        if i not in lexicon:
            lexicon[i]=len(j[1])
        else:
            lexicon[i]+=len(j[1])
    with open("output/lexicon.json","w") as out:
        json.dump(lexicon,out)

    print("\n")
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


def main(directory,m,output):
    documentnumber = 1
    validateLine(directory, documentnumber,m)
    to_json(pos_index)
    loading = (time.time() - start_time)*1000
    combine_json(output)
    describefile()
    final = (time.time() - start_time)*1000
    merging = (final - loading)
    print("--- %s seconds ---LOADING---" % loading)
    print("--- %s seconds ---MERGING---" % merging)
    print("--- %s seconds ---TOTAL---" % final)
