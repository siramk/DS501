from flask import jsonify
from elasticsearch import Elasticsearch

INDEX_NAME = "netflix2"

es = Elasticsearch("http://elasticsearch:9200/")

def scroll_pagewise(pager, pageno):
    scroll_id = pager['_scroll_id']
    hits = pager['hits']['hits']
    scroll_size = len(hits)
    curr_page = 2
    while (scroll_size > 0 and curr_page <= pageno):
        pager = es.scroll(scroll_id = scroll_id, scroll = '1m')
        scroll_id = pager['_scroll_id']
        scroll_size = len(pager['hits']['hits'])
        hits = pager['hits']['hits']
        curr_page += 1 
    return hits



def pagination_movie(pagesize, pageno):
    movie_body = {
        "sort" : [ { "release_year" : "desc" }],
        "query": {"term": {"type":  "Movie"}}
        }
    pager = es.search(index=INDEX_NAME, body=movie_body, scroll='1m', size=pagesize)
    hits = scroll_pagewise(pager, pageno)
    return jsonify(hits)

def pagination_tv(pagesize, pageno):
    tv_body = {
        "sort" : [ { "release_year" : "desc" }],
        "query": {"term": {"type":  "TV Show"}}
        }
    pager = es.search(index=INDEX_NAME, body=tv_body, scroll='1m', size=pagesize)
    hits = scroll_pagewise(pager, pageno)
    return jsonify(hits)



