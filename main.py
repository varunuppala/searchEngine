'''
# TODO: searchEngine

'''


import argparse
import os
import sys


def checkParse():
	# Create the parser
	my_parser = argparse.ArgumentParser(description='List the content of a folder')

	# Add the arguments
	my_parser.add_argument('Path',
	                       metavar='path',
	                       type=str,
	                       help='the path to list')

	# Execute the parse_args() method
	args = my_parser.parse_args()

	input_path = args.Path

	if not os.path.isdir(input_path):
	    print('The path specified does not exist')
	    sys.exit()

	print('\n'.join(os.listdir(input_path)))



#Main function for all the calls to be made program
def main():
	checkParse()
	print("hello world")



# to call the main function
if __name__ == "__main__":
	main()
