import re
import json

pos_index = {}

def readFile(filename):
	for rows in open(filename, "r"):
		yield rows

def validateLine(filename,documentnumber):
	documentnumber = 1
	comment = re.compile(r"^<!--[ a-zA-Z0-9 =\/]*-->$")
	stack = []
	string = ''
	rows = readFile(filename)

	for i in rows:
		match = comment.search(i) #Checking commments
		if i == "<DOC>\n":
			stack.append("1")#appending in stack
		elif i == "</DOC>\n" and stack:
			stack.pop()
			nextString(string,documentnumber)
			string = ""
			documentnumber += 1

		elif not match:
			#Checking if match or not for comment lines and appending if required only
			string+=i


def nextString(s,documentnumber):
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
        	new.append(i)
	tokenize(new,documentnumber)




def tokenize(doc,docno):
	#geekforgeek
	finaltokens = doc
	for pos,term in enumerate(finaltokens):
		if term in pos_index:
		 pos_index[term][0] = pos_index[term][0] + 1
			if docno in pos_index[term][1]:
				pos_index[term][1][docno].append(pos+1)
			else:
				pos_index[term][1][docno] = [pos+1]
		else:
			pos_index[term] = []

			pos_index[term].append(1)

			pos_index[term].append({})

			pos_index[term][1][docno] = [pos+1]

	to_json(pos_index)


def to_json(dict):
	with open("sample.json","w") as outfile:
		json.dump(dict,outfile)


def main(filename):
	documentnumber = 1
	validateLine(filename,documentnumber)
	print(pos_index)
