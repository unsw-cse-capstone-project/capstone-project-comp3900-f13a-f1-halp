from flask import Flask
from flask_login import LoginManager,UserMixin
from flask_sqlalchemy import SQLAlchemy
# import login manager
# import models
# from models.bidSystem import bidApp

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


# instantiate models
# initial_db()

