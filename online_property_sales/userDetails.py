from flask import Flask
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from server import db

#buyers and sellers all have to add extral bank details as some point, and all their attributes are the same,
#So I just treat them all as users, They just need to input the extral details at different time. 
#It is not clearified that if one user should have only 1 or more bank cards, so I treat band details as a class
#and only need to justify a user keep one or a list of bank account

#The difference is that buyers need to register initial bids for properties
#If user keeps the initial bids as an attribute, he/she has to keep a list of initial bids and cooresponding property(ID)
#Or should the property keeps a list of registered auction buyers(RAB) with their cooresponding initial bids 

class User(UserMixin, db.Model):
    __tablename__ = 'User'
    id = db.Column(db.Integer, primary_key = True)

    login_name = db.Column(db.String, unique=True)
    password = db.Column(db.String(20))
    address = db.Column(db.String(1000))  
    date_of_birth = db.Column(db.DateTime)

    cards = db.relationship('BankDetails', backref='author', lazy='dynamic')

    def __repr__(self):
        return '<User %r>' % self.login_name

class BankDetails(db.Model):
    __tablename__ = 'BankDetails'
    id = db.Column("card_number",db.String, primary_key=True)

    phone_number = db.Column(db.String)
    id_confirmation = db.Column(db.String(20))
    holder_fname = db.Column(db.String())
    holder_lname = db.Column(db.String(20))
    cvc = db.Column(db.Integer)
    expire_date = db.Column(db.Date)

    user_id = db.Column(db.Integer, db.ForeignKey('User.id'))


    def __repr__(self):
        return '<BankDetails %r>' % self.id


def clear_session():
    db.session.query(User).delete()
    db.session.query(BankDetails).delete()
    db.session.commit()


# clear_session()

# u1= User(login_name='Tom123', password='psw', address='address', date_of_birth= datetime(2000,12,12))
# u2= User(login_name='Cloudia', password='psw', address='address', date_of_birth= datetime(1999,1,1))
# bank1=BankDetails(id='5555444433331111',phone_number='1530009999',id_confirmation='id',holder_fname='Tom', holder_lname='Han',cvc=123, expire_date=datetime(2022,12,1) ,author = u1)
# bank2 = BankDetails (id='1111222233334444', phone_number='1530009999', id_confirmation='id', holder_fname='Tom', holder_lname='Han', cvc=123, expire_date=datetime(2025,10,1), author=u1)

# db.session.add(u1)
# db.session.add(u2)
# db.session.add(bank1)
# db.session.add(bank2)

# db.session.commit()

# users= User.query.all()
# cards= BankDetails.query.all()
# for u in users:
#     print(u.id, u.login_name, u.cards.all())