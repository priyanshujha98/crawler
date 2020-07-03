from flask import Flask,render_template,request,redirect,url_for, make_response, jsonify

from dbtest import get_everything, get_index, get_data_index, display_data, get_data,get_only_data


from tryv1 import grab_data

app = Flask(__name__)

@app.route('/data/', methods = ['GET','POST'])
def home():
    every = get_everything()
    index = get_index()
    if request.method=='POST':
        back = request.form['article']
        news_search = request.form['news_search']
        news_search = news_search.split(',')
        
        for i in range(news_search.count('')):
            news_search.remove('')
        
        if back !='':
            if news_search =="":
                every = get_data_index(back)
            elif news_search !="":
                every = get_data(news_search, back)
        elif  back =='':
            if len(news_search)== 0:
                every = get_everything()
                # return redirect(url_for('home'))
            elif len(news_search.remove('') )!=0:
                every = get_only_data(news_search)
        
        already_seen = request.cookies.get('visited')
        already_seen = already_seen.split(',')
        every.reset_index(drop=True,inplace=True)
        for i in range(len(every.id)):
            if every.id[i] in already_seen:
                every = every.drop([i],axis= 0)
                
        print(len(every))
        return render_template('home.html', index = index,data=zip(every.Author,every.Summary,every.Title,every.date_crawled,every.date_published,every.full_text,every.img,every.news_source,every.id))
    already_seen = request.cookies.get('visited')
    already_seen = already_seen.split(',')
    print('Before ',len(every))
    every.reset_index(drop=True,inplace=True)
    for i in range(len(every)):
        if every['id'][i] in already_seen:
            print(every['id'][i])
            every = every.drop([i],axis= 0)
    print('After',len(every))
    return render_template('home.html', index = index,data=zip(every.Author,every.Summary,every.Title,every.date_crawled,every.date_published,every.full_text,every.img,every.news_source,every.id))

@app.route('/update/')
def update():
    grab_data()
    return  redirect(url_for('home'))

@app.route('/view/',methods = ['GET','POST'])
def view():
    search = request.args.get('key')
    index_name = request.args.get('index')
    
    every = display_data(search, index_name)
    
    res = make_response(render_template('view.html',data=zip(every.Author,every.Summary,every.Title,every.date_crawled,every.date_published,every.full_text,every.img,every.news_source,every.id)))
    if len(request.cookies.get('visited')) > 0:
        store = request.cookies.get('visited') + ',' + search
        res.set_cookie('visited',store)
    else:
        store= search
        res.set_cookie('visited',store)
    print(request.cookies.get('visited'))
    return res


@app.route('/', methods = ['GET','POST'])
def login():
    if request.method=='POST':
     
        if request.form['username'] =='admin' and request.form['pass']=='12345':
            return redirect(url_for('home'))
    return render_template('login.html')

@app.route('/clear/', methods = ['GET','POST'])
def clear():
    res= make_response(redirect(url_for('home')))
    res.set_cookie('visited','')
    return res

if __name__=='__main__':
        app.run(debug=False)