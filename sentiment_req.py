#News API doc: https://newsapi.org/docs/endpoints/everything
# Import the libraries we need

import pandas as pd
import requests
import numpy as np
from bs4 import BeautifulSoup
import re
import mysql.connector
import datetime
#Scrape wiki article for cabinet members
base_url='https://en.wikipedia.org/wiki/Cabinet_of_the_United_States'
req=requests.get(base_url)
cab_soup = BeautifulSoup(req.content, 'html.parser')
#create list of cabinet members
cabinet = [cab_soup.find_all('table')[3].find_all('tr')[i].find_all('td')[1].find_all('a')[-1]['title']
 for i in range(1,len(cab_soup.find_all('table')[3].find_all('tr')))
]
#president
president = ['Donald Trump']
#scrape wiki article for senators
base_url='https://en.wikipedia.org/wiki/List_of_current_United_States_Senators'
req=requests.get(base_url)
sen_soup = BeautifulSoup(req.content, 'html.parser')
#create list of senators
senate=[sen_soup.find_all('table')[4].tbody.find_all('tr')[i].find_all('th')[0].find_all('a')[0]['title']
 for i in range(1,len(sen_soup.find_all('table')[4].find_all('tr')))]
#scrape wiki for congresspeople
base_url='https://en.wikipedia.org/wiki/List_of_current_members_of_the_United_States_House_of_Representatives'
req=requests.get(base_url)
house_soup = BeautifulSoup(req.content, 'html.parser')
#create list of congresspeople
house=[house_soup.find_all('table')[6].find_all('tr')[i].find_all('td')[1].find_all('a')[-1]['title']
 for i in range(1,len(house_soup.find_all('table')[6].find_all('tr')))
 if len(house_soup.find_all('table')[6].find_all('tr')[i].find_all('td')[1].find_all('i'))==0
]
#democratic candidates
demcands = ["Beto O'Rourke",'Pete Buttigieg','Julian Castro']
#concatenate political lists
politicians = [re.sub(" \(.*?\)","",name) for name in cabinet+senate+house+demcands]
#function to handle requests
def get_news(date,politicians):
    #article counter
    n_articles=0
    president = "Donald Trump"
    base_url = "https://newsapi.org/v2/everything"
    for i in range(int(len(politicians)/100)+1):
        qlist = politicians[i*100:(i+1)*100]
        req= requests.get(
        base_url,
        params={'q':qlist,
           'from':date,
           'sortBy':'popularity',
            'pageSize':100,
            'page':1,
           'language':'en',
           'apiKey':'697e87dceab84ce18c49963b7da44ac3'})
        filename = './data/newscrape'+date+str(i)+'.csv'
        if 'articles' in req.json().keys():
            pd.DataFrame(req.json(),index=range(len(req.json()['articles']))).to_csv(filename)
        if req.json()['totalResults']<100:
            n_articles+=req.json()['totalResults']
        elif req.json()['totalResults']>=100:
            n_articles+=100
    preq= requests.get(
    base_url,
    params={'q':president,
       'from':date,
       'sortBy':'popularity',
        'pageSize':100,
        'page':1,
        'language':'en',
       'apiKey':'697e87dceab84ce18c49963b7da44ac3'})
    filename = './data/newscrape'+date+'trump'+'.csv'
    if 'articles' in preq.json().keys():
        pd.DataFrame(preq.json(),index=range(len(preq.json()['articles']))).to_csv(filename)
    if req.json()['totalResults']<100:
        n_articles+=req.json()['totalResults']
    elif req.json()['totalResults']>=100:
        n_articles+=100
    print(n_articles)
date = datetime.datetime.now()- datetime.timedelta(hours=1)
get_news(date,politicians)
