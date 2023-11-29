from flask import Blueprint, render_template, request, redirect,url_for, session
from app import mysql
from flask_login import login_required, current_user
import re, MySQLdb.cursors



user = Blueprint('user', __name__, url_prefix='/user', template_folder='templates', static_folder='static')


@user.route('/home')
@login_required
def user_home():
    return render_template('user_home.html')


@user.route('/details/<string:number_plate>',  methods=('GET','POST'))
@login_required
def get_details(number_plate):
    if current_user.user_type == 'super_admin':
        return redirect(url_for('auth.login'))
    else:
        if request.method == 'GET':

            query = "SELECT * FROM car WHERE number_plate = %s"

            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute(query, (number_plate,))
            car = cursor.fetchone()  # Fetch the first row from the result set
            cursor.close()
            
            return render_template('view_more.html', car=car)
    return render_template('view_more.html')



@user.route('/cars', methods=('GET','POST'))
@login_required
def user_cars():
    if not current_user.is_authenticated:
        print("User not authenticated. Redirecting to login.")
        return redirect(url_for('auth.login'))
    if request.method == 'GET':

        page = request.args.get('page', 1, type=int)
        limit = request.args.get('limit', 9, type=int)
        start = limit * (page - 1)
        end = start + limit

    
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM car WHERE status = 0 LIMIT %s, %s', (start, end))
        car = cursor.fetchall()  # Fetch all rows from the result set
        cursor.execute('SELECT COUNT(*) FROM car')
    
        total_cars_result = cursor.fetchone()
        if total_cars_result is not None:
            total_cars = total_cars_result['COUNT(*)']
        else:
            total_cars = 0

        pagination = {'table': False, 'prev': start > 0, 'next': end < total_cars}

        cursor.close()

        return render_template('cars.html', car=car, pagination=pagination, page=page)
    return render_template('cars.html')




@user.route('/book')
def book_now():
    
    return render_template('book_now.html')

@user.route('/payments/<string:booking_id>')
def payments(booking_id):

    return render_template('payments.html', booking_id=booking_id)

@user.route('/profile', methods=['GET'])
@login_required
def user_profile():
    if request.method == 'GET':
        user_id = current_user.id

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('''
                            SELECT b.*, c.* 
                            FROM bookings b 
                            INNER JOIN car c ON b.number_plate = c.number_plate 
                            WHERE b.user_id=%s
                        ''', (user_id,))
        bookings = cursor.fetchall()
        cursor.close()
        
        # Query to get user details
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM user WHERE user_id=%s', (user_id,))
        user = cursor.fetchone()
        cursor.close()

        return render_template('user_profile.html', bookings=bookings, user=user)

    return render_template('user_profile.html')
