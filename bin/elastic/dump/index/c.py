import json
import os
from elasticsearch import Elasticsearch

INDEX_NAME = "netflix"



def scroll(pager):
    scroll_id = pager['_scroll_id']
    hits = pager['hits']['hits']
    scroll_size = len(hits)
    while (scroll_size > 0):
        pager = es.scroll(scroll_id=scroll_id, scroll='1m')
        scroll_id = pager['_scroll_id']
        scroll_size = len(pager['hits']['hits'])
        hits += pager['hits']['hits']
        curr_page += 1
    return hits


def prefix_match(string):
    string = "/" + string.strip() + ".*/"
    query = {
        "query": {
            "query_string": {
                "query": string
            }
        }
    }
    pager = es.search(index=INDEX_NAME, body=tv_body, scroll='1m', size=1000)
    hits = scroll(pager)
    return hits


def exact_match_endpoint(field, value):
    field = field.strip()
    value = value.strip()
    query = {
        "query": {
            "match_phrase": {
                field: {
                    "query": value
                }
            }
        }
    }
    pager = es.search(index=INDEX_NAME, body=tv_body, scroll='1m', size=1000)
    hits = scroll(pager)
    return hits

# TODO: gener match endpoint

    
