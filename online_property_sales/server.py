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

#email
app.config.update(
	#EMAIL SETTINGS
	MAIL_SERVER='smtp.gmail.com',
	MAIL_PORT=465,
	MAIL_USE_SSL=True,
	MAIL_USERNAME = 'AuctionWorldWideWeb@gmail.com',
	MAIL_PASSWORD = 'AuctionWorldWideWeb1!'
	)
mail = Mail(app)

# cookies
app.secret_key = "*U78u!#2@fs"

# database
db = SQLAlchemy(app)

#email server
mail = Mail(app)

# instantiate models
# initial_db()

