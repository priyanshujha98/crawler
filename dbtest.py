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
    result = pd.DataFrame()
    for k in search:
        r = es.search(index = index_name, body={'query':{'match':{'full_text':k}}})
        
        test = r['hits']['hits']
        
        
        for i in test:
            t = pd.DataFrame()
            t = pd.DataFrame([i['_source']]) 
            t['id'] = i['_id']
            try:
                if t.loc[0]['_id'] not in result['_id'].values:
                    result = result.append(t)
            except:
                result = result.append(t)
    return result 
        

def display_data(search, index_name):
    es = Elasticsearch(['localhost:9200'])
    r = es.search(index = index_name, body={'query':{'match':{'_id':search}}})
    
    test = r['hits']['hits']
    
    result = pd.DataFrame()
    for i in test:
        t = pd.DataFrame()
        t = pd.DataFrame([i['_source']]) 
        t['id'] = i['_id']
        try:
            if t.loc[0]['_id'] not in result['_id'].values:
                result = result.append(t)
        except:
            result = result.append(t)
        
    return result

def get_data_index(index):
    es = Elasticsearch(['localhost:9200'])
    result = pd.DataFrame()
    r = es.search(index = index)
    
    test = r['hits']['hits']    
    
    # test[0]['_id']
    for i in test:
        t = pd.DataFrame()
        t = pd.DataFrame([i['_source']]) 
        t['id'] = [i['_id']]
        
        try:
            if t.loc[0]['id'] not in result['id'].values:
                result = result.append(t)
        except:
                result = result.append(t)
    return result

def get_index():
    es = Elasticsearch(['localhost:9200'])
    total = list(es.indices.get_alias('*').keys())
    
    final_list=[]
    count = []
    for i in total:
        r = es.search(index = i)
    
        test = r['hits']['hits']    
        final_list.append(i)
        count.append(len(test))
    final =pd.DataFrame({'indices':final_list,'total':count})
    return final

# index = 'www.bbc.com'

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
            t['id'] = [i['_id']]
            try:
                if t.loc[0]['id'] not in result['id'].values:
                    result = result.append(t)
            except:
                result = result.append(t)
    return result

def get_only_data(search):
    es = Elasticsearch(['localhost:9200'])
    total = list(es.indices.get_alias('*').keys())
    
    result = pd.DataFrame()
    for j in total:    
        for k in search:
            r = es.search(index = j, body={'query':{'match':{'full_text':k}}})
            
            test = r['hits']['hits']    
            
            
            for i in test:
                t = pd.DataFrame()
                t = pd.DataFrame([i['_source']]) 
                t['id'] = [i['_id']]
                try:
                    if t.loc[0]['id'] not in result['id'].values:
                        result = result.append(t)
                except:
                    result = result.append(t)
    return result

def get_data_count(search):
    es = Elasticsearch(['localhost:9200'])
    total = list(es.indices.get_alias('*').keys())
    
    result = pd.DataFrame()
    for j in total:    
        for k in search:
            r = es.search(index = j, body={'query':{'match':{'full_text':k}}})
            
            test = r['hits']['hits']    
            
            
            for i in test:
                t = pd.DataFrame()
                t = pd.DataFrame([i['_source']]) 
                t['id'] = [i['_id']]
                try:
                    if t.loc[0]['id'] not in result['id'].values:
                        result = result.append(t)
                except:
                    result = result.append(t)
    return result

def get_type():
    es = Elasticsearch(['localhost:9200'])
    total = list(es.indices.get_alias('*').keys())
    
    result = pd.DataFrame()
    for j in total:    
        r = es.search(index = j)
        
        test = r['hits']['hits']    
        
        
        for i in test:
            t = pd.DataFrame()
            t = pd.DataFrame([i['_source']['Types']]) 
            try:
                    if t.loc[0]['id'] not in result['id'].values:
                        result = result.append(t)
            except:
                    result = result.append(t)
    return result