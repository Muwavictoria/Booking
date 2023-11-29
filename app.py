from app import app
from app.home.routes import home
from app.user.routes import user
from app.admin.routes import admin
from app.accounts.routes import auth,create_super_admin
from app.booking.routes import booking








# filters.py

import base64

def base64_encode(data):
    return base64.b64encode(data).decode('utf-8')


# Initialize Flask-Login
app.register_blueprint(home)
app.register_blueprint(booking)
app.register_blueprint(auth)
app.register_blueprint(admin)
app.register_blueprint(user)


app.jinja_env.filters['b64encode'] = base64_encode

if __name__ == "__main__":
    
    app.run(debug=True)

    with app.app_context():
        create_super_admin()