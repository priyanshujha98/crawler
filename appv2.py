from flask import Flask,render_template,request,redirect,url_for

from dbtest import get_everything, get_index, get_data_index

app = Flask(__name__)

@app.route('/data/', methods = ['GET','POST'])
def home():
    every = get_everything()
    index = get_index()
    if request.method=='POST':
        back = request.form['article']
        every = get_data_index(back)
        return render_template('home.html', index = index,data=zip(every.Author,every.Summary,every.Title,every.date_crawled,every.date_published,every.full_text,every.img,every.news_source))
    
    return render_template('home.html', index = index,data=zip(every.Author,every.Summary,every.Title,every.date_crawled,every.date_published,every.full_text,every.img,every.news_source))

@app.route('/', methods = ['GET','POST'])
def login():
    if request.method=='POST':
     
        if request.form['username'] =='admin' and request.form['pass']=='12345':
            return redirect(url_for('home'))
    return render_template('login.html')

if __name__=='__main__':
        app.run(debug=False)