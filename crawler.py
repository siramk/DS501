from googlesearch import search
import requests
import time
from bs4 import BeautifulSoup
import json


queries = ["Computer Science" ,"IITs in India", "Cities of Chhatisgarh"]


data = [[], [], []]


for query in queries:
	url_count = 0
	for url in search(query, tld="com", lang="en", num=10, stop=None, pause=2, verify_ssl=True):
		print(url)
		time.sleep(5)

		response = requests.get(url)
		soup = BeautifulSoup(response.content, 'html5lib')

		paras = soup.find_all('p')

		content = ""
		count = 0
		for para in paras:
			if count == 2:
				break
			text = para.get_text().strip()
			if text:
				content += para.get_text()
				count += 1

		if content:
			data[queries.index(query)].append(content)
			url_count += 1
		if url_count == 20:
			break

with open('data', 'w') as f:
    f.write(json.dumps(data))