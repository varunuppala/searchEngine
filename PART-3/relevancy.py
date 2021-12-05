import querydoc as qd
import warnings
import json
from math import sqrt
from score import *
from querydoc import *
import itertools
import os

def getRelevantDocuments(queryUpdated,invertedindex,lexicon,doclist,method,resultsPath,initial):
    try:
        os.remove(resultsPath)
    except OSError:
        pass

    with open(resultsPath, 'a') as results_file:
        results_file.write('')


    # Average Doc Len
    avglen  = averagedocl(doclist)

    # Query frequency
    qf = queryfreq(queryUpdated)

    relevant = {}
    # Testing for few queries

    for queryid, querytermlist in queryUpdated.items():
        maindict = {}

        for queryterm in querytermlist:
            if queryterm in invertedindex:

                for docid,tf in invertedindex[queryterm].items():
                    # Finding BM25 
                    value = BM25(lexicon[queryterm],tf,qf[queryid][queryterm],0,len(doclist),doclist[docid][1],avglen)

                    # Storing the score
                    if docid in maindict:
                            maindict[docid] += value

                    else:
                            maindict[docid] = value

        # Sorting for the ranks
        maindict = dict(sorted(maindict.items(), key=lambda x: x[1], reverse=True))
        rank = 0
        s = ""
        for docid, score in maindict.items():
            rank += 1
            s += str(queryid) + ' 0 ' + str(doclist[docid][0]) + ' ' + str(rank) + ' ' + str(score) + ' ' + method + "\n" 
            if queryid not in relevant:
                relevant[queryid] = maindict
            if rank == 100:
                break
        with open(resultsPath, "a") as text_file:
            text_file.write(s)
        print("Loading...")
    
    if initial == 1:
        return relevant

def selectMdocs(docs,m):
    for queryid,doclist in docs.items():
        new = {}
        new = dict(itertools.islice(doclist.items(), m))
        docs[queryid] = new
    return docs


def findnewQuery(query,docs,index,m,n):
    """
    to return updated query
    n = docs
    m = terms
    """
    # Select top n documents
    docs = selectMdocs(docs,m)
    print("Starting expansion process")


    for qid,doc in docs.items():
        # list of documents
        l = list(doc.keys())

        count = {} # has number of documents each word appears
        for k in l:
            for word in index[k]:
                if word not in count:
                    count[word] = []
                    count[word].append(k)
                else:
                    if k not in count[word]:
                        count[word].append(k)


        # intialising first document
        d = index[l[0]]
        
        # for loop to append all the document term list
        for i in l[1:]:
            for term,freq in index[i].items():
                if term not in d and term not in query[qid]:
                    d[term] = freq
                elif term in d and term not in query[qid]:
                    d[term] += freq

        # multiplying document frequency for term selection
        for word in d:
            d[word] = d[word] * (len(count[word]))
        # sorting in reverse order
        new_d = dict(sorted(d.items(), key=lambda x: x[1], reverse=True))



        # catching the top n terms
        new_d = dict(itertools.islice(new_d.items(), n))


        # updated terms
        updatedTerms = new_d.keys()

        #appending them to original query
        for upterm in updatedTerms:
            query[qid].append(upterm)
        print("Updating query ...")

    return query




def findReducedQuery(query,perc,lexicon):
    """
    Find the reduced Query using percentage
    1. Finding the first x% query using top tf
    """

    #calculate query frequency
    qf = queryfreq(query)

    #Calculate query frequency
    newquery = queryLenPerc(query,qf,perc,lexicon)

    #return it
    return newquery

def queryLenPerc(query,qf,perc,lexicon):
    """
    Calculate the query according to the percentage
    """
    perc = perc/100
    d = {}

    for i,queryi in qf.items():
        d[i] = len(queryi)

    
    for qid,words in query.items():
        dl= []
        for word in words:
            if word in lexicon:
                dl.append(word)
                query[qid] = dl
   


    for qid,words in query.items():
        query[qid] = sorted(query[qid], key=lambda x: lexicon[x], reverse = True)

       
    for i,terms in query.items():
        j = int(d[i]*perc)
        qf[i] = terms[j:]

    return qf














