from flask import Flask,request,render_template

from dbtest import get_data

app = Flask(__name__)

@app.route('/',methods = ['POST','GET'])
def home():
    if request.method =='POST':
        search = request.form['search']
        data = get_data(search)
        try:
            return render_template('try.html', data = zip(data['Author'].values,data['Title'].values))
        except:
            return render_template('try.html')

    return render_template('try.html')


if __name__=='__main__':
    app.run(debug = False)