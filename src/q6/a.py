import json
import os
from elasticsearch import Elasticsearch
INDEX_NAME = "netflix"


def scroll(pager, pageno):
    scroll_id = pager['_scroll_id']
    hits = pager['hits']['hits']
    scroll_size = len(hits)
    curr_page = 2
    while (scroll_size > 0 and curr_page <= pageno):
        pager = es.scroll(scroll_id=scroll_id, scroll='1m')
        scroll_id = pager['_scroll_id']
        scroll_size = len(pager['hits']['hits'])
        hits = pager['hits']['hits']
        curr_page += 1
    return hits


def autocomplete_adults(search_query):
    search_query = "/.*" + search_query.strip() + ".*/"
    query = {
        "query": {
            "query_string": {
                "query": search_query
            }
        }
    }
    pager = es.search(index=INDEX_NAME, body=tv_body,
                      scroll='1m', size=pagesize)
    hits = scroll(pager, pageno)
    return hits


def autocomplete_kids(search_query):
    search_query = "/.*" + search_query.strip() + ".*/"
    query = {
        "query": {
            "bool": {
                "must_not": [
                    {"term": {"rating": "PG"}},
                    {"term": {"rating": "R"}},
                    {"term": {"rating": "NC"}}
                ],
                "must": {
                    "query_string": {
                        "query": search_query
                    }
                }
            }
        }
    }
    pager = es.search(index=INDEX_NAME, body=tv_body,
                      scroll='1m', size=pagesize)
    hits = scroll(pager, pageno)
    return hits
