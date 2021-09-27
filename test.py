"""
#ALPHABET-DIGIT
import re
rx2 = r"([a-z]+)(-)([0-9]+)"
s = "f-16 i-20 cdc-50"
s = s.split(' ')
typ2 = re.compile(rx2)

for i in s:
    match = typ2.search(i)
    print(match.group(1)+match.group(3))
    if len(match.group(1))>2:
        print(match.group(1))

"""
"""
#DIGIT ALPHABET
import re

rx2 = r"([0-9]+)(-)([a-z]+)"
s = "1-hour 1-h 50-over"
s = s.split(' ')

typ2 = re.compile(rx2)

for i in s:
    match = typ2.search(i)
    print(match.group(1)+match.group(3))

    if len(match.group(3))>2:
        print(match.group(3))
"""

import re
s = "parts-of-speech"
hyph = re.compile(r"(?=\S*['-])([a-zA-Z'-]+)")
digalpha = re.compile(r"([0-9]+)(-)([a-z]+)")
alphdig = re.compile(r"([a-z]+)(-)([0-9]+)")
onlyalpha = re.compile(r"([a-z]+)")
for i in s.split(' '):

    match = hyph.search(i)
    if match:
        print(i)
        if digalpha.search(i):
            print(digalpha.search(i).group(1)+digalpha.search(i).group(3))
            if len(digalpha.search(i).group(3))>2:
                print(digalpha.search(i).group(3))

        elif alphdig.search(i):
            print(alphdig.search(i).group(1)+alphdig.search(i).group(3))
            if len(alphdig.search(i).group(1))>2:
                print(alphdig.search(i).group(1))
        else:
            print(x for x in match.group(1))
            print(match.group(1))





	"""for i in doc.split(' '):
			print(i)
			if i not in dictonary:
				document = {}
				document[docno] = [flag]
				dictonary[i] = document
			else:
				if docno not in dictonary.values():
					print(flag)
					document = {}
					document[docno] = [flag]
					dictonary[i] = document
				else:
					x = dictonary[i]
					print(x[docno])
					x[docno].append(flag)
					dictonary[i] = x
			flag+=1"""
