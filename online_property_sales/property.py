from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, time
from server import db

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
    #seller
    seller = db.Column(db.String(100))
    inspection_date = db.Column(db.DateTime)
    description = db.Column(db.String(2000))
    year_built = db.Column(db.Integer)
    photo_collection = db.relationship('Photos', backref='author', lazy='dynamic')

    def set_property_type(self, p_type):
        self.property_type = p_type

    def set_address(self, address):
        self.address = address

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
        return '<Property at %r>' % self.id

class Photos(db.Model):
    __tablename__ = 'Photos'

    id = db.Column(db.Integer, primary_key = True)
    photo = db.Column(db.String)
    property_id = db.Column(db.Integer, db.ForeignKey('Property.id'))

    def set_photo(self, photo):
        self.photo = photo
'''

p1 = Property(property_type = 'house', address = '1 John Street, Chatswood, NSW, 2130')
p1.set_num_bedrooms(3)
p1.set_num_bathrooms(3)
p1.set_num_parking(2)
p1.set_building_size(110)
p1.set_land_size(300)
p1.set_seller('Cloudia')
p1.set_inspection_date(datetime(2020,10,20,0,0,0))
p1.set_description('Amazing views in the heart of Chatswood')
p1.set_year_built(1990)

db.session.add(p1)
db.session.commit()

'''