from googlesearch import search
import requests
import time
from bs4 import BeautifulSoup
import json


queries = ["Computer Science" ,"IITs in India", "Cities of Chhatisgarh"]
pages = 20

data = {}


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
			url_count += 1
			index = 'd' + str(url_count) + '_q' + str(queries.index(query) + 1)
			data[index] = {
				'id': url_count + pages*queries.index(query),
				'webpage_url': url,
				'content': content
			}
		if url_count == pages:
			break

with open('data', 'w') as f:
    json.dump(data, f, indent=4)