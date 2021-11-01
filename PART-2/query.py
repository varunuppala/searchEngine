"""
To-do Query processing
1. Process the document as we have done in the first part
2. Compare with the index we have
3. Report the relevancy score
"""
import argparse
import os
import time
import querydoc as qd
import warnings
from pprint import pprint

warnings.filterwarnings('ignore')


def parse_arguments():
    """
    Parsing the Arguments
    """
    parser= argparse.ArgumentParser(description = "Perform Quering")
    parser.add_argument('-i', dest ='indexPath')
    parser.add_argument('-q', dest = 'queryPath')
    parser.add_argument('-m', dest = 'retrievalMode')
    parser.add_argument('-t', dest = 'indexType')
    parser.add_argument('-r', dest = 'resultsPath')
    args= parser.parse_args()
    return args.indexPath,args.queryPath,args.retrievalMode,args.indexType,args.resultsPath


def main():
    """
    main function for the script
    Goals:
    1.Argument Parsing done
    2.Assigns calls as specified by the user.(Can be done later)
    3.Build indexes for the query document
    4.Load the indexes from the previous step(Part-1)
    5.Compare using technqiues
    6.Report them
    """
    start_time = time.time()#tracking time
    #indexPath,queryPath,retrievalMode,indexPath,resultsPath = parse_arguments()
    #print(indexPath,queryPath,retrievalMode,indexPath,resultsPath)
    queries = qd.main()# pass the queryPath to this in the later stage
    queryUpdated = qd.phraseindexQuery(queries)
    pprint(queryUpdated)







if __name__ == "__main__":
    """
    Runs only if run as a script
    """
    main()
