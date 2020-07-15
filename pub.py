from Bio import Entrez
import json
import pandas as pd

def search(query):

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
        results = search(j)
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
    citation = []
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
            site.append('PubMed')
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
            try:
                cit = aut[0]['AffiliationInfo'][0]['Affiliation']
                citation.append(cit)
            except:
                citation.append(None)
            
            a=''
            for i in aut:
                a = a+(i['ForeName']+' '+i['LastName'] )
                a=a+', '
            
            author.append(a[:-2])
        except:
            author.append(None)
            
        
    df = pd.DataFrame({'Author':author,'Title':title,'Date':date, 'Types':types, 'Source':source, 'Site':site, 'Url':url, 'Ref':ref, 'Pdf_url':pdf_url, 'Abstract':abstract, 'Citation' : citation})
    
    
