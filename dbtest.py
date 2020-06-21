from  elasticsearch import Elasticsearch
import pandas as pd

def send_data(data):
    es = Elasticsearch(['localhost:9200'])
    res = es.index(index='articles',doc_type='devops',body=data)    
    
    
def search(title):
    es = Elasticsearch(['localhost:9200'])
    r = es.search(index = 'articles', body={'query':{'match':{'Title':title}}})
    
    test = r['hits']['max_score']    
    return test

def get_data(search):
    es = Elasticsearch(['localhost:9200'])
    r = es.search(index = 'articles', body={'query':{'match':{'Title':search}}})
    
    test = r['hits']['hits']    
    
    result = pd.DataFrame()
    for i in test:
        t = pd.DataFrame()
        t = pd.DataFrame([i['_source']]) 
        try:
            if t.loc[0]['Title'] not in result['Title'].values:
                result = result.append(t)
        except:
            result = result.append(t)
        
    
    return result