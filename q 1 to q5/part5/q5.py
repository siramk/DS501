import json
import nltk
from nltk.stem import WordNetLemmatizer
from nltk.stem import PorterStemmer
import time

def process_query(query):
	query = query.lower()
	terms = query.split('and')
	terms = [word.strip() for word in terms]

	# Lemmatization
	lemmatizer=WordNetLemmatizer()
	terms = [lemmatizer.lemmatize(word) for word in terms]

	#Stemmization
	STEMMER = PorterStemmer()
	terms = [STEMMER.stem(word) for word in terms]

	return terms

def weightedzone_posting(g, li1, li2 = []):
	score = 0
	if 0 in li1:
		score += g[0]
	if 1 in li1:
		score += g[1]
	if 0 in li2:
		score += g[0]
	if 1 in li2:
		score += g[1]
	return score

def zone_score_posting(terms, index_posting):
	score = {}
	g = [0.7, 0.3]
	if len(terms) == 1:
		if terms[0] not in index_posting:
			return score
		p1 = index_posting[terms[0]]
		i = 0
		while i < len(p1):
			score[p1[i][0]] = weightedzone_posting(g, p1[i])
			i += 1
	else:
		if terms[0] not in index_posting:
			return score
		if terms[1] not in index_posting:
			return score
		p1 = index_posting[terms[0]]
		p2 = index_posting[terms[1]]
		i = 0
		j = 0
		while i < len(p1) and j < len(p2):
			if p1[i][0] == p2[j][0]:
				score[p1[i][0]] = weightedzone_posting(g, p1[i], p2[j])
				i += 1
				j += 1
			elif p1[i][0] < p2[j][0]:
				i += 1
			else:
				j += 1
	return score

def zone_score_dictionary(terms, index_dictionary):
	score = {}
	g = [0.7, 0.3]
	if len(terms) == 1:
		if terms[0] + '.0' in index_dictionary:
			p1 = index_dictionary[terms[0] + '.0']
			for doc in p1:
				if doc in score:
					score[doc] += 0.7
				else:
					score[doc] = 0.7
		if terms[0] + '.1' in index_dictionary:
			p1 = index_dictionary[terms[0] + '.1']
			for doc in p1:
				if doc in score:
					score[doc] += 0.3
				else:
					score[doc] = 0.3
		return score
	else:
		if terms[0] + '.0' not in index_dictionary and terms[0] + '.1' not in index_dictionary:
			return score
		if terms[1] + '.0' not in index_dictionary and terms[1] + '.1' not in index_dictionary:
			return score
		p1_title = []
		p1_abstract = []
		p2_title = []
		p2_abstract = []
		if terms[0] + '.0' in index_dictionary:
			p1_title = index_dictionary[terms[0] + '.0']
		if terms[0] + '.1' in index_dictionary:
			p1_abstract = index_dictionary[terms[0] + '.1']
		if terms[1] + '.0' in index_dictionary:
			p2_title = index_dictionary[terms[1] + '.0']
		if terms[1] + '.1' in index_dictionary:
			p2_abstract = index_dictionary[terms[1] + '.1']
		temp = {}
		for doc in p1_title:
			if doc in temp:
				temp[doc] += 0.7
			else:
				temp[doc] = 0.7
		for doc in p1_abstract:
			if doc in temp:
				temp[doc] += 0.3
			else:
				temp[doc] = 0.3
		for doc in p2_title:
			if doc in score:
				score[doc] += 0.7
			elif doc in temp:
				score[doc] = temp[doc] + 0.7
		for doc in p2_abstract:
			if doc in score:
				score[doc] += 0.3
			elif doc in temp:
				score[doc] = temp[doc] + 0.3
	return score

queries = ['monkey AND development', 'schistosoma', 'cholera and risk', 'mosquito and filariasis']


with open('index_posting', 'r') as f:
	index_posting = json.load(f)

with open('index_dictionary', 'r') as f:
	index_dictionary = json.load(f)


dict = {}
info = {}
for query in queries:
	terms = process_query(query)
	score = {}
	start_time = time.time()
	for i in range(100):
		score = zone_score_posting(terms, index_posting)
	time_taken = time.time() - start_time
	info[query] = {}
	info[query]['number_results'] = len(score.keys())
	info[query]['time_posting'] = time_taken


	start_time = time.time()
	for i in range(100):
		score = zone_score_dictionary(terms, index_dictionary)

	time_taken = time.time() - start_time
	info[query]['time_dictionary'] = time_taken
	score = {k: v for k, v in sorted(score.items(), reverse=True, key=lambda item: item[1])}
	dict[query] = score

with open('results', 'w') as f:
	json.dump(info, f, indent=4)
	f.write('\n\n\n\n')
	json.dump(dict, f, indent=4)