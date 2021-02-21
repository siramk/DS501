import nltk 
from nltk.tokenize import word_tokenize 
from nltk.corpus import stopwords 
from nltk.stem import WordNetLemmatizer
from nltk.stem import PorterStemmer
import json
import string
import re


def process(content):
	#Normalization
	content = re.sub(r"[\[][0-9-]*[\]]", "", content)
	content = content.replace("\n", " ").lower()
	for ch in string.punctuation:
		content = content.replace(ch, " ") 
	temp = word_tokenize(content) 

	#Remove Stopwords
	# tokens = [word for word in set(tokens) if not word in stopwords.words('english')]
	stop_words = set(stopwords.words('english'))
	tokens = []
	for w in temp:
	    if w not in stop_words:
	        tokens.append(w)
	# Lemmatization
	lemmatizer=WordNetLemmatizer()
	tokens = [lemmatizer.lemmatize(word) for word in tokens]

	#Stemming
	STEMMER = PorterStemmer()
	tokens = [STEMMER.stem(word) for word in tokens]

	return tokens


index = {}
i = 0
with open('data.txt') as f:
	for line in f:
		i += 1
		article = eval(line)
		title = article['title']
		abstract = article['abstract']
		try:
			pmid = int(article['pmid'])
		except:
			continue

		title_token = process(title)

		for word in set(title_token):
			temp = word + '.0'
			if temp in index:
				index[temp].append(pmid)
			else:
				index[temp] = [pmid]

		abstract_token = process(abstract)

		for word in set(abstract_token):
			temp = word + '.1'
			if temp in index:
				index[temp].append(pmid)
			else:
				index[temp] = [pmid]
		print(i)

for token in index:
	index[token] = sorted(index[token])
with open('index_termlist', 'w') as f:
    json.dump(index, f, indent=1)