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
from math import sqrt
from score import *
from querydoc import *



warnings.filterwarnings('ignore')


def parse_arguments():
    """
    Parsing the Arguments
    """
    parser = argparse.ArgumentParser(description = "Perform Quering")
    parser.add_argument('i', help ='indexPath')
    parser.add_argument('q', help = 'queryPath')
    parser.add_argument('m', help = 'retrievalMode')
    parser.add_argument('t', help = 'indexType')
    parser.add_argument('r', help = 'resultsPath')
    args= parser.parse_args()
    return args.i,args.q,args.m,args.t,args.r

def open_index(fpath,index):
    
    #Opening the Inverted Index
    f = open("%s/%s/final.json" %(fpath,index))


    #Opening the Lexicon
    f2 = open("%s/%s/lexicon.json" %(fpath,index))


    #Opening the Document List
    f3 = open("%s/documentlist.json" %fpath)

    return json.load(f),json.load(f2),json.load(f3)

def main():
    """
    main function for the script
    Goals:
    1.Argument Parsing done
    2.Assigns calls as specified by the user
    3.Build indexes for the query document
    4.Load the indexes from the previous step(Part-1)
    5.Compare using technqiues
    6.Report them
    """
    # tracking time
    start_time = time.time()

    indexPath,queryPath,method,indextype,resultsPath = parse_arguments()
    

    isExist = os.path.exists(resultsPath)
    if not isExist:
        os.makedirs(resultsPath)


    resultsPath = resultsPath+"/results.txt"

    # pass the queryPath to this in the later stage
    queryUpdated = indexType(queryPath,indextype)


    # pass the index path
    invertedindex,lexicon,doclist= open_index(indexPath,indextype)


    # Average Doc Len
    avglen  = averagedocl(doclist)

    # Query frequency
    qf = queryfreq(queryUpdated)

    try:
        os.remove(resultsPath)
    except OSError:
        pass

    with open(resultsPath, 'a') as results_file:
        results_file.write('')


    # Testing for few queries
    numq = 0

    d1,d2 = 0,0 

    for queryid, querytermlist in queryUpdated.items():
        maindict = {}

        for queryterm in querytermlist:
            if queryterm in invertedindex:

                for docid,tf in invertedindex[queryterm].items():

                    #Finding Cosine Product
                    if method == 'cos':
                        value = d(tf,len(doclist),lexicon[queryterm]) * w(qf[queryid][queryterm],len(doclist),lexicon[queryterm])

                    # Finding BM25 
                    elif method == 'bm25':
                        #change third one to qtermfreq
                        value = BM25(lexicon[queryterm],tf,qf[queryid][queryterm],0,len(doclist),doclist[docid][1],avglen)
                      
                            
                    # Finding the Dirchilet smoothing 
                    elif method == 'lm':
                        value = LM(invertedindex[queryterm][docid],tf,len(doclist),avglen)


                    # Storing the score
                    if docid in maindict:
                            maindict[docid] += value

                    else:
                            maindict[docid] = value

        # Sorting for the ranks
        maindict = sorted(maindict.items(), key=lambda x: x[1], reverse=True)

        rank = 0
        s = ""
        # Printing the output for now
        for docid, score in maindict:
            rank += 1
            s += str(queryid) + ' 0 ' + str(doclist[docid][0]) + ' ' + str(rank) + ' ' + str(score) + ' ' + method + "\n"      
            if rank == 100:
                break

        with open(resultsPath, "a") as text_file:
            text_file.write(s)
        print("Loading...")

        




if __name__ == "__main__":
    """
    Runs only if run as a script
    """
    main()
