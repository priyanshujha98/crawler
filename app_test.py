from flask import Flask,render_template,request,redirect,url_for, make_response, jsonify, session

from dbtest import get_everything, get_index, get_data_index, display_data, get_data,get_only_data, get_data_count, get_type


app = Flask(__name__)

app.secret_key = 'super secret key'

@app.route('/academics/')
def academics():
    every = get_data_index('pubmed')
    every = every.append(get_data_index('arxiv'))
    every = every.to_html()
    return every


if __name__=='__main__':
        app.run(debug=False)