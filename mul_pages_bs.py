from bs4 import BeautifulSoup
import requests

root = 'https://subslikescript.com'
website =  f'{root}/movies'
result = requests.get(website)
content = result.text

soup = BeautifulSoup(content , 'lxml')
# print(soup.prettify())

box = soup.find('article', class_ = 'main-article')
pages = []
title_transcript = {}
for link in box.find_all('a', href = True):
    webpage = (f'{root}/{link['href']}')
    pages.append(webpage)
    
    sub_result = requests.get(webpage)
    sub_content = sub_result.text
    sub_soup = BeautifulSoup(sub_content , 'lxml')
    
    sub_box = sub_soup.find('article', class_ = 'main-article')
    title = sub_box.find('h1').get_text()
    transcript = sub_box.find('div', class_ = 'full-script').get_text(strip = True, separator= ' ')
    title_transcript[title] = transcript
    
    with open(f'{title}.txt','w+') as file:
        file.write(transcript)

# print(title_transcript)