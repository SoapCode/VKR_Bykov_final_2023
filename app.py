import flask
from flask import render_template
import pickle
from wtforms import StringField
from category_encoders import TargetEncoder
from wtforms.validators import InputRequired
import pandas as pd

app = flask.Flask(__name__, template_folder = 'templates')

@app.route('/', methods = ['POST', 'GET'])

@app.route('/index', methods = ['POST', 'GET'])
def main():
    with open('all_tags', 'rb') as f:
        all_tags = pickle.load(f)
    with open('knnpickle_file', 'rb') as f:
        loaded_model = pickle.load(f)
    with open('encoder', 'rb') as f:
        encoder = pickle.load(f)

    if flask.request.method == 'GET':
        return render_template('main.html', all_tags=all_tags)
    
    if flask.request.method == 'POST':
        tag1 = flask.request.form['tag1']
        tag2 = flask.request.form['tag2']
        tag3 = flask.request.form['tag3']

        tags = pd.DataFrame([[tag1, tag2, tag3]], columns=['tag1', 'tag2', 'tag3'])
        
        if tags.nunique(axis=1).sum() != 3:
            return render_template('main.html', result = "Разрешены только уникальные значения для каждого тага", all_tags=all_tags)
        else:
            tags = encoder.transform(tags)

        print(loaded_model.predict(tags)[0])
        result = 'Ваша игра будет успешной.' if loaded_model.predict(tags)[0] == 1 else 'Ваша игра не будет успешной.'

        return render_template('main.html', result = result, all_tags=all_tags)
    
if __name__ == '__main__':
    app.run()