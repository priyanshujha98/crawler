from bs4 import BeautifulSoup
import requests
import datetime
import sqlalchemy
import pandas as pd
from washington import start
from dbtest import send_data,search
url ='https://techcrunch.com/'



def grab_data():
    response  = requests.get(url)
    soup = BeautifulSoup(response.text,'html.parser')
    
    links_unread = soup.find_all('div',{'class':'post-block post-block--image post-block--unread'})
    links_read = soup.find_all('div',{'class':'post-block post-block--image post-block--read'})
    
    
    var = []
    for i in links_unread:
        var.append(i)
    
    if len(links_read)!=0:
        for i in links_read:
            var.append(i)
        
    headline=[]
    timestamp=[]
    AUTHORS =[]
    SUMMARY=[]
    date_crawled = []
    news_source = [] 
    full = []
    
    for i in range(len(var)):
        title = var[i].find('a',{'class':'post-block__title__link'}).text
        title = title.replace('\n','')
        title = title.replace('\t','')
        headline.append(title)
        
        time = var[i].find('time',{'class':'river-byline__time'}).text
        time = time.replace('\n','')
        time = time.replace('\t','')
        timestamp.append(time)
        
        author = var[i].find('span',{'class':'river-byline__authors'})
        author = author.find_all('a')
        
        
        string = ''
        for j in author:
            string = string + j.text
            if len(author)>1:
                string = string + ', '
        
        if len(author)>1:
                string = string[:-2]
        
        author = string
        
        author = author.replace('\n','')
        author = author.replace('\t','')
        AUTHORS.append(author)
        
        summary = var[i].find('div',{'class':'post-block__content'}).text
        summary = summary.replace('\n','')
        summary = summary.replace('\t','')
        SUMMARY.append(summary)
        
        date_craw = str(datetime.datetime.today().date())
        date_crawled.append(date_craw)
        
        
        source = 'https://techcrunch.com/'
        news_source.append(source)
        
        full_article_url = var[i].find('a',{'class':'post-block__title__link'})['href'] 
        
        data = requests.get(full_article_url )
        soup = BeautifulSoup(data.text,'html.parser')
        
        result= soup.find('div',{'class':'article-content'})
        
        full_text = result.text
        
        full.append(full_text)
    
    
    final = pd.DataFrame({'Title':headline,'Author':AUTHORS,'Summary':SUMMARY,
                          'full_text':full,'date_published':timestamp, 'date_crawled':date_crawled,
                          'news_source':news_source})
    
    for i in final.index:
        try:
            t = pd.DataFrame()
            t =t.append(final.loc[i])
            t.reset_index(drop=True, inplace=True)
            try:
                count = search(t.loc[0]['Title'])
                print(count)
                if count < 25 :
                    test =t.loc[0].to_json()
                    send_data(test)
                    print('Data sent')
                else:
                    print('Skipped')
            except:
                test =t.loc[0].to_json()
                send_data(test)
                
        except Exception as e:
            print(e)
    start()

grab_data()
