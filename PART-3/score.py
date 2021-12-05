from math import log

k1 = 1.2
k2 = 100
b = 0.75
R = 0.0


def BM25(n, f, qf, r, N, dl, avdl):
    """
    Compute BM25 score
    n = no of documents with query
    f =	frequency
    qf = query frequency
    r = 0
    N = no of documents
    dl = document length
    avdl = average document length
    """
    K = Kfactor(dl, avdl)
    first = log( ( (r + 0.5) / (R - r + 0.5) ) / ( (n - r + 0.5) / (N - n - R + r + 0.5)) )
    second = ((k1 + 1) * f) / (K + f)
    third = ((k2+1) * qf) / (k2 + qf)
    return first * second * third


def Kfactor(dl, avdl):
    return k1 * ((1-b) + b * (float(dl)/float(avdl)))


def d(tf,lendoc,df):
    """
    dot product
    have to divide later
    """
    return (tf)*(1+log(lendoc/df))

def w(tf,lendoc,df):
    """
    dot product
    have to divide later
    """
    return (tf)*(1+log(lendoc/df))

def querytf(termlist):
    """
    Query term frequencies
    """
    terms = {}
    for term in termlist:
        if term in terms:
            terms[term] += 1
        else:
            terms[term] = 1
    return terms

def averagedocl(doclist):
    """
    Average document length
    """

    average = 0
    for docno in doclist.values():
        average += docno[1]
    
    # Average Length
    return(average)/(len(doclist))



def queryfreq(queryUpdated): 
    """
    Calculate the query frequency
    """
    qf = {}
    for queryid,querytermlist in queryUpdated.items():
        qf[queryid] = querytf(querytermlist)
    return qf

def LM(df,tf,length,avdl):
    """
    Language model dirichilet smoothing
    """
    mu = 1000
    return (df + mu*tf/length/(avdl + mu))
