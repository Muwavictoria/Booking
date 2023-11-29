from flask import Blueprint, render_template, request, redirect,url_for, session
from app import mysql
from PIL import Image
from flask_login import login_required, current_user
import re, MySQLdb.cursors, io



admin = Blueprint('admin', __name__, url_prefix='/admin', template_folder='templates', static_folder='static')



@admin.route("/dashboard")
@login_required
def admin_home():
    try:
        # Connect to the database
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

        # Count of all cars
        cursor.execute('SELECT COUNT(*) AS total_cars FROM car')
        total_cars = cursor.fetchone()['total_cars']

        # Count of available cars
        cursor.execute('SELECT COUNT(*) AS available_cars FROM car WHERE status = 0')
        available_cars = cursor.fetchone()['available_cars']

        # Count of booked cars
        cursor.execute('SELECT COUNT(*) AS booked_cars FROM car WHERE status = 1')
        booked_cars = cursor.fetchone()['booked_cars']
        

        return render_template('dashboard/home_dashboard.html', total_cars=total_cars, available_cars=available_cars, booked_cars=booked_cars)

    except Exception as e:
        # Handle the exception (e.g., log the error)
        return f"An error occurred: {str(e)}"

    

# ====================================CARS============================
# Adding cars
@admin.route('/addproducts', methods=['POST','GET'])
@login_required
def add_products():
    msg = ''
    if request.method == 'POST' and 'numberplate' in request.form and 'carname' in request.form and 'brand' in request.form and 'color' in request.form and 'description' in request.form and  'price' in request.form and 'seats' in request.form and 'image' in request.files :
        numberplate = request.form['numberplate']
        carname = request.form['carname']
        brand = request.form['brand']
        color = request.form['color']
        description = request.form['description']
        price = request.form['price']
        seats = request.form['seats']
        image_file = request.files['image']

        
        if image_file:
            # Load the image using PIL
            image = Image.open(image_file)
            # if image.mode == 'RGBA':
            # # Convert the image to RGB mode
            #     image = image.convert('RGB')

            image_data = io.BytesIO()
            
            image.save(image_data,'png')  #it can change to any image format
            image_data = image_data.getvalue()
        else:
            image_data = None

        
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('INSERT INTO car VALUES (% s, % s, % s, % s, % s, % s, % s,% s,% s)', (numberplate, carname, brand, color, description, price, seats, image_data,'0' ))
        mysql.connection.commit()
        msg = 'You have successfully added products !'
        return redirect(url_for('admin.getproduct'))
    return render_template('dashboard/admin_cars.html')

# Getting cars
@admin.route('/products', methods=['POST','GET'])
@login_required
def getproduct():
    msg =""
    if request.method == 'GET':
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT `number_plate`, `car_name`, `brand`, `color`, `description`, `price`, `seats`, `image` FROM `car`')
        car = cursor.fetchall()  # Fetch all rows from the result set
        cursor.close()
        msg = 'You have successfully got products !'

        return render_template('dashboard/admin_cars.html', msg=msg, car=car,title= 'Dashboard')

    return render_template('dashboard/admin_cars.html', car=car, msg=msg)


# deleting#
@admin.route('/delete/<string:number_plate>', methods = ['GET','POST','DELETE'])
@login_required
def delete_products(number_plate):
    msg=''
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('DELETE FROM `car` WHERE number_plate=%s', (number_plate,))
    mysql.connection.commit()
    cursor.close()
    msg = 'You successfully deleted the car'

    return redirect(url_for('admin.getproduct'))
    
#updating 
@admin.route('/update/<string:number_plate>', methods=['GET', 'POST'])
@login_required
def update_car(number_plate):
    if request.method == 'POST':
        new_carname = request.form.get('new_carname')
        new_brand = request.form.get('new_brand')
        new_color = request.form.get('new_color')
        new_description = request.form.get('new_description')
        new_price = request.form.get('new_price')
        new_seats = request.form.get('new_seats')
        image_file = request.files.get('new_image')


        if image_file:
            # Load the image using PIL
            image = Image.open(image_file)
            image_data = io.BytesIO()
            image.save(image_data, 'png')  #it can change to any image format
            image_data = image_data.getvalue()
        else:
            image_data = None




        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("UPDATE car SET car_name=%s, brand=%s, color=%s, description=%s, price=%s, seats=%s, image=%s WHERE number_plate=%s",
                       (new_carname, new_brand, new_color, new_description, new_price, new_seats,image_data, number_plate))
        mysql.connection.commit()
        cursor.close()

        return redirect(url_for('admin.getproduct'))

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM car WHERE number_plate = %s", (number_plate,))
    car = cursor.fetchone()
    cursor.close()

    return render_template('dashboard/admin_cars.html', car=car)


#===================================== CRUD ADMIN START============================
@admin.route('/get_admin')
@login_required
def admins():
    try:
        # Open a cursor
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

        # Execute the query
        cursor.execute("SELECT * FROM user WHERE user_type = 'admin'")

        # Fetch all the admin users
        admins = cursor.fetchall()

        # Close the cursor
        cursor.close()

        return render_template('dashboard/admin.html', admins=admins)
    except Exception as e:
        return str(e)



#===================================== get customers ============================
@admin.route('/get_customers')
@login_required
def customers():
    try:
        # Open a cursor
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

        # Execute the query
        cursor.execute("SELECT * FROM user WHERE user_type = 'customer'")

        # Fetch all the admin users
        admins = cursor.fetchall()

        # Close the cursor
        cursor.close()

        return render_template('dashboard/customers.html', admins=admins)
    except Exception as e:
        return str(e)


# =========================================DISPLAYING BOOKED CARS======================
@admin.route('/booked_cars')
def booked_cars():
    try:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM car WHERE status = 1')
        cars = cursor.fetchall()
        return render_template('dashboard/booked_cars.html', cars=cars)

    except Exception as e:
        return f"An error occurred: {str(e)}"

    finally:
        cursor.close()



# ============================================DISPLAYING AVAILABLE CARS==========================
@admin.route('/available_cars')
def available_cars():
    try:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM car WHERE status = 0')
        cars = cursor.fetchall()
        return render_template('dashboard/available_cars.html', cars=cars)

    except Exception as e:
        return f"An error occurred: {str(e)}"

    finally:
        cursor.close()



# ==================================DISPLAYING PAYMENTS CARRIED OUT================================
@admin.route('/payments', methods=['GET'])
def display_payments():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM payments')
    payment_data = cursor.fetchall()
    cursor.close()
    
    return render_template('dashboard/payments.html', payments=payment_data)