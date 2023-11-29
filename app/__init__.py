from  flask import Flask, request, flash, redirect, url_for
from flask_mysqldb import MySQL
from flask_login import LoginManager, current_user
from flask_apscheduler import APScheduler
from datetime import datetime, timedelta
import re, MySQLdb.cursors


app = Flask(__name__)

app.secret_key = 'your secret key'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'car_app'

login_manager = LoginManager(app)
login_manager.login_view = 'auth.login'  # 'auth.login' should match your login route
mysql = MySQL(app)


scheduler = APScheduler()
scheduler.init_app(app)
scheduler.start()

@app.before_request
def check_user_role():
    # Check if the user is logged in
    if current_user.is_authenticated:
        # Define the restricted views
        restricted_views = ['admin.admin_home']

        # Check if the user is trying to access a restricted view
        if request.endpoint and request.endpoint in restricted_views:
            flash('You do not have permission to access this page.', 'warning')
            return redirect(url_for(current_user.redirect_route))


# Define the job to check and update bookings
@scheduler.task('interval', id='check_bookings', minutes=30)
def check_bookings():
    with app.app_context():
        # Connect to the database
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

        # Get current time
        current_time = datetime.utcnow()

        # Check and update bookings
        cursor.execute('SELECT * FROM bookings')
        bookings = cursor.fetchall()

        for booking in bookings:
            booking_time = booking['booking_time']
            payment_time = booking['payment_time']
            car_id = booking['car_id']

            # Calculate time difference
            booking_duration = timedelta(minutes=30)
            time_difference = current_time - booking_time

            if time_difference > booking_duration and not payment_time:
                # Unbook the car if not paid after 30 minutes
                cursor.execute('UPDATE bookings SET status=%s WHERE car_id=%s', ('unbooked', car_id))

            # Check if booking duration is over
            if booking_time + booking_duration < current_time:
                # Set the car status to available
                cursor.execute('UPDATE cars SET status=%s WHERE id=%s', ('available', car_id))

        # Commit changes and close the cursor
        mysql.connection.commit()
        cursor.close()



  