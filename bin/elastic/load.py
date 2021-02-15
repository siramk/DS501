import json
import os
from elasticsearch import Elasticsearch

SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))
DATA_DUMP_DIR = os.path.join(SCRIPT_DIR, 'dump', 'data')
INDEX_DIR = os.path.join(SCRIPT_DIR, 'dump', 'index')


class ES:
    @staticmethod
    def connect():
        return Elasticsearch("http://elasticsearch:9200/")

    @staticmethod
    def format_index_name(filename):
        index_name = filename[:-5]
        return index_name


    @staticmethod
    def create_index(es_client, filename):
        index_name = ES.format_index_name(filename)
        
        if es_client.indices.exists(index_name):
            return
        filename = os.path.join(INDEX_DIR, filename)
        with open(filename, "r") as f:
            index_doc = json.load(f)
        es_client.indices.create(index_name, body=index_doc)

    @staticmethod
    def index_document(es_client, filename, docs):
        index_name = ES.format_index_name(filename)
        count = 0
        
        for doc in docs:
            es_client.index(index=index_name, body=docs[doc], id=count)
            count += 1
            
    @staticmethod
    def push():
        es = ES.connect()

        filepath = DATA_DUMP_DIR
        for filename in os.listdir(filepath):
            print(filename)
            ES.create_index(es, filename)
            with open(os.path.join(filepath, filename), "r") as fp:
                docs = json.load(fp)
            ES.index_document(es, filename, docs)


if __name__ == "__main__":
    ES.push()
