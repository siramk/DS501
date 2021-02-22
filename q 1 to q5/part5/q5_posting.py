import nltk 
from nltk.tokenize import word_tokenize 
from nltk.corpus import stopwords 
from nltk.stem import WordNetLemmatizer
from nltk.stem import PorterStemmer
import json
import string
import re


def Sort(sub_li): 
    return(sorted(sub_li, key = lambda x: x[0]))

def process(content):
	#Normalization
	content = re.sub(r"[\[][0-9-]*[\]]", "", content)
	content = content.replace("\n", " ").lower()
	for ch in string.punctuation:
		content = content.replace(ch, " ") 
	temp = word_tokenize(content) 

	#Remove Stopwords
	# tokens = [word for word in tokens if not word in stopwords.words('english')]
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
		abstract_token = process(abstract)

		tokens = set(title_token + abstract_token)
		for word in tokens:
			li = [pmid]
			if word in title_token:
				li.append(0)
			if word in abstract_token:
				li.append(1)
			if word in index:
				index[word].append(li)
			else:
				index[word] = [li]
		print(i)

for token in index:
	index[token] = Sort(index[token])
with open('index_posting', 'w') as f:
    json.dump(index, f, indent=1)