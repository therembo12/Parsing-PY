from re import S
import requests
from bs4 import BeautifulSoup
from pprint import pp, pprint
import json
URL = 'https://quotes.toscrape.com/'

quotes_list = []
page = 1


def getResponse(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    return soup


def ParseIF(authorName, quoteText):
    for elem in quotes_list:
        if authorName in elem['author']:
            elem['quote'].append(quoteText)
            return True
    return False


while True:
    soup = getResponse(f'{URL}page/{page}/')
    page = page + 1
    quotes = soup.find_all('span', class_='text')
    if len(quotes) == 0:
        break
    authors = soup.find_all('small', class_='author')

    for i in range(0, len(quotes)):
        au = authors[i].text.strip()
        qu = quotes[i].text.strip()
        if ParseIF(au, qu) == True:
            continue

        quote = {}
        quote['author'] = au
        quote['author_info'] = URL + \
            authors[i].find_next_sibling().get('href')[1:]
        quote['quote'] = []
        quote['quote'].append(qu)

        quotes_list.append(quote)

quotes_list = sorted(
    quotes_list, key=lambda quotes_list: quotes_list['author'], reverse=True)

author_list = []
for index, item in enumerate(quotes_list):
    if index > 0 and item['author'] == quotes_list[index-1]['author']:
        continue
    soup = getResponse(item['author_info'])
    author = {}
    author['name'] = soup.find('h3', class_='author-title').text.strip()
    author['born'] = soup.find('span', class_='author-born-date').text.strip()
    author['location'] = soup.find(
        'span', class_='author-born-location').text.strip()
    author['description'] = soup.find(
        'div', class_='author-description').text.strip()
    author['url'] = item['author_info']
    author['quote'] = []
    author['quote'].append(item['quote'])
    author_list.append(author)
pprint(author_list)
with open('quotes.json', 'w') as file:
    json.dump(author_list, file, indent=4)
    file.close()
