import argparse
import re
import singleword
import positional
import stem
import phrase
import os


def main():
    """
    Sole heart of the program.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("f",help="Please enter the filename to be indexed")
    parser.add_argument("t", help = "Please specify the type of index")
    parser.add_argument("m",help = "please specify the memory",type = int)
    parser.add_argument("o", help = "Please specify the output directory")
    args = parser.parse_args()
    outz = args.o +"/" +args.t
    isExist = os.path.exists(outz)

    if not isExist:
        os.makedirs(outz)

    files = os.listdir(outz)

    for i in files:
        if os.path.exists("output/%s/%s" %(args.t , i)):
            os.remove("output/%s/%s" %(args.t , i))




    if args.m == "No":
        m = 0
    else:
        m = args.m


    
    if not args.f:
        print("Please Enter the File to Be Indexed")

    elif args.f:
        if args.t == "single":
            singleword.main(args.f,m,outz)
        elif args.t == "pos":
            positional.main(args.f,m,outz)
        elif args.t == "stem":
            stem.main(args.f,m,outz)
        elif args.t == "phrase":
            phrase.main(args.f,m,outz)
        else:
            print("Wrong Command")

    print("\n")




if __name__ == "__main__":
    """
    Runs only if run as a script.
    """
    main()
