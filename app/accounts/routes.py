from flask import Blueprint, render_template, request, redirect,url_for, session, abort,flash
import re, MySQLdb.cursors, io
from flask_login import login_user, current_user, logout_user, login_required, LoginManager,UserMixin
from functools import wraps
from app import mysql,login_manager
from PIL import Image
from werkzeug.security import check_password_hash,generate_password_hash
from app import app


auth = Blueprint('auth', __name__, url_prefix='/auth', template_folder='templates', static_folder='static')


# user class
class User:
    def __init__(self, user_id, username, user_type, password_hash, email, image):
        self.id = user_id
        self.username = username
        self.user_type = user_type
        self.password_hash = password_hash
        self.email = email
        self.image = image
        if user_type == 'super_admin' or user_type == 'admin':
            self.redirect_route = 'admin.admin_home'
        else:
            self.redirect_route = 'user.user_cars'

    def set_password(self, password):
        self.password_hash = generate_password_hash(password, method='pbkdf2:sha256')

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
        
    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)  # Replace with your logic
    

# initiating a login manager user_loader that loads a specific user   
@login_manager.user_loader
def load_user(user_id):
    # Load a user from the user ID
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM user WHERE user_id = %s', (user_id,))
    user_data = cursor.fetchone()
    cursor.close()

    if user_data:
        user = User(
            user_data['user_id'], 
            user_data['username'], 
            user_data['user_type'], 
            user_data['email'], 
            user_data['image'], 
            user_data['password_hash'] if 'password_hash' in user_data else None,
            )

        if user.user_type == 'admin':
            user.redirect_route = 'admin.admin_home'
        elif user.user_type == 'super_admim':
            user.redirect_route = 'admin.admin_home'   
        else:
            user.redirect_route = 'user.user_cars'
        return user
    else:
        return None

# creating a super_admin
def create_super_admin():
    super_admin_username = 'admin'
    super_admin_password = 'super'
    email='admin@gmail.com'

    # Use the application context to access the database
    with app.app_context():
        # Check if the super admin already exists
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM user WHERE username = %s', (super_admin_username,))
        existing_super_admin = cursor.fetchone()
        cursor.close()

        if not existing_super_admin:
            # If not, create the super admin
            hashed_password = generate_password_hash(super_admin_password, method='pbkdf2:sha256')

            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute(
                'INSERT INTO user (username, password, user_type, email) VALUES (%s, %s, %s, %s)',
                (super_admin_username, hashed_password, 'super_admin', email))
            mysql.connection.commit()
            cursor.close()

            return 'Super admin created successfully!'
        else:
            return 'Super admin already exists!'

    

#Logining in the users, admin and the customer
@auth.route("/login", methods=['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM user WHERE username = %s', (username,))

        user = cursor.fetchone()

       
        if user and check_password_hash(user['password'], password):
            user_obj = User(user['user_id'], user['username'], user['user_type'])
            login_user(user_obj)
            # Redirect to the appropriate route based on user type
            print(user_obj.redirect_route)  # Add this line for debugging
            return redirect(url_for(user_obj.redirect_route))
    
        else:
            msg = 'Incorrect username/password!'

    return render_template("login.html", msg=msg)

# registering customer users 
@auth.route("/register", methods=['GET', 'POST'])
def register():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']

        # Check if the current user is a super admin
        if current_user.is_authenticated and current_user.user_type == 'super_admin':
            user_type = request.form.get('user_type', 'customer')
        else:
            user_type = 'customer'

        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM user WHERE username = %s', (username,))

        existing_user = cursor.fetchone()

        if existing_user:
            msg = 'Username already exists. Please choose a different one.'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address!'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers!'
        elif not username or not password or not email:
            msg = 'Please fill out the form!'
        else:
            cursor.execute('INSERT INTO user (username, password,email, user_type) VALUES (%s, %s,%s, %s)', (username, hashed_password, email, user_type))
            mysql.connection.commit()
            return redirect(url_for('auth.login'))
    elif request.method == 'POST':
        msg = 'Please fill out the form!'

    return render_template("register.html", msg=msg)

# logout users
@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

#creating and admin by the super_admin
@auth.route("/create_admin", methods=['POST'])
@login_required
def create_admin():
    # Check if the current user is a super admin
    if current_user.user_type != 'super_admin':
        abort(403)  # Only super admins can create other admins

    # Extract form data for creating a new admin
    username = request.form.get('username')
    password = request.form.get('password')
    email = request.form.get('email')
    image_file = request.files.get('image')
    # Extract other relevant details as needed

    # Hash the password
    hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

    # image
    if image_file:
        # Load the image using PIL
        image = Image.open(image_file)

        image_data = io.BytesIO()
            
        image.save(image_data,'png')  #it can change to any image format
        image_data = image_data.getvalue()
    else:
        image_data = None


    # Perform the database insertion for the new admin
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('INSERT INTO user (user_id, username, password, email, user_type, image) VALUES (NULL,%s, %s, %s, %s, %s)', (username, hashed_password, email,'admin', image_data))
    mysql.connection.commit()
    cursor.close()

    flash('Admin created successfully!', 'success')
    return redirect(url_for('admin.admins'))  # Redirect back to the dashboard


# checking if current user is super_admin
def superuser_required(view_func):
    @wraps(view_func)
    def wrapper(*args, **kwargs):
        # Check if the current user is a super admin
        if not current_user.is_authenticated or current_user.user_type != 'super_admin':
            return redirect(url_for('auth.login'))
        return view_func(*args, **kwargs)
    return wrapper

# getting admins
@auth.route("/admin_dashboard")
@login_required
@superuser_required
def admin_dashboard():
    # Retrieve a list of all admins
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM user WHERE user_type = %s', ('admin',))
    admins = cursor.fetchall()
    cursor.close()

    return render_template("admin_dashboard.html", admins=admins)



#edittig the admins
@auth.route("/edit_admin/<int:admin_id>", methods=['GET', 'POST'])
@login_required
@superuser_required
def edit_admin(admin_id):
    # Retrieve admin details
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM user WHERE user_id = %s', (admin_id,))
    admin = cursor.fetchone()
    cursor.close()

    if not admin:
        abort(404)  # Admin not found

    if request.method == 'POST':
        # Update admin details based on the form data
        username = request.form.get('username')
        email= request.form.get('email')
        image_file = request.files.get('image')

        # Hash the password
        # hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
         # image
        if image_file:
            # Load the image using PIL
            image = Image.open(image_file)

            image_data = io.BytesIO()
                
            image.save(image_data,'png')  #it can change to any image format
            image_data = image_data.getvalue()
        else:
            image_data = None

        # Perform the database update for the admin
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('UPDATE user SET username=%s, email=%s, image=%s WHERE user_id=%s', (username, email,image_data, admin_id))
        mysql.connection.commit()
        cursor.close()

        flash('Admin updated successfully!', 'success')
        return redirect(url_for('admin.admins'))  # Redirect back to the admin dashboard

    return render_template("edit_admin.html", admin=admin)

#deleting the admin
@auth.route("/delete_admin/<int:admin_id>", methods=['POST', 'GET'])
@login_required
@superuser_required
def delete_admin(admin_id):
    # Perform the database deletion for the admin
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('DELETE FROM user WHERE user_id=%s', (admin_id,))
    mysql.connection.commit()
    cursor.close()

    flash('Admin deleted successfully!', 'success')
    return redirect(url_for('admin.admins'))

#editting user_details, password, username, image,email
@auth.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    if request.method == 'POST':
        # Get form data
        new_username = request.form.get('username')
        new_email = request.form.get('email')
        new_password = request.form.get('password')
        new_image = request.files.get('image')

        # Update username if provided
        if new_username:
            current_user.username = new_username

        # Update email if provided
        if new_email:
            current_user.email = new_email

        
        # Update password if provided
        if new_password:
            if current_user.check_password(new_password):
                flash('New password must be different from the current password', 'danger')
                return redirect(url_for('auth.edit_profile'))
            current_user.set_password(new_password)

        # Update image if provided
        if new_image:
            image = Image.open(new_image)
            image_data = io.BytesIO()
            image.save(image_data, 'jpeg')  # Adjust based on your image format
            current_user.image = image_data.getvalue()

        # Commit changes to the database
        cursor = mysql.connection.cursor()
        cursor.execute('UPDATE user SET username=%s, email=%s, password=%s, image=%s WHERE user_id=%s',
                       (current_user.username, current_user.email, current_user.password_hash, current_user.image, current_user.id))
        mysql.connection.commit()
        cursor.close()

        flash('Profile updated successfully!', 'success')
        return redirect(url_for('user.user_profile'))
    
    flash('Profile not updated successfully!', 'failure')
    return redirect(url_for('user.user_profile'))
