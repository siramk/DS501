from flask import jsonify
from elasticsearch import Elasticsearch

INDEX_NAME = "netflix"


es = Elasticsearch("http://elasticsearch:9200/")


def scroll(pager, limit=10**5):
    scroll_id = pager['_scroll_id']
    hits = pager['hits']['hits']
    scroll_size = len(hits)
    while (scroll_size > 0 and len(hits) < limit):
        pager = es.scroll(scroll_id=scroll_id, scroll='1m')
        scroll_id = pager['_scroll_id']
        scroll_size = len(pager['hits']['hits'])
        hits += pager['hits']['hits']
    return hits


def prefix_match(search_query):
    search_query = "/" + search_query.strip() + ".*/"
    query = {
        "query": {
            "query_string": {
                "query": search_query,
                "default_field": "description"
            }
        }
    }
    pager = es.search(index=INDEX_NAME, body=query, scroll='1m', size=1000)
    hits = scroll(pager)
    return jsonify(hits)


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
    pager = es.search(index=INDEX_NAME, body=query, scroll='1m', size=1000)
    hits = scroll(pager)
    return jsonify(hits)

# TODO: gener match endpoint


def genre_match_endpoint(boolean_query):
    boolean_query = boolean_query.replace("and", "AND")
    boolean_query = boolean_query.replace("or", "OR")
    boolean_query = boolean_query.replace("not", "NOT")
    query = {
        "query": {
            "query_string": {
                "query": boolean_query,
                "default_field": "listed_in"
            }
        }
    }
    pager = es.search(index=INDEX_NAME, body=query, scroll='1m', size=1000)
    hits = scroll(pager)
    return jsonify(hits)
