from flask import Flask
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func, and_
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
    phone_number = db.Column(db.String,unique=True, nullable=False)
    id_confirmation = db.Column(db.String(100), nullable=True)
    #one-to-many
    auctionId = db.relationship('AuctionDetails', backref='seller', lazy='dynamic')
    properties = db.relationship('Property', backref='sellerID', lazy='dynamic')
    cards = db.relationship('BankDetails', backref='user', lazy='dynamic')
    registeredProperties = db.relationship('Property',secondary=lambda: RegisteredAssociation.__table__, backref="RegisteredBidders")


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
    
    def set_id_confirmation(self,value):
        self.id_confirmation=value

    def __repr__(self):
        return '<User %r>' % self.login_name

@login_manager.user_loader
def load_user(id):
    return User.query.get(id)

class RegisteredAssociation(db.Model):
    __tablename__ = 'RegisteredAssociation'
    RegisteredBidderID = db.Column(db.Integer, db.ForeignKey('User.id'), primary_key=True, nullable=False)
    PropertyID = db.Column(db.Integer, db.ForeignKey('Property.id'), primary_key=True, nullable=False)

class BankDetails(db.Model):
    __tablename__ = 'BankDetails'
    id = db.Column("card_number",db.String, primary_key=True)
    holder_fname = db.Column(db.String(), nullable=False)
    holder_lname = db.Column(db.String(20), nullable=False)
    cvc = db.Column(db.String, nullable=False)
    expire_date = db.Column(db.DateTime, nullable=False)
    
    user_id = db.Column(db.Integer, db.ForeignKey('User.id'), nullable=False)

    def set_fname(self,value):
        self.holder_fname=value

    def set_lname(self,value):
        self.holder_lname=value

    def set_cvc(self,value):
        self.cvc=value

    def set_expire_date(self,value):
        self.expire_date=value

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
        return f"AuctionDetails('{self.id}', '{self.PropertyID}', '{self.SellerID}', {self.AuctionStart}, {self.AuctionEnd}, {self.ReservePrice}, {self.MinBiddingGap})"

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
    num_bedrooms = db.Column(db.Integer)
    num_parking = db.Column(db.Integer)
    num_bathrooms = db.Column(db.Integer)
    parking_features = db.Column(db.String)
    building_size = db.Column(db.Integer)
    land_size = db.Column(db.Integer)
    inspection_date = db.Column(db.DateTime)
    description = db.Column(db.String(2000))
    year_built = db.Column(db.Integer)
    status = db.Column(db.String)   
    #seller
    seller = db.Column(db.Integer, db.ForeignKey('User.id'))
    #one-to-one
    auctionId = db.relationship('AuctionDetails', backref='Property', uselist=False)
    #one-to-many
    photo_collection = db.relationship('Photos', backref='Property', lazy='dynamic')
    #many-to-many
    registeredBidders = db.relationship('User',secondary=lambda: RegisteredAssociation.__table__, backref="RegisteredProperties")
    

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
    db.session.query(Bid).delete()
    db.session.query(RegisteredAssociation).delete()
    db.session.commit()

def initial_db():

    clear_session()
    db.create_all()

    u1= User(login_name='Tom123@g', id_confirmation='id1', email="tom@gmail.com", address='address', date_of_birth= datetime.strptime("01/01/1999","%d/%m/%Y"),phone_number='1844444444')
    u1.set_password('Tom123@g')
    u2= User(login_name='Cloudia0@g', id_confirmation='id2', email="Couldia@gmail.com", address='address', date_of_birth= datetime.strptime("01/01/1999","%d/%m/%Y"),phone_number='1899999999')
    u2.set_password('Cloudia0@g')
    #professional bidder
    u3= User(login_name='Sky123@g', id_confirmation='id3', email="sky@gmail.com", address='address', date_of_birth= datetime.strptime("01/01/1999","%d/%m/%Y"),phone_number='1899999990')
    u3.set_password('Sky123@g')
    bank1=BankDetails(id='5555444433331111', holder_fname='Tom', holder_lname='Han',cvc='123', expire_date=datetime.strptime("12/2022","%m/%Y") ,user = u1)
    bank2 = BankDetails (id='1111222233334444', holder_fname='Sky', holder_lname='Sky', cvc='123', expire_date=datetime.strptime("12/2021","%m/%Y"), user=u3)
    bank3 = BankDetails (id='1111222233335555', holder_fname='Cloudia', holder_lname='Scan', cvc='123', expire_date=datetime.strptime("12/2021","%m/%Y"), user=u2)
    property1 = Property(   property_type = 'House',
                            add_num = '10', add_name = 'street', add_suburb = 'suburb1',
                            add_state = 'NSW', add_pc = '2000', num_bedrooms = '1',
                            num_parking = '1', num_bathrooms = '1',
                            parking_features = 'park features', building_size = '200',
                            land_size = '200', seller = 1, inspection_date = datetime.strptime('2020-12-12',"%Y-%m-%d"),
                            description = 'desc', year_built = '2019', status = 'auction')
    #auction not start
    auction1 = AuctionDetails(AuctionStart = datetime.strptime("2020-12-30 14:00:00","%Y-%m-%d %H:%M:%S"),
                                AuctionEnd = datetime.strptime("2020-12-31 14:00:00","%Y-%m-%d %H:%M:%S"),
                                ReservePrice = 500.0,
                                MinBiddingGap = 20.0,

                                PropertyID = 1,
                                SellerID = 1)

    property2 = Property(   property_type = 'House',
                            add_num = '99', add_name = 'street', add_suburb = 'suburb2',
                            add_state = 'NSW', add_pc = '2000', num_bedrooms = '3',
                            num_parking = '3', num_bathrooms = '3',
                            parking_features = 'park features', building_size = '200',
                            land_size = '200', seller = 1, inspection_date = datetime.strptime('2020-12-12',"%Y-%m-%d"),
                            description = 'desc', year_built = '2019', status = 'auction')
    #auction holding
    auction2 = AuctionDetails(AuctionStart = datetime.strptime("2020-11-10 14:00:00","%Y-%m-%d %H:%M:%S"),
                                AuctionEnd = datetime.strptime("2020-12-31 14:00:00","%Y-%m-%d %H:%M:%S"),
                                ReservePrice = 500.0,
                                MinBiddingGap = 20.0,

                                PropertyID = 2,
                                SellerID = 1)

    property3 = Property(   property_type = 'House',
                            add_num = '56', add_name = 'some street', add_suburb = 'suburb2',
                            add_state = 'NSW', add_pc = '2616', num_bedrooms = '3',
                            num_parking = '3', num_bathrooms = '3',
                            parking_features = 'park features', building_size = '200',
                            land_size = '200', seller = 1, inspection_date = datetime.strptime('2020-12-12',"%Y-%m-%d"),
                            description = 'desc', year_built = '2019', status = 'auction')
 

    property4 = Property(   property_type = 'Unit',
                            add_unit='01',add_num = '13', add_name = 'some street', add_suburb = 'suburb3',
                            add_state = 'NSW', add_pc = '2040', num_bedrooms = '5',
                            num_parking = '5', num_bathrooms = '5',
                            parking_features = 'park features', building_size = '1000',
                            land_size = '1000', seller = 2, inspection_date = datetime.strptime('2020-12-12',"%Y-%m-%d"),
                            description = 'desc', year_built = '2019', status = 'sold')
    #auction ends and sold
    auction4 = AuctionDetails(AuctionStart = datetime.strptime("2020-10-30 14:00:00","%Y-%m-%d %H:%M:%S"),
                                AuctionEnd = datetime.strptime("2020-10-31 14:00:00","%Y-%m-%d %H:%M:%S"),
                                ReservePrice = 500.0,
                                MinBiddingGap = 20.0,

                                PropertyID = 4,
                                SellerID = 2)

    property5 = Property(   property_type = 'Unit',
                            add_unit='52', add_num = '23', add_name = 'street', add_suburb = 'suburb4',
                            add_state = 'NSW', add_pc = '3100', num_bedrooms = '3',
                            num_parking = '2', num_bathrooms = '3',
                            parking_features = 'park features', building_size = '200',
                            land_size = '200', seller = 2, inspection_date = datetime.strptime('2020-12-12',"%Y-%m-%d"),
                            description = 'desc', year_built = '2019', status = 'Under Offer')
    #auction ends and under offer
    auction5 = AuctionDetails(AuctionStart = datetime.strptime("2020-10-30 14:00:00","%Y-%m-%d %H:%M:%S"),
                                AuctionEnd = datetime.strptime("2020-11-01 14:00:00","%Y-%m-%d %H:%M:%S"),
                                ReservePrice = 500.0,
                                MinBiddingGap = 20.0,

                                PropertyID = 5,
                                SellerID = 2)


    bid2 = Bid ( BidderID = 3, AuctionID = 3, Amount = 600) #sold
    bid3 = Bid ( BidderID = 3, AuctionID = 4, Amount = 400) #under offer

    register2 = RegisteredAssociation(RegisteredBidderID=3, PropertyID = 4)
    register3 = RegisteredAssociation(RegisteredBidderID=3, PropertyID = 5)

    photo1 = Photos(photo = '1.jpg', property_id = 1 )
    photo2 = Photos(photo = '1-bedroom.jpg', property_id = 1 )
    photo3 = Photos(photo = '2.jpg', property_id = 2 )
    photo4 = Photos(photo = '2-bathroom.jpg', property_id = 2 )
    photo5 = Photos(photo = '03.jpg', property_id = 3 )

    db.session.add(u1)
    db.session.add(u2)
    db.session.add(u3)
    db.session.add(bank1)
    db.session.add(bank2)
    db.session.add(bank3)
    db.session.add(property1)
    db.session.add(property2)
    db.session.add(property3)
    db.session.add(property4)
    db.session.add(property5)
    db.session.add(auction1)
    db.session.add(auction2)
    db.session.add(auction4)
    db.session.add(auction5)
    db.session.add(bid2)
    db.session.add(bid3)
    db.session.add(register2)
    db.session.add(register3)
    db.session.add(photo1)
    db.session.add(photo2)
    db.session.add(photo3)
    db.session.add(photo4)
    db.session.add(photo5)

    db.session.commit()


# initial_db()

#buyers and sellers all have to add extral bank details at some point, and all their attributes are the same,
#So I just treat them all as users, They just need to input the extral details at different time. 
#It is not clearified that if one user should have only 1 or more bank cards, so I treat band details as a class
#and only need to justify a user keep one or a list of bank account

#The difference is that buyers need to register initial bids for properties
#If user keeps the initial bids as an attribute, he/she has to keep a list of initial bids and cooresponding property(ID)
#Or should the property keeps a list of registered auction buyers(RAB) with their cooresponding initial bids 
