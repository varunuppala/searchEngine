'''
# TODO: searchEngine
---> enter the filename and get the tokens out of it.
---> Get all the stop words to ignore them from the document.
---> tokenize the documents using the stop words list.
'''


#-------------import package/module----------------------------#
#
import argparse
import os
import sys
import re

#---------------- Validate Rows---------------------#
def validateLine():
	document = readFile()
	# for comment lines
	comment = re.compile(r"^<!--[ a-zA-Z0-9 =\/]*-->$")
	# for Blank Spaces
	#blank = re.compile(r"[\s]+")
	for i in document:
		match = comment.search(i)
		#match1 = blank.search(i)
		if match:
			pass
		else:
			print(i.split(' '))


#----------------Loading all the stopwords to check further-------------------------#

def getStopWords():
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
	#stroing document numbers
	documents = {}
	doc_re = re.compile(r'<DOCNO>.([A-Za-z_-][A-Za-z0-9_-]*).<\/DOCNO>')
	for i in document:
		match = doc_re.search(i)
		if match:
			documents[len(documents)+1] = match.group(1)
	for i in documents.values():
		print(i)








#----------------To read and yield each line of a file-------------------------#
def readFile():
	for row in open("example.txt", "r"):
		yield row

#-----------------Main function for all the calls to be made program------------------------#

def main():
	#s = input("enter a string")
	#readFile()
	validateLine()

#---------------------to call the main function----------------------------#


if __name__ == "__main__":
	main()
