import nltk 
from nltk.tokenize import word_tokenize 
from nltk.corpus import stopwords 
from nltk.stem import WordNetLemmatizer
from nltk.stem import PorterStemmer
from collections import OrderedDict
import json
import string
import re

with open('data') as f:
	data = json.load(f, object_pairs_hook=OrderedDict)



inverted_index = {}

for doc in data:

	content = data[doc]['content']
	doc_id = data[doc]['id']

	#Normalization
	content = re.sub(r"[\[][0-9-]*[\]]", "", content)
	content = content.replace("\n", " ").lower()
	for ch in string.punctuation:
		content = content.replace(ch, " ") 
	tokens = word_tokenize(content) 

	#Remove Stopwords
	tokens = [word for word in tokens if not word in stopwords.words()] 

	# Lemmatization
	lemmatizer=WordNetLemmatizer()
	tokens = [lemmatizer.lemmatize(word) for word in tokens]

	#Stemming
	STEMMER = PorterStemmer()
	tokens = [STEMMER.stem(word) for word in tokens]



	for word in set(tokens):
		if word in inverted_index.keys(): 
			inverted_index[word].append(doc_id)
		else:
			inverted_index[word] = [doc_id]

inverted_index = OrderedDict(sorted(inverted_index.items()))
with open('inverted_index_stem', 'w') as f:
    json.dump(inverted_index, f, indent=4)

# lis = []
# for token in inverted_index:
# 	lis.append(len(inverted_index[token]))
# lis.sort()
# print(lis)
