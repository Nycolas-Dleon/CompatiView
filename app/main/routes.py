from flask import Flask, render_template, url_for
from app.utils.data_manager import load_json
from app import app 

@app.route('/')
def homepage():
    return render_template('index.html')

@app.route('/selection')
def selectionpage():
    components = load_json()
    nomes = app.config["nomes"]
    return render_template('selection.html', components=components, nomes=nomes)


