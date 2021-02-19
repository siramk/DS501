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


def preprocess(data):
	#Normalization
	data = re.sub(r"[\[].*[\]]", "", data)
	data = data.replace("\n", " ").lower()
	for ch in string.punctuation:                                                                                                     
    	data = data.replace(ch, " ") 
	tokens = word_tokenize(data) 

	#Remove Stopwords
	tokens = [word for word in tokens if not word in stopwords.words()] 

	# Lemmatization
	lemmatizer=WordNetLemmatizer()
	tokens = [lemmatizer.lemmatize(word) for word in tokens]

	#Stemming
	STEMMER = PorterStemmer()
	tokens = [STEMMER.stem(word) for word in tokens]


	return tokens


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



with open('data', 'r') as f:
	data = json.load(f, object_pairs_hook=OrderedDict)

documents = []
for doc in data:
	documents.append(data[doc]['content'])

idf = inverse_doc_frequency(documents)

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


with open('temp','w+') as f:
     f.write(str(tf_idf))