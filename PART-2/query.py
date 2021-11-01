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
import json
import pandas as pd

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
    queryUpdated = qd.singleindexQuery(queries)
    pprint(queryUpdated)

    f = open("../PART-1/Output/final.json",)
    f2 = open("../PART-1/Output/lexicon.json",)
    f3 = open("../PART-1/Output/documentlist.json",)

    invertedindex = json.load(f)
    lexicon = json.load(f2)
    doclist = json.load(f3)
    method = 'lm'
    df = pd.DataFrame(columns = ['queryid', '0', 'docid', 'rank', 'score', 'method'])
    numq = 0
    for queryid, querytermlist in queryUpdated.items():
        dict1 = {}
        for queryterm in querytermlist:
            for docid, tf in invertedindex[queryterm].items():
                if method == 'cos':
                    sim = tf*(len(doclist)/lexicon[queryterm])*(len(doclist)/lexicon[queryterm])
                elif method == 'bm':
                    sim = 2.2*tf*((len(doclist) - lexicon[queryterm])/lexicon[queryterm])/(tf + 1.2*(0.25 + 0.75*1))
                elif method == 'lm':
                    sim = (invertedindex[queryterm][docid] + 0.2*tf/len(doclist))/(220 + 0.2)
                if docid in dict1:
                    dict1[docid] += sim
                else:
                    dict1[docid] = sim

        dict1 = sorted(dict1.items(), key=lambda x: x[1], reverse=True)

        rank = 0
        for docid, score in dict1:
            rank += 1
            print(str(queryid) + ' 0 ' + str(doclist[docid]) + ' ' + str(rank) + ' ' + str(score) + ' ' + method)        
            if rank == 100:
                break
        numq += 1
        if numq == 5:
            exit()
        





if __name__ == "__main__":
    """
    Runs only if run as a script
    """
    main()
