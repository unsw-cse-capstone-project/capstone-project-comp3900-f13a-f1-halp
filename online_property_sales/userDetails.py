from flask import Flask
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from server import db, login_manager

class User(UserMixin, db.Model):
    __tablename__ = 'User'
    id = db.Column(db.Integer, primary_key = True)

    login_name = db.Column(db.String, unique=True)
    password_hash = db.Column(db.String)
    address = db.Column(db.String(1000))  
    date_of_birth = db.Column(db.DateTime)
    phone_number = db.Column(db.String)
    cards = db.relationship('BankDetails', backref='author', lazy='dynamic')
    #create hashed password for security
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
        
    def set_address(self, value):
        self.address=value

    def set_date_of_birth(self, value):
        self.date_of_birth=value
    
    def set_phone_number(self, value):
        self.phone_number=value

    def __repr__(self):
        return '<User %r>' % self.login_name


@login_manager.user_loader
def load_user(id):
    return User.query.get(id)

class BankDetails(db.Model):
    __tablename__ = 'BankDetails'
    id = db.Column("card_number",db.String, primary_key=True)
    holder_fname = db.Column(db.String())
    holder_lname = db.Column(db.String(20))
    cvc = db.Column(db.Integer)
    expire_date = db.Column(db.DateTime)
    id_confirmation = db.Column(db.String(100))
    user_id = db.Column(db.Integer, db.ForeignKey('User.id'))

    def set_fname(self,value):
        self.holder_fname=value

    def set_lname(self,value):
        self.holder_lname=value

    def set_cvc(self,value):
        self.cvc=value

    def set_expire_date(self,value):
        self.expire_date=value

    def set_id_confirmation(self,value):
        self.id_confirmation=value

    def __repr__(self):
        return '<BankDetails %r>' % self.id


def clear_session():
    db.session.query(User).delete()
    db.session.query(BankDetails).delete()
    db.session.commit()

class AuctionDetails(db.Model):
    AuctionID = db.Column(db.String, primary_key=True)
    PropertyID = db.Column(db.String, unique=True, nullable=False)
    SellerID = db.Column(db.String, nullable=False)
    AuctionStart = db.Column(db.DateTime, nullable=False)
    AuctionEnd = db.Column(db.DateTime, nullable=False)
    ReservePrice = db.Column(db.Float, nullable=False)
    MinBiddingGap = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f"AuctionDetails('{self.AuctionID}', '{self.PropertyID}', '{self.SellerID}', {self.AuctionStart}, {self.AuctionEnd}, {self.ReservePrice}, {self.MinBiddingGap})"

# clear_session()
# db.create_all()

# u1= User(login_name='Tom123', address='address', date_of_birth= datetime.strptime("01/01/1999","%d/%m/%Y"),phone_number='1844444444')
# u1.set_password('123')
# u2= User(login_name='Cloudia', address='address', date_of_birth= datetime.strptime("01/01/1999","%d/%m/%Y"),phone_number='1899999999')
# u2.set_password('123')
# bank1=BankDetails(id='5555444433331111',id_confirmation='id' ,holder_fname='Tom', holder_lname='Han',cvc=123, expire_date=datetime.strptime("12/2022","%m/%Y") ,author = u1)
# bank2 = BankDetails (id='1111222233334444',id_confirmation='id',holder_fname='Tom', holder_lname='Han', cvc=123, expire_date=datetime.strptime("12/2021","%m/%Y"), author=u1)

# db.session.add(u1)
# db.session.add(u2)
# db.session.add(bank1)
# db.session.add(bank2)

# db.session.commit()

# users= User.query.all()
# cards= BankDetails.query.all()
# for u in users:
#     print(u.id, u.login_name, u.cards.all())

#buyers and sellers all have to add extral bank details as some point, and all their attributes are the same,
#So I just treat them all as users, They just need to input the extral details at different time. 
#It is not clearified that if one user should have only 1 or more bank cards, so I treat band details as a class
#and only need to justify a user keep one or a list of bank account

#The difference is that buyers need to register initial bids for properties
#If user keeps the initial bids as an attribute, he/she has to keep a list of initial bids and cooresponding property(ID)
#Or should the property keeps a list of registered auction buyers(RAB) with their cooresponding initial bids 
