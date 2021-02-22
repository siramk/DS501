import nltk 
from nltk.tokenize import word_tokenize 
from nltk.corpus import stopwords 
from nltk.stem import WordNetLemmatizer
from nltk.stem import PorterStemmer
from collections import OrderedDict
from collections import Counter
import json
import string
import re
import math
import os
import sys
path = os.getcwd() 
parent = os.path.abspath(os.path.join(path, os.pardir))
sys.path.insert(1, parent)
from part2.q2 import Q2


def preprocess(data):
	#Normalization
	data = re.sub(r"[\[][0-9-]*[\]]", "", data)
	data = data.replace("\n", " ").lower()
	for ch in string.punctuation:
		data = data.replace(ch, " ")
	tokens = word_tokenize(data) 

	#Remove Stopwords
	tokens = [word for word in tokens if not word in stopwords.words('english')] 

	# Lemmatization
	lemmatizer=WordNetLemmatizer()
	tokens = [lemmatizer.lemmatize(word) for word in tokens]

	#Stemming
	STEMMER = PorterStemmer()
	tokens = [STEMMER.stem(word) for word in tokens]


	return tokens


#Return the idf calculated for each token
def inverse_doc_frequency(documents):
	df = {}
	for i in range(len(documents)):
		tokens = preprocess(documents[i])
		for token in set(tokens):
			if token in df:
				df[token] = df[token] + 1
			else:
				df[token] = 1
	idf = {}
	N = len(documents)
	for token in df:
		idf[token] = math.log(N/df[token])
	return idf



with open('../part1/crawled_data', 'r') as f:
	data = json.load(f, object_pairs_hook=OrderedDict)

documents = []
for doc in data:
	documents.append(data[doc]['content'])

idf = inverse_doc_frequency(documents)

#Calculating the tf_idf 
tf_idf = {}
for doc in data:
	doc_id = data[doc]['id']
	content = data[doc]['content']

	tokens = preprocess(content)
	counter = Counter(tokens)

	max_freq = counter.most_common(1)[0][1]
	for token in set(tokens):
		tf = 0.5 + (0.5*counter[token]/max_freq)
		tf_idf[doc_id, token] = tf*idf[token]


with open('../part1/inverted_index', 'r') as f:
	postings = json.load(f)

queries = ['IIT and Computer', 'IIT and mhrd', 'Bhilai and Raipur and bilaspur']
for query in queries:
	terms = Q2.process_query(query)
	result = Q2.multi_intersect(terms, postings)

	#Scoring the document retrived from Q2
	rank_dict = {}
	for doc_id in result:
		num = 0
		den = 0
		for term in terms:
			num += tf_idf[doc_id, term]
			den += pow(tf_idf[doc_id, term], 2)
		den = math.sqrt(den)
		rank_dict[doc_id] = num/den


	final_res = [key for key, value in sorted(rank_dict.items(), reverse= True, key=lambda item: item[1])]

	print(final_res)
