import arxivscraper
import datetime
import pandas as pd
from dbtest import send_data,search
import numpy as np

def axir_data():
    f = open('categories.txt','r')
    f = f.read().split('\n')
    
    for i in range(0, len(f)):
        f[i] = f[i].split('\t')
        for j in range(f[i].count('')):
            try:
                f[i].remove('')
            except:
                pass
    #print (f)
    output = []
    for i in f:
        print(i[1])
        scraper = arxivscraper.Scraper(category=i[1], date_from=str((datetime.datetime.now()-datetime.timedelta(1)).date()),date_until=str(datetime.datetime.now().date()))
        output.append(scraper.scrape())
    
    
    cols = ('id', 'title', 'categories', 'abstract', 'doi', 'created', 'updated', 'authors')
    df = pd.DataFrame([],columns=cols)
    for i in output:
        try:
            df = df.append(pd.DataFrame(i,columns=cols))
        except:
            pass
    df.reset_index(drop=True, inplace = True)
    
    df = df.rename(columns={'abstract':'Abstract'})
    df = df.rename(columns={'created':'Date'})
    df = df.rename(columns={'title':'Title'})
    df['Types'] = 'academic'
    df['Site'] = 'arxiv'
    df['Source'] =None
    
    for i in range(len(df.authors)):
        a=''
        for j in df.authors[i]:
            a= a+ j
            a=a+', '
        a=a[:-2]
        df.authors[i] = a
    df = df.rename(columns={'authors':'Authors'})
    
    var=[]
    for i in range(len(df.id)):
        u = 'https://arxiv.org/abs/'
        var.append(u + df.id[i])
    
    for i in range(len(df.doi)):
        df.doi[i] = 'http://doi.org/'+df.doi[i]
    
    df = df.rename(columns={'doi':'Ref'})
    
    df['Url'] = var
    
    
    var=[]
    for i in range(len(df.id)):
        u = 'https://arxiv.org/pdf/'
        var.append(u + df.id[i])
    
    df['Pdf_url'] = var
    #print (df)

    df = df.where(pd.notnull(df), np.nan)
    for i in df.index:
        try:
            t = pd.DataFrame()
            t =t.append(df.loc[i])
            t.reset_index(drop=True, inplace=True)
            try:
                count = search(t.loc[0]['Title'],t.loc[0]['Site'])
                print(count)
                if count < 25 :
                    test =t.loc[0].to_json()
                    send_data(test,t.loc[0]['Site'])
                    print('Data sent')
                else:
                    print('Skipped')
            except:
                test =t.loc[0].to_json()
                send_data(test,t.loc[0]['Site'])
                
        except Exception as e:
            print(e)
    print('info fetched')

axir_data()
