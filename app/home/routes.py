from flask import Blueprint, render_template
from PIL import Image

home = Blueprint('home', __name__, template_folder='templates', static_folder='static')


@home.route("/")
@home.route("/home")
def home_page():
    username = ''
    return render_template("homepage/index.html")


@home.route('/about')
def about():
    return render_template('homepage/about.html')

