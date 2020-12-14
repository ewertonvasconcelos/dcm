from app import app
from flask import render_template

@app.route('/')
def home():
   return "Data Center Manager - UFRJ 2020"


@app.route('/template')
def template():
    return render_template('home.html')


