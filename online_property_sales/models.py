from flask import Flask
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from server import db, login_manager

class User(UserMixin, db.Model):
    __tablename__ = 'User'
    id = db.Column(db.Integer, primary_key = True)

    login_name = db.Column(db.String(collation='NOCASE') ,unique=True, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    password_hash = db.Column(db.String, nullable=False)
    address = db.Column(db.String(1000), nullable=False)  
    date_of_birth = db.Column(db.DateTime, nullable=False)
    phone_number = db.Column(db.String, nullable=False)

    #one-to-many
    auctionId = db.relationship('AuctionDetails', backref='seller', lazy='dynamic')
    properties = db.relationship('Property', backref='sellerID', lazy='dynamic')
    cards = db.relationship('BankDetails', backref='user', lazy='dynamic')

    #create hashed password for security
    def set_login_name(self, value):
        self.login_name=value

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
        
    def set_address(self, value):
        self.address=value

    def set_email(self, value):
        self.email=value

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
    holder_fname = db.Column(db.String(), nullable=False)
    holder_lname = db.Column(db.String(20), nullable=False)
    cvc = db.Column(db.Integer, nullable=False)
    expire_date = db.Column(db.DateTime, nullable=False)
    id_confirmation = db.Column(db.String(100), nullable=False)
    
    user_id = db.Column(db.Integer, db.ForeignKey('User.id'), nullable=False)

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

class AuctionDetails(db.Model):
    __tablename__ = 'AuctionDetails'
    id = db.Column(db.Integer, primary_key=True)
    # AuctionID = db.Column(db.String, primary_key=True)
    AuctionStart = db.Column(db.DateTime, nullable=False)
    AuctionEnd = db.Column(db.DateTime, nullable=False)
    ReservePrice = db.Column(db.Float, nullable=False)
    MinBiddingGap = db.Column(db.Float, nullable=False)

    PropertyID = db.Column(db.String, db.ForeignKey('Property.id'), unique=True, nullable=False)
    SellerID = db.Column(db.Integer, db.ForeignKey('User.id'), nullable=False)

    def __repr__(self):
        return f"AuctionDetails('{self.AuctionID}', '{self.PropertyID}', '{self.SellerID}', {self.AuctionStart}, {self.AuctionEnd}, {self.ReservePrice}, {self.MinBiddingGap})"

class Bid(db.Model):
    __tablename__ = 'Bid'
    id = db.Column(db.Integer, primary_key=True)
    BidderID = db.Column(db.Integer, db.ForeignKey('User.id'), nullable=False)
    AuctionID = db.Column(db.Integer, db.ForeignKey('AuctionDetails.id'), nullable=False)
    Amount = db.Column(db.Float, nullable=False)

class Property(db.Model):
    __tablename__ = 'Property'

    id = db.Column(db.Integer, primary_key = True)
    property_type = db.Column(db.String)
    add_unit = db.Column(db.String(100))
    add_num = db.Column(db.String(100))
    add_name = db.Column(db.String(100))
    add_suburb = db.Column(db.String(100))
    add_state = db.Column(db.String(3))
    add_pc = db.Column(db.String(4))
    #address = db.Column(db.String(1000))
    num_bedrooms = db.Column(db.Integer)
    num_parking = db.Column(db.Integer)
    num_bathrooms = db.Column(db.Integer)
    parking_features = db.Column(db.String)
    building_size = db.Column(db.Integer) #is it meant to be float?
    land_size = db.Column(db.Integer) #float?
    inspection_date = db.Column(db.DateTime)
    description = db.Column(db.String(2000))
    year_built = db.Column(db.Integer)

    #seller
    seller = db.Column(db.Integer, db.ForeignKey('User.id'))
    #one-to-one
    #backref defines the varible that the other table should call
    auctionId = db.relationship('AuctionDetails', backref='Property', uselist=False)
    #one-to-many
    photo_collection = db.relationship('Photos', backref='Property', lazy='dynamic')

    def set_property_type(self, p_type):
        self.property_type = p_type

    def set_address_unit_num(self, u_num):
        self.add_unit = u_num

    def set_address_street_num(self, s_num):
        self.add_num = s_num

    def set_address_street_name(self, s_name):
        self.add_name = s_name

    def set_address_suburb(self, suburb):
        self.add_suburb = suburb

    def set_address_state(self, state):
        self.add_state = state

    def set_address_postcode(self, pc):
        self.add_pc = pc

    def set_num_bedrooms(self, bedrooms):
        self.num_bedrooms = bedrooms

    def set_num_parking(self, parking):
        self.num_parking = parking

    def set_num_bathrooms(self, bathrooms):
        self.num_bathrooms = bathrooms

    def set_parking_features(self, features):
        self.parking_features = features

    def set_building_size(self, size):
        self.building_size = size
    
    def set_land_size(self, size):
        self.land_size = size

    def set_inspection_date(self, date):
        self.inspection_date = date

    def set_description(self, description):
        self.description = description

    def set_year_built(self, year):
        self.year_built = year

    # Might not need start

    def set_seller(self, seller):
        self.seller = seller

    def set_photo(self, image):
        self.photo_collection = image

    # Might not need end

    def __repr__(self):
        return '<Property ID at %r>' % self.id

class Photos(db.Model):
    __tablename__ = 'Photos'

    id = db.Column(db.Integer, primary_key = True)
    photo = db.Column(db.String)
    property_id = db.Column(db.Integer, db.ForeignKey('Property.id'))

    def set_photo(self, photo):
        self.photo = photo

def clear_session():
    db.session.query(User).delete()
    db.session.query(BankDetails).delete()
    db.session.query(AuctionDetails).delete()
    db.session.query(Property).delete()
    db.session.query(Photos).delete()
    db.session.commit()

def initial_db():

    # clear_session()
    db.create_all()

    u1= User(login_name='Tom123@g', email="tom@gmail.com", address='address', date_of_birth= datetime.strptime("01/01/1999","%d/%m/%Y"),phone_number='1844444444')
    u1.set_password('Tom123@g')
    u2= User(login_name='Cloudia@g', email="Couldia@gmail.com", address='address', date_of_birth= datetime.strptime("01/01/1999","%d/%m/%Y"),phone_number='1899999999')
    u2.set_password('Cloudia@g')
    bank1=BankDetails(id='5555444433331111',id_confirmation='id' ,holder_fname='Tom', holder_lname='Han',cvc=123, expire_date=datetime.strptime("12/2022","%m/%Y") ,user = u1)
    bank2 = BankDetails (id='1111222233334444',id_confirmation='id',holder_fname='Tom', holder_lname='Han', cvc=123, expire_date=datetime.strptime("12/2021","%m/%Y"), user=u1)

    db.session.add(u1)
    db.session.add(u2)
    db.session.add(bank1)
    db.session.add(bank2)

    db.session.commit()

# initial_db()

#query examples
# users= User.query.all()
# cards= BankDetails.query.all()
# for u in users:
#     print(u.id, u.login_name, u.cards.all())

#buyers and sellers all have to add extral bank details at some point, and all their attributes are the same,
#So I just treat them all as users, They just need to input the extral details at different time. 
#It is not clearified that if one user should have only 1 or more bank cards, so I treat band details as a class
#and only need to justify a user keep one or a list of bank account

#The difference is that buyers need to register initial bids for properties
#If user keeps the initial bids as an attribute, he/she has to keep a list of initial bids and cooresponding property(ID)
#Or should the property keeps a list of registered auction buyers(RAB) with their cooresponding initial bids 
