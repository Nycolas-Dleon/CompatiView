from flask import Flask, render_template, url_for
from app import app 

@app.route('/')
def homepage():
    return render_template('index.html')

@app.route('/selection')
def selectionpage():
    return render_template('selection.html')


