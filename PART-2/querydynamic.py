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

def checkRelevancy(listt):
    if len(listt) == 1:
        return True
    else:
        for i in listt[0]:
            for j in listt[1]:
                if (i-j)*(i-j) < 25:
                    return True
    return False

def parse_arguments():
    """
    Parsing the Arguments
    """
    parser = argparse.ArgumentParser(description = "Perform Quering")
    parser.add_argument('i', help ='indexPath')
    parser.add_argument('q', help = 'queryPath')
    parser.add_argument('r', help = 'resultsPath')
    args= parser.parse_args()
    print(args.i)
    return args.i,args.q,args.r

def open_invertedindex(fpath,index):
    """
    Opening all the indexes
    """
    #Opening the Inverted Index
    f = open("%s/%s/final.json" %(fpath,index))
    return json.load(f)

def open_lexicon(fpath,index):
    #Opening the Lexicon
    f2 = open("%s/%s/lexicon.json" %(fpath,index))

    return json.load(f2)

def open_documentlist(fpath):
    f3 = open("%s/documentlist.json" %fpath)
    return json.load(f3)


def main():

    indexpath,querypath,resultspath = parse_arguments()
    print(indexpath)

    isExist = os.path.exists(resultspath)
    if not isExist:
        os.makedirs(resultsPath)

    
    try:
        os.remove(resultspath)


    except OSError:
        pass

    resultspath = resultspath +"/results_dynamic.txt"

    with open(resultspath, 'a') as results_file:
        results_file.write('')

    print("waiting..")

    #############################
    # 		SCRIPT STARTS       #
    #############################

    # load document list
    doclist = open_documentlist(indexpath)
    maindict = {}

    # Load all indexes
    invertedindex_phrase = open_invertedindex(indexpath,"phrase")
    lexicon_phrase = open_lexicon(indexpath,"phrase")

    print("waiting..")
    avglen  = averagedocl(doclist)   

    queryUpdated_phrase = indexType(querypath,"phrase")
    qf_phrase = queryfreq(queryUpdated_phrase) 


    # Load all query indices
    

    #pass the path later

    maindict = {}
    rank = 0
    print("starting..")
    # 
    for queryid in queryUpdated_phrase:
        maindict = {}
        dupdict = {}
        queryUpdated_phrase = indexType(querypath,"phrase")
        querytermlist = queryUpdated_phrase[queryid]
        for queryterm in querytermlist:
            if queryterm in invertedindex_phrase:
                for docid,tf in invertedindex_phrase[queryterm].items():
                    # Finding BM25 
                    value = BM25(lexicon_phrase[queryterm],tf,qf_phrase[queryid][queryterm],0,len(doclist),doclist[docid][1],avglen)

            
                    # Storing the score
                    if docid in dupdict:
                        dupdict[docid] += value

                    else:
                        dupdict[docid] = value

        dupdict = sorted(dupdict.items(), key=lambda x: x[1], reverse=True)
        maindict.update(dupdict)


        print("Loading.")
        dupdict={}

        invertedindex_pos = open_invertedindex(indexpath,"pos")
        lexicon_pos = open_lexicon(indexpath,"pos")

        invertedindex_single = open_invertedindex(indexpath,"single")
        lexicon_single = open_lexicon(indexpath,"single")

        queryUpdated_pos = indexType(querypath,"pos")
        querytermlist_pos = queryUpdated_pos[queryid]

        queryUpdated_single = indexType(querypath,"single")
        querytermlist_single = queryUpdated_single[queryid]

        qf_pos = queryfreq(queryUpdated_pos) 
        qf_single = queryfreq(queryUpdated_single) 

        qf_pos = queryfreq(queryUpdated_pos)
        qf_single = queryfreq(queryUpdated_single)    

        li = {}
        relevant = []
        for queryterm in querytermlist_pos:
            if queryterm in invertedindex_pos:
                for docid,position in invertedindex_pos[queryterm][1].items():
                    if docid not in li:
                        li[docid]= [position]
                    else:
                        li[docid].append(position)
        
        print("Loading..")

        for docid in li.keys():
            if checkRelevancy(li[docid]):
                relevant.append(docid)
            if queryterm in invertedindex_single:
                for docid,tf in invertedindex_single[queryterm].items():
                        if docid not in relevant:
                            continue
                        # Finding BM25 
                            value = BM25(lexicon_single[queryterm],tf,qf_single[queryid][queryterm],0,len(doclist),doclist[docid][1],avglen)
                        # Storing the score
                        if docid in dupdict:
                            dupdict[docid] += value

                        else:
                            dupdict[docid] = value        
        
        li = {}
        
        dupdict = sorted(dupdict.items(), key=lambda x: x[1], reverse=True)
        maindict.update(dupdict)
        dupdict = {}
        for queryterm in querytermlist_single:
            if queryterm in invertedindex_single:
                for docid,tf in invertedindex_single[queryterm].items():
                        # Finding BM25 
                        value = BM25(lexicon_single[queryterm],tf,qf_single[queryid][queryterm],0,len(doclist),doclist[docid][1],avglen)
                        # Storing the score
                        if docid in dupdict:
                            dupdict[docid] += value

                        else:
                            dupdict[docid] = value   

        dupdict = sorted(dupdict.items(), key=lambda x: x[1], reverse=True)
        maindict.update(dupdict)
        dupdict = {}   

        invertedindex_stem = open_invertedindex(indexpath,"stem")
        lexicon_stem = open_lexicon(indexpath,"stem")

        queryUpdated_stem = indexType(querypath,"stem")
        querytermlist_stem = queryUpdated_stem[queryid]
        qf_stem = queryfreq(queryUpdated_stem) 




        for queryterm in querytermlist_stem:
            if queryterm in invertedindex_stem:
                for docid,tf in invertedindex_stem[queryterm].items():

                        # Finding BM25 
                        value = BM25(lexicon_stem[queryterm],tf,qf_stem[queryid][queryterm],0,len(doclist),doclist[docid][1],avglen)
                        # Storing the score
                        if docid in dupdict:
                            dupdict[docid] += value

                        else:
                            dupdict[docid] = value   

        dupdict = sorted(dupdict.items(), key=lambda x: x[1], reverse=True)
        
        maindict.update(dupdict)
        dupdict = {}          


        s = ""


        for docid, score in maindict.items():
            rank += 1
            s += str(queryid) + ' 0 ' + str(doclist[docid][0]) + ' ' + str(rank) + ' ' + str(score) + ' ' + "bm25" + "\n"      
            if rank == 100:
                break
        
        with open(resultspath, "a") as text_file:
            text_file.write(s)        
        rank = 0
        print("Loading...")




if __name__ == '__main__':
    main()







