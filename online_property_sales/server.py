from flask import Flask
from flask_login import LoginManager,UserMixin
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
import os
# from models import *

# instantiate app object
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Please login to access this page'
login_manager.login_message_category = 'warning'

# cookies
app.secret_key = "*U78u!#2@fs"

# database
db = SQLAlchemy(app)

#email server
mail = Mail(app)

app.config['MAIL_SERVER']='vps19984.inmotionhosting.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'comp3900@minamamoto.cloud'
app.config['MAIL_PASSWORD'] = 'COMP3900F1-HALP'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_DEFAULT_SENDER '] = 'comp3900@minamamoto.cloud'

# instantiate models
# initial_db()

