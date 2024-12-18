from flask import Flask, redirect, url_for
from flask import render_template
from flask import request
from flask import session
from database.db import DB
from app.app import App
import os



my_db = DB('example.db')
appFlask = Flask(__name__)
appFlask.secret_key = os.urandom(24)




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
               session['pk'] = restaurant.pk
               return redirect(url_for('order_pannel'))
          else:
               return render_template('login.html', error="Invalid email or password.")
     return render_template('login.html') 

@appFlask.route('/order_pannel', methods=['GET', 'POST'])
def order_pannel():
     if 'pk' not in session:
        return redirect(url_for('login'))
     
     orders = DB.get_orders_id_name(my_db, session['pk'])
     
     if request.method == 'POST':
          action = request.form.get('action')
          order_id = request.form.get('order_id')
          
          if action in ['1', '2', '3', '4']:
               DB.update_status_order(my_db, order_id, action) 
     
     ####################
     
     order_info = []
     for order in orders:
          order_id = order[0]
          client = order[1]
          
          status_raw = DB.get_order_status(my_db, order_id)
          status = status_raw[0]
          
          products = DB.get_products_and_quantity_from_order(my_db, order_id)
          product_details = [{"name": product[0], "quantity": product[1]} for product in products]
          
          order_info_dic = {
               "order_id": order_id,
               "client": client,
               "product_details": product_details,
               "status": status
          }
          order_info.append(order_info_dic)
     return render_template('order_pannel.html', orders=order_info, user=session['pk']) 

@appFlask.route('/logout', methods=['GET', 'POST'])
def logout():
     session.pop('email', None)
     return redirect(url_for('index'))

@appFlask.route('/report', methods=['GET', 'POST'])
def report():
     if 'pk' not in session:
        return redirect(url_for('login'))
     #RESTAURANTS
     
     #1
     average_ticketRAW = DB.get_avg_ticket(my_db, session['pk']) #usar index [0], [1]  
     
     #2
     most_expensive_orderRAW = DB.get_most_expensive_order(my_db, session['pk'])
     
     #3
     biggest_order_in_quantityRAW = DB.get_biggest_order_in_quantity(my_db, session['pk'])
     
     #4
     
     #5
     most_ordered_productRAW = DB.get_most_ordered_product(my_db, session['pk'])
     
     #6
     quantity_of_products_per_statusRAW = DB.get_quantity_of_products_per_status(my_db, session['pk']) #usar index [0][0], [0][1]
     
     #ADMIN
     
     #1
     quantity_of_restaurantsRAW = DB.get_quantity_of_restaurants(my_db)
     
     quantity_of_clientsRAW = DB.get_quantity_of_clients(my_db)
     
     #2
     unique_clients_per_restaurantRAW = DB.get_unique_clients_per_restaurant(my_db)

     
     #3
     average_ticket_per_restaurantRAW = DB.get_average_ticket_per_restaurant(my_db)
     
     return render_template('report.html',
                            #RESTAURANTS
                            average_ticket=average_ticketRAW,
                            most_expensive_order=most_expensive_orderRAW,
                            biggest_order_in_quantity=biggest_order_in_quantityRAW,
                            most_ordered_product=most_ordered_productRAW,
                            quantity_of_products_per_status=quantity_of_products_per_statusRAW,
                            
                            #ADMIN
                            quantity_of_restaurants=quantity_of_restaurantsRAW,
                            quantity_of_clients=quantity_of_clientsRAW,
                            unique_clients_per_restaurant=unique_clients_per_restaurantRAW,
                            average_ticket_per_restaurant=average_ticket_per_restaurantRAW,
                            user=session['pk']) 
           

if __name__ == '__main__':
    appFlask.run(debug=True) 