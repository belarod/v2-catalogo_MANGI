from flask import Flask, request, render_template, session, redirect, url_for
from database.db import DB



app = Flask(__name__)



@app.route('/')
def index():
     return render_template('index.html')
 
@app.route('/login')
def login():
    return render_template('login.html')