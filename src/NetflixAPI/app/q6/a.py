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


def autocomplete_adults(search_query):
    search_query = search_query.strip()

    query = {
        "size":5,
        "sort": [{"_score": "desc"}],
        "query": {
            
            "multi_match": {
                "query": "order",
                "type": "phrase_prefix",
                "fields":     ["cast", "title", "country", "date_added", "description", "listed_in", "duration"]
            }
        }
    }

    pager = es.search(index=INDEX_NAME, body=query)
    hits = pager['hits']['hits']

    return jsonify(hits)



def autocomplete_kids(search_query):
    search_query = search_query.strip()
    query = {
        "size":5,
        "sort": [{"_score": "desc"}],
        "query": {
            "bool": {
                "must_not": [
                    {"prefix": {"rating": "PG"}},
                    {"prefix": {"rating": "R"}},
                    {"prefix": {"rating": "NC"}},
                    {"prefix": {"rating": "TV-R"}},
                    {"prefix": {"rating": "TV-PG"}},
                    {"prefix": {"rating": "TV-NC"}}
                ],
                "must": {
                    "multi_match": {
                        "query":      search_query,
                        "type":       "phrase_prefix",
                        "fields":    ["cast", "title", "country", "date_added", "description", "listed_in", "duration"]
                    }
                }
            }
        }
    }

    pager = es.search(index=INDEX_NAME, body=query)
    hits = pager['hits']['hits']

    return jsonify(hits)
