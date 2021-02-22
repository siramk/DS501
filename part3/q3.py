import os
import sys
import json
import nltk
from nltk.stem import WordNetLemmatizer
from nltk.stem import PorterStemmer
import time
import math

path = os.getcwd() 
parent = os.path.abspath(os.path.join(path, os.pardir))
sys.path.insert(1, parent)
from part2.q2 import Q2

def skip_intersect(p1, p2):
	answer = []
	i = 0
	j = 0
	len_p1 = len(p1)
	len_p2 = len(p2)
	skip_size_p1 = int(math.sqrt(len_p1))
	skip_size_p2 = int(math.sqrt(len_p2))
	check_p1 = 0
	check_p2 = 0
	while i < len_p1 and j < len_p2:
		if p1[i] == p2[j]:
			answer.append(p1[i])
			i += 1
			j += 1
		elif p1[i] < p2[j]:
			if i == check_p1 and i+skip_size_p1 < len_p1 and p1[i+skip_size_p1] <= p2[j]:
				i += skip_size_p1
			else:
				i += 1
		else:
			if j == check_p2 and  j+skip_size_p2 < len_p2 and p2[j+skip_size_p2] <= p1[i]:
				j += skip_size_p2
			else:
				j += 1
		if i >= check_p1:
			check_p1 += skip_size_p1
		if j >= check_p2:
			check_p2 += skip_size_p2
	return answer

def skip_multi_intersect(terms, postings):
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
		result = skip_intersect(result, lis)
	return result


with open('../part1/inverted_index', 'r') as f:
	postings = json.load(f)

dict = {}
queries = ['IIT and Computer', 'IIT and mhrd', 'Bhilai and Raipur and bilaspur']
for query in queries:
	terms = Q2.process_query(query)

	start_time = time.time()
	for i in range(100):
		temp = Q2.multi_intersect(terms, postings)
	time_taken = (time.time() - start_time)
	dict[query] = {}
	dict[query]['Without_skip_pointer'] = time_taken

	start_time = time.time()
	for i in range(100):
		temp = skip_multi_intersect(terms, postings)
	time_taken = (time.time() - start_time)
	dict[query]['With_skip_pointer'] = time_taken

with open('Readme', 'w') as f:
    json.dump(dict, f, indent=4)