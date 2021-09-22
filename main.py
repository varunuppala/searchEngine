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

#---------------- Validate Rows---------------------#
def validateLine():
	"""
	checking if there are any comment lines
	returning lines without comment lines
	"""
	document = readFile()
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

def removePunctuations(row):
	s = ''.join(c for c in row if c not in string.punctuation)
	if " " in s:
		tokenize(s)





def tokenize(row):
		"""
		catch the tokens clean them and hold in memory

		"""
		stopwords=getStopWords()
		for i in row.split(" "):
			if i not in stopwords.keys():
				if i not in dict:
					dict[i] = 1






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
	stopWords=getStopWords()
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
def readFile():
	for row in open("example.txt", "r"):
		yield row

#-----------------Main function for all the calls to be made program------------------------#
def main():
	#s = input("enter a string")
	#readFile()
	validateLine()
	for i in dict:
		print(i)

#---------------------to call the main function----------------------------
if __name__ == "__main__":
	main()
