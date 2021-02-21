import json
import nltk
from nltk.stem import WordNetLemmatizer
from nltk.stem import PorterStemmer

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
	if 'title' in li1:
		score += g[0]
	if 'abstract' in li1:
		score += g[1]
	if 'title' in li2:
		score += g[0]
	if 'abstract' in li2:
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


with open('index_posting', 'r') as f:
	index_posting = json.load(f)

queries = ['monkey AND development', 'schistosoma', 'cholera and risk', 'mosquito and filariasis', 'health and structure']

for query in queries:
	terms = process_query(query)
	score = zone_score_posting(terms, index_posting)
	print(score)
