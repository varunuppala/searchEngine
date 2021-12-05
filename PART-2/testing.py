"""
testing
"""
from pprint import pprint
def readFile():
	with open("P2files/queryfile.txt", 'rt') as f:
		for rows in open("P2files/queryfile.txt", "r"):
			yield rows



rows = readFile()
stack = []
string = ""
count = {}
j = 0
for i in rows:
    if i == "<narr> Narrative:\n":
        stack.append("1")  # appending in stack
    elif i == "</top>\n" and stack:
        stack.pop()
        count[j] = string
        j+=1
        string = ""

    elif stack:
        # Checking if match or not for comment lines and appending if required only
        string += i.strip("\n")+" "

print(count)


