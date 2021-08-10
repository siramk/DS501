# Netflix Search API
Command to run NetflixSearchAPI locally

`cd NetflixSearchAPI`

`./docker/run.sh console`

After doing above steps, localhost:5000/ and use the endpoints

Dependencies for NetflixSearchAPI
1. docker
2. docker-compose

# API details

<!-- ### DOMIAN​ : “​ https://netflix-ds501.herokuapp.com​ ” -->

## REST API ENDPOINTS
**NOTE**: All endpoints support only GET requests.

**Autocomplete Adults**

'/autocomplete_adults/<string:search_query>'
Example: ​ /autocomplete_adults/order

**Autocomplete Kids**

'/autocomplete_kids/<string:search_query>'

Example: ​ /autocomplete_kids/order

**Pagination Movie**

'/pagination_movie/<int:pagesize>/<int:pageno>'

Example: ​ /pagination_movie/5/1

**Pagination TV series**

'/pagination_tv/<int:pagesize>/<int:pageno>'

Example:​ /pagination_tv/5/1

**Exact Match**

'/exact_match/<string:field>/<string:value>'

Example: ​ /exact_match/director/Ross Venokur

**PREFIX MATCH**

'/prefix_match/<string:search_query>'

Example: ​ /prefix_match/after

**Genre Match Endpoint**

'/genre_match/<string:boolean_query>'

Example: ​ genre_match/dramas AND thrillers


### TOKENIZERS USED
Standard tokenizer

### **QUERY TYPES USED**

**Autocomplete Adults**

Multi_match query with type as “phrase_prefx”

**Autocomplete Kids**

Bool query with Multi_match query with type as “phrase_prefx”

**Pagination Movie**

Term query with sort

**Pagination TV series**

Term query with sort

**Exact Match**

Match_phrase query

**Prefix Match**

Query_string query with default_field as description

**Genre Match Endpoint**

Query_string query with default_filed as listed_in

**MAPPING**
``` {
    "settings": {
        "analysis": {
            "analyzer": {
                "ngram_analyzer": {
                    "type": "custom",
                    "tokenizer": "standard",
                    "filter": [
                        "lowercase",
                        "4_grams"
                    ]
                },
                "lowercase_analyzer": {
                    "type": "custom",
                    "tokenizer": "standard",
                    "filter": [
                        "lowercase"
                    ]
                },
                "keyword_analyzer": {
                    "type": "custom",
                    "tokenizer": "keyword",
                    "filter": [
                        "lowercase"
                    ]
                }
            },
            "filter": {
                "4_grams": {
                    "type": "ngram",
                    "min_gram": 4,
                    "max_gram": 4
                }
            }
        },
        "number_of_shards": 1,
        "number_of_replicas": 0
    },
    "mappings": {
        "properties": {
            "type": {
                "type": "keyword"
            },
            "title": {
                "type": "text",
                "analyzer": "lowercase_analyzer",
                "fields": {
                    "keyword": {
                        "type": "keyword"
                    }
                }
            },
            "director": {
                "type": "text",
                "analyzer": "ngram_analyzer",
                "fields": {
                    "keyword": {
                        "type": "keyword"
                    }
                }
            },
            "cast": {
                "type": "text",
                "analyzer": "lowercase_analyzer",
                "fields": {
                    "keyword": {
                        "type": "keyword"
                    }
                }
            },
            "country": {
                "type": "text",
                "analyzer": "lowercase_analyzer",
                "fields": {
                    "keyword": {
                        "type": "keyword"
                    }
                }
            },
            "date_added": {
                "type": "text",
                "analyzer": "lowercase_analyzer",
                "fields": {
                    "keyword": {
                        "type": "keyword"
                    }
                }
            },
            "release_year": {
                "type": "short",
                "fields": {
                    "keyword": {
                        "type": "keyword"
                    }
                }
            },
            "rating": {
                "type": "keyword",
                "fields": {
                    "keyword": {
                        "type": "keyword"
                    }
                }
            },
            "duration": {
                "type": "text",
                "analyzer": "lowercase_analyzer",
                "fields": {
                    "keyword": {
                        "type": "keyword"
                    }
                }
            },
            "listed_in": {
                "type": "text",
                "analyzer": "lowercase_analyzer",
                "fields": {
                    "keyword": {
                        "type": "keyword"
                    }
                }
            },
            "description": {
                "type": "text",
                "analyzer": "lowercase_analyzer",
                "fields": {
                    "keyword": {
                        "type": "keyword"
                    }
                }
            }
        }
    }
} ```
