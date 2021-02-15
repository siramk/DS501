from googlesearch import search 
import tldextract  
import requests 
from bs4 import BeautifulSoup 
import csv

# to search 
query = "Computer science"

for url in search(query,"co.in", num=20,start= 1, stop=20, pause=2):  #Printing the top 15 URL responses
	print(url)

# Loop for each search result
for url in search(query,"co.in", num=20,start= 1, stop=20, pause=2): 
	respons = requests.get(url) #Response for the current URL
	soup = BeautifulSoup(respons.content, 'html5lib')
	paras=soup.find_all('p')  #Finding all the paragraph within the response

	para = "" #Initializing a empty paragraph
	for p in paras:   # Loop though each paragraph in response and append the contnet of that paragraph to  "para" so that we can save it as a continue paragraph
		para += p.get_text()

	if(para != ""):  #Perfom writing to file onlw when there is something in para
		ext_url = tldextract.extract(url)  #parsing the URL 
		domin_name = ext_url.domain   #Get the domain name from the parsed URL so that we can use it as a fine name

		with open('./{}.txt'.format(domin_name), mode='wt', encoding='utf-8') as file:  #Wtite "para" to a txt file whose filename is a domain name of current URL
			file.write(para)

