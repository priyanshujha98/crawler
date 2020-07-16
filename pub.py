from Bio import Entrez
import json
import pandas as pd
from dbtest import send_data,search
import numpy as np

def search_query(query):

    handle = Entrez.esearch(db='pubmed', 
                            sort='relevance', 
                            retmax='20',
                            retmode='xml', 
                            term=query)
    results = Entrez.read(handle)
    return results

def fetch_details(id_list):
    ids = ','.join(id_list)
    handle = Entrez.efetch(db='pubmed',
                           retmode='xml',
                           id=ids)
    results = Entrez.read(handle)
    return results


def pub_data():
    f = open('pubmedcat.txt','r')
    f = f.read().split('\n')
    s=[]
    
    for j in f:
        results = search_query(j)
        id_list = results['IdList']
        papers = fetch_details(id_list)
        
        for i in papers['PubmedArticle']:
            s.append(json.dumps(i, indent=2, separators=(',', ':')))
    
    
    
    author=[]
    title = []
    date = []
    types = []
    source = []
    site = []
    url = []
    ref = []
    pdf_url = []
    abstract = []
    
    for le in range(len(s)):
        data =json.loads(s[le])['MedlineCitation']['Article']
        try:
            url.append('https://pubmed.ncbi.nlm.nih.gov/'+json.loads(s[le])['MedlineCitation']['PMID'])
        except:
            url.append(None)
        
        try:
            abstract.append(data['Abstract']['AbstractText'][0])
        except:
            abstract.append(None)
        
        try:
            pdf_url.append('http://doi.org/'+data['ELocationID'][0])
        except:
            pdf_url.append(None)
        
        try:
            site.append('pubmed')
        except:
            site.append(None)
        
        try:
            issn = 'ISSN: '+ data['Journal']['ISSN']
            tit = data['Journal']['Title']
            vol = 'volume'+' '+ data['Journal']['JournalIssue']['Volume']
            yr = data['Journal']['JournalIssue']['PubDate']['Year']
            
            ref.append(tit+'('+issn+')'+','+vol+'('+yr+')')
        except:
            ref.append(None)
        
        try:
            source.append(data['Journal']['Title'])
        except:
            source.append(None)
        
        try:
            types.append('academic')
        except:
            types.append(None)
        
        try:
            d = json.loads(s[le])['MedlineCitation']['DateCompleted']['Year']+'-'+json.loads(s[le])['MedlineCitation']['DateCompleted']['Month']+'-'+json.loads(s[le])['MedlineCitation']['DateCompleted']['Day']
            date.append(d)
        except:
            date.append(None)
        
        try:
            title.append(data['ArticleTitle'])
        except:
            title.append(None)
        
        try:
            aut = data['AuthorList']
            
            
            a=''
            for i in aut:
                a = a+(i['ForeName']+' '+i['LastName'] )
                a=a+', '
            
            author.append(a[:-2])
        except:
            author.append(None)
            
    
    df = pd.DataFrame({'Authors':author,'Title':title,'Date':date, 'Types':types, 'Source':source, 'Site':site, 'Url':url, 'Ref':ref, 'Pdf_url':pdf_url, 'Abstract':abstract})
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

pub_data()