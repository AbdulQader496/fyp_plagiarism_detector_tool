from bs4 import BeautifulSoup as bs
import warnings
import requests

warnings.filterwarnings('ignore', module='bs4')

def searchBing(query, num):

    url = 'https://www.bing.com/search?q=' + query
    urls = []

    page = requests.get(url, headers= {'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36'})
    soup = bs(page.text, 'html.parser')

    for link in soup.find_all('a'):
        url = str(link.get('href'))
        if url.startswith('http'):
            if not url.startswith('http://go.m') and not url.startswith('https://go.m'):
                urls.append(url)

    return urls[:num]

def extractText(url):
    page = requests.get(url)
    soup = bs(page.text, 'html.parser')
    return soup.get_text()