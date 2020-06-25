from newsfetch.news import newspaper
from bs4 import BeautifulSoup

from selenium import webdriver

import requests
import pandas as pd
from dbtest import send_data,search


websites = ['https://www.abc.net.au',
'https://www.bbc.com',
'https://www.voanews.com',
'https://techcrunch.com',
'https://www.theguardian.com']


asli = []



for j in websites:
    response = requests.get(j)
        
    soup = BeautifulSoup(response.text,'html.parser')
    
    url = soup.find_all('a')
    
    
    for i in range(len(url)) :
        try:
            url[i] = url[i]['href']
        except:
            try:
                url.remove(url[i])
            except:
                pass
    
    var=[]
    for i in url:
       if i not in var:
           var.append(i)

    
    url = var
   

    try:
        f  = open('urlparsed.txt','r')
        already_parsed = f.read().split('\n')
        f.close()
    except:
        f = open('urlparsed.txt','w')
        for i in url:
            try:
                i =i['href']
            except:
                pass
            f.write(str(i))
            f.write('\n')
        f.close()
       
    try:
        for i in already_parsed:
            try:
                url.remove(i)
            except:
                pass
        
        for i in url:
            already_parsed.append(i)
        
        f = open('urlparsed.txt','w')
        for i in already_parsed:
                try:
                    i =i['href']
                except:
                    pass
                f.write(str(i))
                f.write('\n')
        f.close()
    except:
        pass
        
    for i in url:    
        try :
            try:
                i =i['href']
            except:
                pass
            
            
            if 'https' not in i:
                if 'http' not in i:
                    i = j+i
            
            print('\n',i)
                
            response = requests.get(i)
            details = newspaper(i)
            count = len(details.article)
            publish_date = details.date_publish
            cr_date = details.date_download
            description = details.description
            summary = details.summary
            category = details.category
            if count > 1500:
                if len(description) > 10 or len(summary) > 10:
            
                    print("Appended")
                    asli.append(i)
                    
                else:
                    pass
            else:
                pass
        except:
            pass




headline=[]
timestamp=[]
AUTHORS =[]
SUMMARY=[]
date_crawled = []
news_source = [] 
full = []
img_url = []
for i in asli:
    driver = webdriver.Chrome('/home/priyanshu/project 10/chromedriver')
    driver.get(i)
    details = newspaper(i)
    headline.append(details.headline)
    timestamp.append(details.date_publish)
    author=''
    for i in details.authors:
        author = author + i
        author =author + ', '
        
    
    author= author[:-2]
    AUTHORS.append(author)
    
    if len(details.summary) > 10:
        SUMMARY.append(details.summary)
    else:
        SUMMARY.append(details.description)
    
    date_crawled.append(details.date_download)
    news_source.append(details.source_domain)
    
    full.append(details.article)
    
    re = driver.find_elements_by_tag_name('img')
    for i in re:
        if'.jpg' in i.get_attribute('src'):
            img_url.append(i.get_attribute('src'))
            break;
    
    driver.close()

final = pd.DataFrame({'Title':headline,'Author':AUTHORS,'Summary':SUMMARY,
                          'full_text':full,'date_published':timestamp, 'date_crawled':date_crawled,
                          'news_source':news_source,'img':img_url})
    
for i in final.index:
    try:
        t = pd.DataFrame()
        t =t.append(final.loc[i])
        t.reset_index(drop=True, inplace=True)
        try:
            count = search(t.loc[0]['Title'],t.loc[0]['news_source'])
            print(count)
            if count < 25 :
                test =t.loc[0].to_json()
                send_data(test,t.loc[0]['news_source'])
                print('Data sent')
            else:
                print('Skipped')
        except:
            test =t.loc[0].to_json()
            send_data(test,t.loc[0]['news_source'])
            
    except Exception as e:
        print(e)
