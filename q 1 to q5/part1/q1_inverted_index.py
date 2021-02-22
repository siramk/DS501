import nltk 
from nltk.tokenize import word_tokenize 
from nltk.corpus import stopwords 
from nltk.stem import WordNetLemmatizer
from nltk.stem import PorterStemmer
from collections import OrderedDict
import json
import string
import re

with open('crawled_data') as f:
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

with open('inverted_index', 'w') as f:
    json.dump(inverted_index, f, indent=4)




#Since inverted index of the crawled data contains many of the word once.
#So, there are many words which are least used.
#So, instead of printing, we appended it into a file names as most_used_least_used.
lis = []
for token in inverted_index:
	lis.append(len(inverted_index[token]))
lis.sort(reverse=True)
max_list = lis[:3]
min_list = lis[-3:]
dict = {
	'most_used' : [],
	'least_used': []
}
for token in inverted_index:
	if len(inverted_index[token]) in max_list:
		dict['most_used'].append({token: inverted_index[token]})
	if len(inverted_index[token]) in min_list:
		dict['least_used'].append({token: inverted_index[token]})
with open('most_used_least_used', 'w') as f:
    json.dump(dict, f, indent=4)