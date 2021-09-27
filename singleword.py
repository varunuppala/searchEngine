'''
# TODO: searchEngine
---> enter the filename and get the tokens out of it.
---> Get all the stop words to ignore them from the document.
---> tokenize the documents using the stop words list.
'''
dict = {}

#-------------import package/module----------------------------#
#
import argparse
import os
import sys
import re
import string
import json

#---------------- Validate Rows---------------------#
def validateLine(filename):
	"""
	checking if there are any comment lines
	returning lines without comment lines
	"""
	document = readFile(filename)
	# for comment lines
	comment = re.compile(r"^<!--[ a-zA-Z0-9 =\/]*-->$")

	for i in document:
		match = comment.search(i)
		#match1 = blank.search(i)
		if not match:
			removeNewLine(i.split('\n'))

#------------------------------------------------------------------------

def removeNewLine(l):
	"""
	removing all the blank lines
	returns pure lines
	"""
	pure = []
	for i in l:
		if i:
			pure.append(i)
	if pure:
		handletags(pure[0])

#-----------------------------------------------------------------------

def handletags(row):
	"""
	handles tags for example <doc>
	returns lines without them
	"""
	tags = re.compile(r"<[a-zA-Z\/]+>")
	match = tags.search(row)
	if match:
		pass
	else:
		removePunctuations(row.lower())

def checkTokenType(row):
	htmlentity = {'&blank;':' ','&hyph;':'-','&sect;':'§','&times':'x'}
	row = row.split(' ')
	# All the Regex
	abbrevations = re.compile(r"[a-z]+[.][a-z]+") ### u.s.a
	monetory = re.compile(r"[$]([\d,]+)")#$20
	digsepbycomma = re.compile(r"[\^\d]+[\,][\d]")
	hyph = re.compile(r"(?=\S*['-])([a-zA-Z'-]+)")
	digalpha = re.compile(r"([0-9]+)(-)([a-z]+)")
	alphdig = re.compile(r"([a-z]+)(-)([0-9]+)")
	onlyalpha = re.compile(r"([a-z]+)")
	fileextension = re.compile(r"[a-z0-9]+[.][\a-z]{2,4}$")
	emailcheck = re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b")
	URLcheck = re.compile(r'(http|ftp|https):\/\/([\w\-_]+(?:(?:\.[\w\-_]+)+))([\w\-\.,@?^=%&:/~\+#]*[\w\-\@?^=%&/~\+#])?')
	ipcheck = re.compile(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$')

	for i in row:
		#Step a
		if (abbrevations.search(i)):
			j = i.replace('.',"")
			removePunctuations(j)

		#monetory search step b
		elif(monetory.search(i)):

			if (digsepbycomma.search(monetory.search(i).group(1))):
				j=monetory.search(i).group(1)
				j = j.replace(',',"")
				removePunctuations(str(int(float(j))))
			else:
				removePunctuations(monetory.search(i).group(1))

		#Hyphene search step c,d,e
		elif (hyph.search(i)):
			if digalpha.search(i):
				removePunctuations(digalpha.search(i).group(1)+digalpha.search(i).group(3))
				if (len(digalpha.search(i).group(3)) > 2):
					removePunctuations(digalpha.search(i).group(3))
			elif alphdig.search(i):
				removePunctuations(alphdig.search(i).group(1)+alphdig.search(i).group(3))
				if len(alphdig.search(i).group(1))>2:
					removePunctuations(alphdig.search(i).group(1))


		#Dates
		#number formatting
		elif (digsepbycomma.search(i)):

			j = i.replace(',',"")
			removePunctuations(str(int(float(j))))


		#file extensions
		elif (fileextension.search(i)):

			i = i.replace('.','')
			removePunctuations(i)

		#email
		elif (emailcheck.search(i)):

			removePunctuations(i)

		#ip address
		elif (ipcheck.search(i)):
			removePunctuations(i)

		#urls
		elif (URLcheck.search(i)):
			removePunctuations(i)

		else:
			removePunctuations(i)


def htmlentities(row):
	htmlentity = {'&blank':' ','&hyph':'-','&sect':'§','&times':'x'}
	row = row.split(';')
	for i in row:
		if i in htmlentity.keys():
			i = ""
	return "".join(i)


def removePunctuations(row):
	"""
	removing punctuations
	"""
	s = ''.join(c for c in row if c not in string.punctuation)
	tokenize(s)



def tokenize(row):
		"""
		catch the tokens clean them and hold in memory

		"""
		stopwords=getStopWords()
		for i in row.split(" "):
			if i not in stopwords.keys():
				if i not in dict:
					dict[i] = ""





#----------------Loading all the stopwords to check further-------------------------#
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

#--------------to check the document lines----------------------------#
def identifyTokens():
	stopWords= getStopWords()
	document = readFile()
	#storing document numbers
	documents = {}
	doc_re = re.compile(r'<DOCNO>.([A-Za-z_-][A-Za-z0-9_-]*).<\/DOCNO>')
	for i in document:
		match = doc_re.search(i)
		if match:
			documents[len(documents)+1] = match.group(1)
	for i in documents.values():
		print(i)



#----------------To read and yield each line of a file-------------------------
def readFile(filename):
	for row in open(filename, "r"):
		yield row

def to_json(dict):
	with open("sample.json","w") as outfile:
		json.dump(dict,outfile)

#-----------------Main function for all the calls to be made program------------------------#
def main(filename):
	#s = input("enter a string")
	#readFile()
	validateLine(filename)
	to_json(dict)


#---------------------to call the main function----------------------------
if __name__ == "__main__":
	main()
