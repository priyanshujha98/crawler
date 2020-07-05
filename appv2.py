from flask import Flask,render_template,request,redirect,url_for, make_response, jsonify, session

from dbtest import get_everything, get_index, get_data_index, display_data, get_data,get_only_data, get_data_count


from tryv1 import grab_data

app = Flask(__name__)

app.secret_key = 'super secret key'


@app.route('/data/', methods = ['GET','POST'])
def home():
    every = get_everything()
    try:
        # print('Printing session',session['val'])
        if len(session['val']) >0:
            val_dict = session['val']
            if len(val_dict['articles']) > 0:
                articles = val_dict['articles']
            else:
                articles=[]
            if val_dict['keyword'] !=None:
                words = val_dict['keyword']   
            else:
                words=[]
        else:
            articles = []
            words = []
    except:
        articles = []
        words = []


    # print(articles,words)
    if request.method=='POST':
        news_search = request.form['news_search']
        news_search = news_search.split(',')
        
        for i in range(news_search.count('')):
            news_search.remove('')
    
        if len(news_search)== 0:
            every = get_everything()
            # return redirect(url_for('home'))
        elif len(news_search)!=0:
            every = get_only_data(news_search)

        try:
            already_seen = request.cookies.get('visited')
            already_seen = already_seen.split(',')
            every.reset_index(drop=True,inplace=True)
            for i in range(len(every.id)):
                if every.id[i] in already_seen:
                    every = every.drop([i],axis= 0)
        except:
            pass
                
        # print(len(every))
        index_count = []
        for i in articles:
                count = list(every.news_source).count(i)
                # va = []
                # count  = get_index()
                # for j in range(len(count)):
                #     if i == count['indices'][j]:
                #         va = count['total'][j]
                        
                index_count.append(count)
        # print(index_count)
        
        word_count = []
        for i in words:
            res = get_data_count([i])
            res.reset_index(drop=True, inplace=True)
            try:
                for j in range(len(res.id)):
                    try:
                        if res.id[j] in already_seen:
                            res = res.drop([j],axis = 0)
                    except:
                        # print('Into the pass')
                        pass
            except:
                pass
            word_count.append(len(res))
        return render_template('home.html',articles=zip(articles,index_count),words=zip(words,word_count),data=zip(every.Author,every.Summary,every.Title,every.date_crawled,every.date_published,every.full_text,every.img,every.news_source,every.id))
    try:
        already_seen = request.cookies.get('visited')
        already_seen = already_seen.split(',')

        # print('Before ',len(every))
        every.reset_index(drop=True,inplace=True)
        for i in range(len(every)):
            if every['id'][i] in already_seen:
                # print(every['id'][i])
                every = every.drop([i],axis= 0)
    except:
        pass
    # print('After',len(every))
    #print(every)
    index_count = []
    for i in articles:
            count = list(every.news_source).count(i)
            index_count.append(count)
    # print('I_C',index_count)
    
    word_count = []
    for i in words:
        res = get_data_count([i])
        res.reset_index(drop=True, inplace=True)
        try:
            for j in range(len(res.id)):
                try:
                    if res.id[j] in already_seen:
                        res = res.drop([j],axis = 0)
                except:
                    # print('Into the pass')
                    pass
        except:
            pass
        word_count.append(len(res))
        
    # print('W_C',word_count)
    return render_template('home.html',articles=zip(articles,index_count),words=zip(words,word_count),data=zip(every.Author,every.Summary,every.Title,every.date_crawled,every.date_published,every.full_text,every.img,every.news_source,every.id))

@app.route('/update/')
def update():
    return  redirect(url_for('home'))

@app.route('/seekeyword/')
def seekeyword():
    key_word = request.args.get('key_word')
    every =  get_only_data([key_word])
    
    if len(session['val']) >0:
        val_dict = session['val']
        if len(val_dict['articles']) > 0:
            articles = val_dict['articles']
        else:
            articles=[]

        if len(val_dict['keyword']) > 0:
            words = val_dict['keyword']   
        else:
            words = []
    else:
        articles = []
        words = []
    # print('words',words)
    try:
        already_seen = request.cookies.get('visited')
        already_seen = already_seen.split(',')

        # print('Before ',len(every))
        every.reset_index(drop=True,inplace=True)
        for i in range(len(every)):
            if every['id'][i] in already_seen:
                # print(every['id'][i])
                every = every.drop([i],axis= 0)
    except:
        pass
    index_count = []
    for i in articles:
            count = list(every.news_source).count(i)
            index_count.append(count)
    word_count = []
    for i in words:
        res = get_data_count([i])
        res.reset_index(drop=True, inplace=True)
        try:
            for j in range(len(res.id)):
                try:
                    if res.id[j] in already_seen:
                        res = res.drop([j],axis = 0)
                except:
                    # print('Into the pass')
                    pass
        
        except:
            pass
        word_count.append(len(res))
    # print('word Af',words,word_count,articles,index_count)
    if len(every) >0:
        return render_template('home.html',articles=zip(articles,index_count),words=zip(words,word_count),data=zip(every.Author,every.Summary,every.Title,every.date_crawled,every.date_published,every.full_text,every.img,every.news_source,every.id))
    else:
        return render_template('home.html',articles=zip(articles,index_count),words=zip(words,word_count))


@app.route('/seeindex/')
def seeindex():
    index_name = request.args.get('index')
    every =  get_data_index(index_name)

    if len(session['val']) >0:
        val_dict = session['val']
        if len(val_dict['articles']) > 0:
            articles = val_dict['articles']
        if len(val_dict['keyword']) > 0:
            words = val_dict['keyword']   
    else:
        articles = []
        words = []
    try:
        already_seen = request.cookies.get('visited')
        already_seen = already_seen.split(',')

        # print('Before ',len(every))
        every.reset_index(drop=True,inplace=True)
        for i in range(len(every)):
            if every['id'][i] in already_seen:
                # print(every['id'][i])
                every = every.drop([i],axis= 0)
    except:
        pass
    index_count = []
    for i in articles:
            count = list(every.news_source).count(i)
            index_count.append(count)
    word_count = []
    for i in words:
        res = get_data_count([i])
        res.reset_index(drop=True, inplace=True)
        try:
            for j in range(len(res.id)):
                try:
                    if res.id[j] in already_seen:
                        res = res.drop([j],axis = 0)
                except:
                    # print('Into the pass')
                    pass
        except:
            pass
        word_count.append(len(res))
        
    # print('W_C',word_count,len(every))
    return render_template('home.html',articles=zip(articles,index_count),words=zip(words,word_count),data=zip(every.Author,every.Summary,every.Title,every.date_crawled,every.date_published,every.full_text,every.img,every.news_source,every.id))


@app.route('/view/',methods = ['GET','POST'])
def view():
    search = request.args.get('key')
    index_name = request.args.get('index')
    
    every = display_data(search, index_name)
    
    res = make_response(render_template('view.html',data=zip(every.Author,every.Summary,every.Title,every.date_crawled,every.date_published,every.full_text,every.img,every.news_source,every.id)))
    try:
        if len(request.cookies.get('visited')) > 0:
            store = request.cookies.get('visited') + ',' + search
            res.set_cookie('visited',store)
        else:
            store= search
            res.set_cookie('visited',store)
    except:
        store= search
        res.set_cookie('visited',store)

    # print(request.cookies.get('visited'))
    return res

@app.route('/saveindex/',methods=['GET','POST'])
def save_index():
    index = get_index()

    if request.method=='POST':
        articles = request.form.getlist('articles')
        keywords = request.form['keywords']
        keywords = keywords.split(',')
        
        for i in range(keywords.count('')):
            keywords = keywords.remove('')
        
        session['val'] = {'articles':articles,'keyword':keywords}
      

        # print(session['val'])
        return (redirect(url_for('home')))

    return render_template('saveindex.html',index=zip(index['indices'], index['total']))

@app.route('/addindex/',methods=['GET','POST'])
def add_index():
    index = get_index()

    if request.method=='POST':
        try:
            articles = request.form.getlist('articles')
            keywords = request.form['keywords']
            keywords = keywords.split(',')
            
            for i in range(keywords.count('')):
                keywords = keywords.remove('')
            
            # print(articles,keywords)
            if len(articles)>0:
                for i in articles:
                    if  i !=None:
                        session['val']['articles'].append(i)
            if keywords !=None:
                for j in keywords:
                    session['val']['keyword'].append(j)
        except Exception as e:
            # print(e)
            articles = request.form.getlist('articles')
            keywords = request.form['keywords']
            keywords = keywords.split(',')
            
            for i in range(keywords.count('')):
                keywords = keywords.remove('')
            
            session['val'] = {'articles':articles,'keyword':keywords}
            
        session['val'] = session['val']
        # print('After Adding',session['val'])
        return (redirect(url_for('home')))

    return render_template('saveindex.html',index=zip(index['indices'], index['total']))

@app.route('/', methods = ['GET','POST'])
def login():
    if request.method=='POST':
     
        if request.form['username'] =='admin' and request.form['pass']=='12345':
            return redirect(url_for('save_index'))
    return render_template('login.html')

@app.route('/clear/', methods = ['GET','POST'])
def clear():
    res= make_response(redirect(url_for('home')))
    res.set_cookie('visited','')
    return res

@app.route('/clearsession/')
def clearsession():
    session.clear()
    return redirect(url_for('home'))

if __name__=='__main__':
        app.run(debug=False)