from googlesearch import search
import requests
import time
from bs4 import BeautifulSoup
import json
import urllib3

#To disable the warning of Insecure Request
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


#Given queries
queries = ["Computer Science" ,"IITs in India", "Cities of Chhatisgarh"]
#Number of pages to retrieve
pages = 20

data = {}


for query in queries:
	url_count = 0
	for url in search(query, tld="com", lang="en", num=10, stop=None, pause=2, verify_ssl=True):
		print(url)
		time.sleep(20)

		response = requests.get(url, verify = False) #Getting response of the link retrived from googlesearch
		soup = BeautifulSoup(response.content, 'html5lib')

		#Extracting all paragraphs of the website
		paras = soup.find_all('p')

		content = ""
		count = 0
		for para in paras:
			if count == 2: #Number of para in each website we have to retrieve
				break
			text = para.get_text().strip()
			if text: #Check paragraph is empty or not
				content += para.get_text()
				count += 1

		if content:
			#Storing the data obtained in dictionary
			url_count += 1
			index = 'd' + str(url_count) + '_q' + str(queries.index(query) + 1)
			data[index] = {
				'id': url_count + pages*queries.index(query),
				'webpage_url': url,
				'content': content
			}
		if url_count == pages: #Checking the url retrieve is equal to the number of pages we have to retrieve
			break

#Dumping the dictionary into the file
with open('crawled_data', 'w') as f:
    json.dump(data, f, indent=4)
