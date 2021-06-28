import requests
from bs4 import BeautifulSoup
URL = 'https://quotes.toscrape.com/'
response = requests.get(URL)

# print(response.text)

# soup = BeautifulSoup(response.text, 'html.parser')
soup = BeautifulSoup(response.text, 'lxml')

# print(soup)

# quotes = soup.find('span', class_='text')


# quotes = soup.find_all('span', class_='text')
# quotes = soup.select_one('span.text')

# print(quotes.name)
# print(quotes.get_text(strip=True))

# print(quotes.get('itemprop'))

# quotes.decompose()
# quotes = soup.select_one('span.text')
# print(quotes.get_text(strip=True))

# quotes = soup.find('div', class_='quote')

# print(quotes.descendants)

# for item in quotes.descendants:
#     if item.name is not None:
#         print(item.name)
#         if item.name == 'a':
#             print(item.get('href'))

quotes_list = []
quotes = soup.find('span', class_='text')
authors = soup.find_all('small', class_='authors')

tags = soup.find_all('div', class_='tags')

for i in range(0, len(quotes)):
    quote = {}
    quote['quote'] = quotes[i].text
    quote['author'] = authors[i].text
    quote['author_info'] = URL + authors[i].find_next_sibling().get('href')

    # print(quotes[i].text)
    # print('--' + authors[i].text)
    parseTags = tags[i].find_all('a', class_='tag')
    for tag in parseTags:
        print(tag.text)
print()
quotes_list.append(quote)

print(quotes_list)
