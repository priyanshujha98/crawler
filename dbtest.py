from  elasticsearch import Elasticsearch
import pandas as pd

def send_data(data,index_name):
    es = Elasticsearch(['localhost:9200'])
    res = es.index(index=index_name,doc_type='devops',body=data)    
    
    
def search(title,index_name):
    es = Elasticsearch(['localhost:9200'])
    r = es.search(index = index_name, body={'query':{'match':{'Title':title}}})
    
    test = r['hits']['max_score']    
    return test

def get_data(search, index_name):
    es = Elasticsearch(['localhost:9200'])
    r = es.search(index = index_name, body={'query':{'match':{'Title':search}}})
    
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

def get_data_index(index):
    es = Elasticsearch(['localhost:9200'])
    result = pd.DataFrame()
    r = es.search(index = index)
    
    test = r['hits']['hits']    
    
    
    for i in test:
        t = pd.DataFrame()
        t = pd.DataFrame([i['_source']]) 
        try:
            if t.loc[0]['Title'] not in result['Title'].values:
                result = result.append(t)
        except:
                result = result.append(t)
    return result

def get_index():
    es = Elasticsearch(['localhost:9200'])
    total = list(es.indices.get_alias('*').keys())
    return total    


def get_everything():
    es = Elasticsearch(['localhost:9200'])
    total = list(es.indices.get_alias('*').keys())
    
    result = pd.DataFrame()
    for j in total:    
        r = es.search(index = j)
        
        test = r['hits']['hits']    
        
        
        for i in test:
            t = pd.DataFrame()
            t = pd.DataFrame([i['_source']]) 
            try:
                if t.loc[0]['Title'] not in result['Title'].values:
                    result = result.append(t)
            except:
                result = result.append(t)
    return result