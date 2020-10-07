from flask import Flask
from flask_login import LoginManager,UserMixin
from flask_sqlalchemy import SQLAlchemy
from datetime import date

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database_user.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

# app.secret_key = 'very-secret-123'
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

db = SQLAlchemy(app)

#buyers and sellers all have to add extral bank details as some point, and all their attributes are the same,
#So I just treat them all as users, They just need to input the extral details at different time. 
#It is not clearified that if one user should have only 1 or more bank cards, so I treat band details as a class
#and only need to justify a user keep one or a list of bank account

#The difference is that buyers need to register initial bids for properties
#If user keeps the initial bids as an attribute, he/she has to keep a list of initial bids and cooresponding property(ID)
#Or should the property keeps a list of registered auction buyers(RAB) with their cooresponding initial bids 

class User(UserMixin, db.Model):
    __tablename__ = 'User'
    id = db.Column('login_name',db.String, primary_key = True)
    password = db.Column(db.String(20))
    address = db.Column(db.String(1000))  
    date_of_birth = db.Column(db.Date)

    def __repr__(self):
        return '<User %r>' % self.id

class BankDetails(db.Model):
    __tablename__ = 'BankDetails'

    id = db.Column("card_number",db.String, primary_key=True)
    phone_number = db.Column(db.String)
    id_confirmation = db.Column(db.String(20))
    holder_fname = db.Column(db.String())
    holder_lname = db.Column(db.String(20))
    cvc = db.Column(db.Integer)
    expire_date = db.Column(db.Date)

    login_name = db.Column(db.String, db.ForeignKey('User.login_name'))


    def __repr__(self):
        return '<BankDetails %r>' % self.id

db.create_all()

#samples

u1= User(id='Tom123', password='psw', address='address', date_of_birth= date(2000,12,12))
u2= User(id='Cloudia', password='psw', address='address', date_of_birth= date(1999,1,1))
bank1=BankDetails(id='5555444433331111',phone_number='1530009999',id_confirmation='id',holder_fname='Tom', holder_lname='Han',cvc=123, expire_date=date(2022,12,1) ,login_name='Tom123')
db.session.add(u1)
db.session.add(u2)
db.session.add(bank1)

db.session.commit()