import re
import json
import singleword as sw
import os

phrase_index_2 = {}

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
        s = finaltokens[j]+" "+finaltokens[j+1]
        if s not in phrase_index_2:
            phrase_index_2[s]=1
            if len(phrase_index_2)==m:
                to_json(phrase_index_2)
                phrase_index_2.clear()

        else:
            phrase_index_2[s]+=1
            if len(phrase_index_2)==m:
                #print("hi")
                to_json(phrase_index_2)
                phrase_index_2.clear()





def combine_json():
    files = readDirectory("output")
    for file in files:
        with open(file) as json_file:
            data = json.load(json_file)

        if os.path.exists("output/final.json"):
            with open("output/final.json") as final:
                dicto = json.load(final)
                for i in data.keys():
                    if i in dicto.keys():
                        dicto[i] += data[i]
                    else:
                        dicto[i] = data[i]

        else:
            with open("output/final.json","w") as final:
                json.dump(data,final)
        os.remove(file)



def to_json(dict):
    fileno.append(len(fileno)+1)
    with open("output/%s.json" %fileno[len(fileno)-1], "w") as outfile:
        json.dump(dict, outfile)




def main(directory,m):
    documentnumber = 1
    validateLine(directory, documentnumber,m)
    to_json(phrase_index_2)
    combine_json()
