import argparse
import sys
import re
sys.path.insert(1, 'P1-packages')
import singleword
import os

# insert at 1, 0 is the script path (or '' in REPL)



def main():
    """
    Sole heart of the program.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("f",help="Please enter the filename to be indexed")
    args = parser.parse_args()
    outz = "output/single"
    
    isExist = os.path.exists(outz)

    if not isExist:
        os.makedirs(outz)

    files = os.listdir(outz)

    for i in files:
        if os.path.exists("output/%s/%s" %("single", i)):
            os.remove("output/%s/%s" %("single" , i))

    m = 0

    if not args.f:
        print("Please Enter the File to Be Indexed")

    elif args.f:
        singleword.main(args.f,m,outz)

    print("\n")




if __name__ == "__main__":
    """
    Runs only if run as a script.
    """
    main()