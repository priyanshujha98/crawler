from bs4 import BeautifulSoup
import requests
import datetime
from dbtest import send_data,search
import pandas as pd

from selenium import webdriver


url ='https://www.theguardian.com/'



def grab(test,count):
    headline=[]
    timestamp=[]
    AUTHORS =[]
    SUMMARY=[]
    date_crawled = []
    news_source = [] 
    full = []
    

    for k in range(0,len(test)):
        try:
            driver = webdriver.Chrome('/home/priyanshu/project 10/chromedriver')
            driver.get(test[k])
            try:
                title= driver.find_element_by_tag_name('h1').text
                
              
                
                author= driver.find_elements_by_class_name('tone-colour')
                
                
                a=''
                for i in author:
                    if len(author) <2:
                        a = a+i.text
                    else:
                        a = a+i.text
                        a = a+', '
                
                if len(author) <2 :
                        a = a[:-2]  
                
                author = a
                
                
                time = driver.find_element_by_class_name('content__dateline').text.split('\n')[0]
                
                
                try:
                    soup = BeautifulSoup(driver.page_source,'html.parser')
                    content = soup.find('div',{'class':'content__article-body from-content-api js-article__body'}).text
                
                    replace = soup.find('div',{'class':'after-article js-after-article'}).next.next.text
                    
                    replacement = soup.find_all('aside')
                    for i in replacement:
                        content = content.replace(i.text,'')
                    
                    content = content.replace(soup.find('div',{'class':'submeta'}).text,'')
                    
                    content = content.replace(replace,'')
                    summary = soup.find('div',{'class':'content__standfirst'}).text
                    if len(summary)>300:
                        summary = summary[:300]
                except:
                    summary = soup.find('div',{'class':'content__standfirst'}).text
                    content = summary
                    if len(summary)>300:
                        summary = summary[:300]
                
                headline.append(title)
                AUTHORS.append(author)
                timestamp.append(time)
                SUMMARY.append(summary)
                full.append(content)
                
                
                
                date = str(datetime.datetime.today().date())
                date_crawled.append(date)
                
                source = 'https://www.theguardian.com/'
                news_source.append(source)
                driver.close()
            except:
                try:
                    
                    title= driver.find_element_by_tag_name('h1').text
                 
                    
                    soup = BeautifulSoup(driver.page_source,'html.parser')
                    author = soup.find_all('address',{'aria-label':'Contributor info'})
                    
                    a=''
                    for i in author:
                        if len(author) <2:
                            a = a+i.text
                        else:
                            a = a+i.text
                            a = a+', '
                    
                    if len(author) <2 :
                        a = a[:-2]
                
                    author = a
                    
                    time = soup.find('div',{'class':'css-1kkxezg'}).text.replace(soup.find('span',{'class':'css-nyo8hb'}).text,'')
                    
                    try:
                        soup = BeautifulSoup(driver.page_source,'html.parser')
                        content = soup.find('div',{'class':'article-body-commercial-selector css-79elbk'}).text
                    
                        replace = soup.find('section',{'class':'css-q5digb'}).text
                        
                        replacement = soup.find_all('div',{'class':'css-wz7t6r'})
                        for i in replacement:
                            content = content.replace(i.text,'')
                        
                        content = content.replace(soup.find('div',{'class':'css-739uag'}).text,'')
                        
                        content = content.replace(replace,'')
                        summary = soup.find('div',{'class':'css-12nmdsr'}).text
                        if len(summary)>300:
                            summary = summary[:300]
                    except:
                        summary = soup.find('div',{'class':'content__standfirstcss-12nmdsr'}).text
                        content = summary
                        if len(summary)>300:
                            summary = summary[:300]
                    
                    if title not in headline:
                        headline.append(title)
                    AUTHORS.append(author)
                    timestamp.append(time)
                    SUMMARY.append(summary)
                    full.append(content)
                    
                    
                    date = str(datetime.datetime.today().date())
                    date_crawled.append(date)
                    
                    source = 'https://www.theguardian.com/'
                    news_source.append(source)
                    driver.close()
                except:
                    print('Passed: ',test[k])
                    driver.close()
            
        except Exception as err:
            print(err)
            driver.close()
            pass

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
                print('Data sent')
        except Exception as e:
            print(e)
            # print("This error occured due to unique constraint and no need to worry this error can be skipped:")
        
def start():
    response = requests.get(url)
    
    soup = BeautifulSoup(response.text,'html.parser')
    
    result = soup.find_all('div',{'class':'fc-container--rolled-up-hide fc-container__body'})
    
    links=[]
    for i in range(len(result)):
        links.append(result[i].find_all('a'))
    
    
    
    
    test=[]
    
    for i in links:
        for j in i:
            if j['href'] not in test:
                test.append(j['href'])
    count = 0
    grab(test,count)


