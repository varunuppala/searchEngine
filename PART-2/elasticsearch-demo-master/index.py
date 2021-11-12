# built-in modules
import os
import re
import json
import codecs
from time import time
from tqdm import tqdm

# installed modules
from elasticsearch import Elasticsearch

# project modules
from config import *


def parse_raw_data(raw_data):
    '''Parse raw data into a collection of documents

    Args:
        raw_data (basestring): string containing documents

    Returns:
        documents (dict): a <document_identifier, cleaned_document_text>
            dictionary
    '''

    documents = {}

    # split documents by looking for end of document
    # and start of new document tags
    raw_documents = re.split(r'</DOC>\s*<DOC>', raw_data)

    for raw_doc in raw_documents:
        # find the document identifier
        doc_id = re.search(r'<DOCNO>\s([\w+-]+)\s</DOCNO>', raw_doc).group(1)

        #remove parent
        raw_doc = re.sub(r'<PARENT>\s([\w+-]+)\s</PARENT>', '', raw_doc)

        # split on text tags, grab what's between them
        # (i.e., the middle split)
        raw_text = re.split(r'</?TEXT>', raw_doc)[1]

        # replace HTML entities
        raw_text = re.sub(r'&blank;', ' ', raw_text)
        raw_text = re.sub(r'&\w+;', '', raw_text)

        # remove all HTML tags
        clean_text = re.sub(r'<.*?>', '', raw_text)

        # remove multiple spaces
        clean_compact_text = re.sub(r'(\r\n| )(\r\n| )*', r'\1', clean_text)

        # add document to collection
        documents[doc_id] = clean_compact_text

    return documents


def index_parsed_data(documents, index_name, es):
    '''Index documents in the collection, one by one.

    Args:
        documents (dict): a <document_identifier, cleaned_document_text>
            dictionary
        index_name (basestring): name of the index to add data to
        es: Elasticserach connection instance
    '''

    for doc_id, doc_content in tqdm(documents.items(), total=len(documents)):
        # the name 'content' for the content field and the doc_type are
        # specified in the mapping
        es.create(
            index=index_name, id=doc_id,
            body={'content': doc_content}
        )


def bulk_index_parsed_data(
    documents, index_name, es, bulk_max_ops_cnt=600):
    '''Index documents in the collection in bulk.

    Args:
        documents (dict): a <document_identifier, cleaned_document_text>
            dictionary
        index_name (basestring): name of the index to add data to
        es: Elasticsearch instance
        bulk_max_ops_cnt (int): maximum number of operations for bulk action
    '''

    # initialize an operations counter and an operations collector
    opts = []

    for doc_id, doc_content in tqdm(documents.items(), total=len(documents)):
        # append appropriate operations
        opts.append({'create':
            { '_index': index_name, '_id' : doc_id}})
        opts.append({'content': doc_content})

        if len(opts) >= 2*bulk_max_ops_cnt:
            # do bulk operations
            es.bulk(body=opts)

            # empty list and reset operations count
            del opts[:]

    if len(opts) > 0:
        es.bulk(body=opts)


def create_index(index_name, index_settings, es):
    '''Create an index in the cluster

    Args:
        index_name (basestring): name of the index to add data to
        index_settings (dictionary): settings for the index that
            follow the Elasticsearch specs
        es: Elasticsearch connection instance
    '''

    # delete the previous index if it exists
    if es.indices.exists(index=index_name):
        es.indices.delete(index=index_name)

    # create new index
    es.indices.create(index=index_name, body=index_settings)


def main():
    '''Script main method'''

    # load the settings
    with open(INDEX_SETTINGS_FP) as f:
        index_settings = json.load(f)

    # we time the operations
    start_time = time()

    # get all documents
    documents = {}
    for fn in os.listdir(DATA_DIR):
        fp = os.path.join(DATA_DIR, fn)
        with open(fp) as f:
            documents.update(parse_raw_data(f.read()))

    end_time = time()
    print('pre-processing:   {:.3f} s'.format(end_time - start_time))

    # connecting to elasticsearch
    es = Elasticsearch([ 'http://{}:{}'.format(ES_HOST, ES_PORT) ])

    # we time the operations
    start_time = time()

    # create the index
    create_index(INDEX_NAME, index_settings, es)

    # index data one by one
    index_parsed_data(documents, INDEX_NAME, es)

    end_time = time()
    print('one-by-one index: {:.3f} s'.format(end_time - start_time))

    # we time the operations
    start_time = time()

    # delete and recreate the index
    create_index(INDEX_NAME, index_settings, es)
    # index data in bulk
    bulk_index_parsed_data(
        documents, INDEX_NAME, es, BULK_MAX_OPS_CNT)

    end_time = time()
    print('bulk index: {:.3f} s'.format(end_time - start_time))


if __name__ == '__main__':
    main()
