import argparse
import re
import singleword
import positional
import stem
import phrase

def validateLine(document):
	"""
	checking if there are any comment lines
	returning lines without comment lines
	"""
	# for comment lines
	comment = re.compile(r"^<!--[ a-zA-Z0-9 =\/]*-->$")

	for i in document:
		match = comment.search(i)
		#match1 = blank.search(i)
		if not match:
			return i.split('\n')



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
		return pure[0]

def identifyDocument(row):
    print(row)



def readFile():
    """
    opening a file
    """
    for row in open("example.txt", "r"):
        if not row == "\n":
            yield row

def main():
    """
    Sole heart of the program.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("f",help="Please enter the filename to be indexed")
    parser.add_argument("t", help = "Please specify the type of index")
    args = parser.parse_args()

    if not args.f:
        print("Please Enter the File to Be Indexed")

    elif args.f:
        if args.t == "single":
            singleword.main(args.f)

        elif args.t == "pos":
            positional.main(args.f)

        elif args.t == "stem":
            stem.main(args.f)

        elif args.t == "phrase":
            phrase.main(args.f)

        else:
            print("Wrong Command")




if __name__ == "__main__":
    """
    Runs only if run as a script.
    """
    main()
