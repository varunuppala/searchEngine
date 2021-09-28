import re
import json
import singleword as sw

phrase_index = {}


def readFile(filename):
    for rows in open(filename, "r"):
        yield rows


def validateLine(filename, documentnumber):
    documentnumber = 1
    comment = re.compile(r"^<!--[ a-zA-Z0-9 =\/]*-->$")
    stack = []
    string = ''
    rows = readFile(filename)

    for i in rows:
        match = comment.search(i)  # Checking commments
        if i == "<DOC>\n":
            stack.append("1")  # appending in stack
        elif i == "</DOC>\n" and stack:
            stack.pop()
            nextString(string, documentnumber)
            string = ""
            documentnumber += 1

        elif not match:
            # Checking if match or not for comment lines and appending if required only
            string += i


def nextString(s, documentnumber):
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

    tokenize(''.join(new), documentnumber)
    #print(''.join(new))


def tokenize(doc, docno):
    # geekforgeek
    finaltokens = doc.split(' ')



def to_json(dict):
    with open("sample.json", "w") as outfile:
        json.dump(dict, outfile)


def main(filename):
    documentnumber = 1
    validateLine(filename, documentnumber)
    print(phrase_index)
