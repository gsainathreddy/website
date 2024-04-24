# app/__init__.py
from flask import Flask
#from .config import Config
from flask_mysqldb import MySQL
from flask_login import LoginManager
from flask_mail import Mail

#from app.user import get_user  # Move the import statement here

#from app.routes import bp as routes_bp  # Specify unique names


app = Flask(__name__)
#app.config.from_object(Config)
app.config['SECRET_KEY'] = 'your secret key'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Sainath@123'
app.config['MYSQL_DB'] = 'login1'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'




app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


# Initialize Flask-Mail
mail = Mail(app)

mysql = MySQL(app)

login_manager = LoginManager(app)

login_manager.login_view = 'routes.login'


@login_manager.user_loader
def load_user(user_id):
    return get_user(user_id)

from app.user import get_user  # Move the import statement here

from app.routes import bp as routes_bp  # Specify unique names


app.register_blueprint(routes_bp)
