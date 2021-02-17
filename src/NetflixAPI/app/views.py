
import os
import json
from flask import Flask

from q6.a import scroll, autocomplete_adults, autocomplete_kids
from q6.b import scroll_pagewise, pagination_movie, pagination_tv
from q6.c import prefix_match, exact_match_endpoint, genre_match_endpoint




app = Flask(__name__) 
app.add_url_rule('/autocomplete_adults/<string:search_query>', 'autocomplete_adults', autocomplete_adults)
app.add_url_rule('/autocomplete_kids/<string:search_query>', 'autocomplete_kids', autocomplete_kids)
app.add_url_rule('/pagination_movie/<int:pagesize>/<int:pageno>', 'pagination_movie', pagination_movie)
app.add_url_rule('/pagination_tv/<int:pagesize>/<int:pageno>', 'pagination_tv', pagination_tv)
app.add_url_rule('/exact_match_endpoint/<string:field>/<string:value>', 'exact_match_endpoint', exact_match_endpoint)
app.add_url_rule('/prefix_match/<string:search_query>', 'prefix_match', prefix_match)
app.add_url_rule('/genre_match_endpoint/<string:boolean_query>', 'genre_match_endpoint', genre_match_endpoint)


   
if __name__ == '__main__': 

    app.run(host="0.0.0.0", port=5000, debug=True)
