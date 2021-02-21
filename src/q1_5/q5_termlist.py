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
	content = re.sub(r"[\[].*[\]]", "", content)
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

	return tokens


index = {}
i = 0
with open('data.txt') as f:
	for line in f:
		i += 1
		article = eval(line)
		title = article['title']
		abstract = article['abstract']
		pmid = article['pmid']

		title_token = process(title)

		for word in set(title_token):
			temp = word + '.title'
			if temp in index:
				index[temp].append(pmid)
			else:
				index[temp] = [pmid]

		abstract_token = process(abstract)

		for word in set(abstract_token):
			temp = word + '.abstract'
			if temp in index:
				index[temp].append(pmid)
			else:
				index[temp] = [pmid]
		print(i)
with open('index_termlist', 'w') as f:
    json.dump(index, f, indent=4)