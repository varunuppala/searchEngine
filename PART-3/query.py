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
import json
from math import sqrt
from score import *
from querydoc import *
from relevancy import *



warnings.filterwarnings('ignore')


def parse_arguments():
    """
    Parsing the Arguments
    """
    parser = argparse.ArgumentParser(description = "Perform Quering")
    
    parser.add_argument('-i','--index_path', help ='indexPath',required = True)
    parser.add_argument('-q','--query_path', help = 'queryPath',required = True)
    parser.add_argument('-r','--result_path', help = 'resultsPath',required = True)
    parser.add_argument('-rt','--reform_type',choices=["a", "b", "c"], help="a) Expansion b) Reduction c) Expansion and Reduction",required = True)
    parser.add_argument('-d','--number_documents', help = 'Number of Documents',required = False,type = int)
    parser.add_argument('-tc','--term_count', help = 'Number of Top Terms',required = False,type = int)
    parser.add_argument('-qp','--query_perc', help = 'Percentage of narr',required = False,default = 0,type = int)
    
    args= parser.parse_args()

    return args.index_path,args.query_path,args.result_path,args.reform_type,args.number_documents,args.term_count,args.query_perc

def open_index(fpath,index):
    
    #Opening the Inverted Index
    f = open("%s/%s/final.json" %(fpath,index))

    #Opening the Lexicon
    f2 = open("%s/%s/lexicon.json" %(fpath,index))

    #Opening the Document List
    f3 = open("%s/documentlist.json" %fpath)

    #Opening the Index
    f4 = open("%s/index.json" %fpath)

    return json.load(f),json.load(f2),json.load(f3),json.load(f4)

def main():
    """
    """
    start_time = time.time()
    indexPath,queryPath,resultsPath,typ,m,n,perc = parse_arguments()
    
    # Method and index type
    indextype = "single"
    method = "bm25"

    # Creating results directory
    isExist = os.path.exists(resultsPath)
    if not isExist:
        os.makedirs(resultsPath)

    # original results
    resultsPath0 = resultsPath+"/results.txt"

    # Get all the indexes
    invertedindex,lexicon,doclist,index = open_index(indexPath,indextype)
    

    if typ == "a":

        theta = (time.time() - start_time)
        # Original queries
        queryOriginal = indexType(queryPath,indextype)
        

        #pass 0 for returning and 1 for not return
        reldocs = getRelevantDocuments(queryOriginal,invertedindex,lexicon,doclist,method,resultsPath0+"_a",1)
        
        Original = (time.time() - start_time)

        # Updated query original query,relevant docs,index,docs,terms
        queryUpdated = findnewQuery(queryOriginal,reldocs,index,m,n)
        
        resultsPath1 = resultsPath+"/results_%sX%s.txt" %(m,n)
        #pass 0 for returning and 1 for not return
        getRelevantDocuments(queryUpdated,invertedindex,lexicon,doclist,method,resultsPath1,0)
        Updated = (time.time() - start_time)

    if typ == "b":

        theta = (time.time() - start_time)
        
        # Original queries
        queryOriginal = indexType1(queryPath,indextype)


        #pass 0 for returning and 1 for not return
        reldocs = getRelevantDocuments(queryOriginal,invertedindex,lexicon,doclist,method,resultsPath0+"_b",1)
        
        Original = (time.time() - start_time)

        # Updated query original query,relevant docs,index,docs,terms
        queryUpdated = findReducedQuery(queryOriginal,perc,lexicon)

        #Last results path
        resultsPath1 = resultsPath+"/results_%s.txt" %(perc)
        
        #pass 0 for returning and 1 for not return
        getRelevantDocuments(queryUpdated,invertedindex,lexicon,doclist,method,resultsPath1,0)

        Updated = (time.time() - start_time)

    if typ == "c":

        theta = (time.time() - start_time)

        # Original queries
        queryOriginal = indexType1(queryPath,indextype)
        
        #pass 0 for returning and 1 for not return
        reldocs = getRelevantDocuments(queryOriginal,invertedindex,lexicon,doclist,method,resultsPath0+"_c",1)

        Original = (time.time() - start_time)

        queryUpdated = findReducedQuery(queryOriginal,perc,lexicon)

        queryExpanded = findnewQuery(queryUpdated,reldocs,index,m,n)

        #Last results path
        resultsPath1 = resultsPath+"/results_%sX%s_%s.txt" %(m,n,perc)
        
        #pass 0 for returning and 1 for not return
        getRelevantDocuments(queryUpdated,invertedindex,lexicon,doclist,method,resultsPath1,0)

        Updated = (time.time() - start_time)

    
    updated_time = Updated - Original
    print("--- %s seconds ---Time Taken To Find Relevant Documents using Original Query---" % (Original - theta))
    print("\n")
    print("--- %s seconds ---Time Taken To Find Relevant Documents using Updated Query---" % (Updated - Original))
    print("Above are the results for %s" %resultsPath1)


        

if __name__ == "__main__":
    """
    Runs only if run as a script
    """
    print("\n")
    main()
    print("\n")
