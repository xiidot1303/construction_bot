from dotenv import load_dotenv
import os

basedir = os.path.abspath(os.path.dirname(''))
load_dotenv(os.path.join(basedir, '.env'))
WHERE = os.environ.get('WHERE')
from bs4 import BeautifulSoup
import requests
def currency():
    if WHERE != 'SERVER':
        return 10000.00
    url = 'https://bank.uz/currency'
    content = BeautifulSoup(requests.get(url).content, features='lxml')
    top_left = content.find('div', {'class':"diogram-top-left"})
    ul = top_left.find('ul', {'class': 'nav nav-tabs'})
    tabs_a = ul.find('div', {'class': 'tabs-a'})
    text = tabs_a.find_all('span', {'class': "medium-text"})
    curren = float(text[1].text.replace(' ', ''))
    return curren