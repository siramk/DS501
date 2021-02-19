import json
import nltk
from nltk.stem import WordNetLemmatizer
from nltk.stem import PorterStemmer


class Q2:
	@staticmethod
	def intersect(p1, p2):
		i = 0
		j = 0
		answer = []
		while i < len(p1) and j < len(p2):
			if p1[i] == p2[j]:
				answer.append(p1[i])
				i += 1
				j += 1
			elif p1[i] < p2[j]:
				i += 1
			else:
				j += 1
		return answer

	@staticmethod
	def multi_intersect(terms, postings):
		mul_list = []
		result = []
		for term in terms:
			if term in postings:
				mul_list.append(postings[term])
			else:
				return result
		mul_list.sort(key=len, reverse=True)
		result = mul_list[0]
		for lis in mul_list[1:]:
			if len(result) == 0:
				return result
			result = Q2.intersect(result, lis)
		return result

	@staticmethod
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



if __name__ == "__main__":
	with open('inverted_index_stem', 'r') as f:
		postings = json.load(f)


	print("Enter query")
	query = input()
	# query = 'Bhilai AND Raipur AND Bilaspur'
	terms = Q2.process_query(query)
	print(Q2.multi_intersect(terms, postings))



#Some Queries
#IIT And computer 
#IIT and computer and GOA
#IIT and technology and department
#IIT and mhrd
#Bhilai and Raipur and bilaspur
#State and Raipur