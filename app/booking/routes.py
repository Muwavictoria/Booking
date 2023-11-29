from flask import Blueprint, render_template, request, redirect,url_for, session, abort,flash
import re, MySQLdb.cursors, io
from flask_login import login_user, current_user, logout_user, login_required, LoginManager, UserMixin
from app import mysql
from PIL import Image
from werkzeug.security import check_password_hash,generate_password_hash
from app import app


booking = Blueprint('booking', __name__, url_prefix='/book', template_folder='templates', static_folder='static')

@booking.route('/book_now')
@login_required
def book():
    return redirect(url_for('user.book_now'))
    
@booking.route('/book_car/<string:number_plate>', methods=['GET', 'POST'])
@login_required
def book_car(number_plate): 
    if request.method == 'POST' :
        # Get details from the form
        number_plate = request.form['number_plate_hidden']
        pickup_location = request.form['pickup_location']
        dropoff_location = request.form['dropoff_location']
        pickup_date = request.form['pickup_date']
        return_date = request.form['return_date']
        
        if current_user.is_authenticated:
            user_id = current_user.id
        else:
            # Handle the case when the user is not authenticated
            flash('You need to be logged in to book a car.', 'error')
            return redirect(url_for('auth.login'))
        
        # Check if the car is available
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM car WHERE number_plate = %s AND status = 0', (number_plate,))
        existing_car = cursor.fetchone()

        if  existing_car:
            # Mark the car as booked
            cursor.execute('UPDATE car SET status = 1 WHERE number_plate = %s', (number_plate,))
            mysql.connection.commit()

            # Insert the booking details into the bookings table
            cursor.execute('INSERT INTO bookings (booking_id, user_id, pickup_location, dropoff_location, pickup_date, return_date, number_plate) VALUES (NULL,%s, %s, %s, %s, %s, %s)',(user_id, pickup_location, dropoff_location,pickup_date,return_date, number_plate)) 
            
            flash('Car booked successfully!', 'success')
            
            # Get the booking_id of the last inserted record
            booking_id = cursor.lastrowid

            mysql.connection.commit()
            
            print("Before redirect to payments")
            return redirect(url_for('user.payments', booking_id = booking_id))

        else:
            flash('Car is not available for booking', 'error')
            return redirect(url_for('user.get_details', number_plate=number_plate))
       
    # If it's a GET request, show the booking form
    #  If it's a GET request, show the booking form with read-only car details
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM car WHERE number_plate = %s', (number_plate,))
    car = cursor.fetchone()
    cursor.close()

    return render_template('user.get_details', car=car, number_plate=number_plate)
    
@booking.route('/complete_payment/<string:booking_id>', methods=['POST'])
@login_required
def complete_payment(booking_id):
    if request.method == 'POST':
        # Retrieve form data
        booking_id = request.form.get('booking_id')
        card_number = request.form.get('card_number')
        expiration_date = request.form.get('expiration_date')
        cvv = request.form.get('cvv')
        billing_address = request.form.get('billing_address')


        # Check if the booking_id exists in the bookings table
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM bookings WHERE booking_id = %s', (booking_id,))
        existing_booking = cursor.fetchone()
        cursor.close()

        if not existing_booking:
            flash('Invalid booking_id. Please provide a valid booking_id.', 'error')
            return redirect(url_for('booking.index'))

        # Continue with payment insertion
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(
                'INSERT INTO payments (booking_id, card_number, expiration_date, cvv, billing_address, user_id) VALUES (%s, %s, %s, %s, %s, %s)',
                (booking_id, card_number, expiration_date, cvv, billing_address, current_user.id)
            )
        mysql.connection.commit()
        cursor.close()
        flash('Payment successful!', 'success')
        return redirect(url_for('booking.payment_confirmation'))  # Redirect to a confirmation page
        
            

    # Handle cases where the request method is not POST
    flash('Invalid request method.', 'error')
    return redirect(url_for('booking.index'))  # Redirect to a relevant page

@booking.route('/complete')
@login_required
def payment_confirmation():
    return redirect(url_for('user.user_profile'))