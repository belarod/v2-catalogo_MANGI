from flask import Flask, redirect, url_for
from flask import render_template
from flask import request
from flask import session
from database.db import DB
from app.app import App


my_db = DB('example.db')
appFlask = Flask(__name__)
appFlask.secret_key = 'secret'




@appFlask.route('/')
def index():
     return render_template('index.html')
 
@appFlask.route('/login', methods=['GET', 'POST'])
def login():
     if request.method == 'POST':
          email = request.form['email']
          password = request.form['password']
          restaurant= DB.login_restaurant(my_db, email= email, password= password)
          
          if restaurant is not None:
               session['email'] = request.form['email']
               return redirect(url_for('order_pannel'))
          else:
               return render_template('login.html', error="Invalid email or password.")
     return render_template('login.html') 

@appFlask.route('/order_pannel', methods=['GET', 'POST'])
def order_pannel():
     return render_template('order_pannel.html')  
           
if __name__ == '__main__':
    appFlask.run(debug=True)