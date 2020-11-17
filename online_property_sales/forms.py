from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, BooleanField, SubmitField, DecimalField, DateTimeField, SelectField, DateField
from wtforms.validators import ValidationError, DataRequired, EqualTo, Length, Regexp, Optional, Email, NumberRange
from flask import flash
from models import User
from sqlalchemy import func
import re
from datetime import datetime


class BankDetailsForm(FlaskForm):
    holder_fname = StringField ('Holder First Name', validators=[DataRequired(), Regexp('^[A-Za-z]+$', message="Please input only characters")])
    holder_lname = StringField ('Holder Last Name', validators=[DataRequired(), Regexp('^[A-Za-z]+$', message="Please input only characters" )])
    card_number = StringField ( 'Card Number',validators=[ DataRequired(),Length(min=16, max=16), Regexp('^[0-9]{16}$', message='Please input exact 16 digits')  ] )
    cvc = StringField ( 'CVC', validators=[ DataRequired(),Length(min=3, max=3), Regexp('^[0-9]{3}$', message='Please input exact 3 digits') ] )
    expire_date = DateTimeField('Expire Date', format = "%m/%Y", validators=[DataRequired()])
    submit = SubmitField()

    def validate_expire_date(self, value):
        if datetime.now() > self.expire_date.data:
            return False
        return True

    def validate_cvc(self, value):
        if self.cvc.data == '000':
            return False
        return True

class searchForm(FlaskForm):
    auction_before =  DateTimeField('Auction Before', format='%Y-%m-%d %H:%M:%S',validators=[Optional()])
    auction_after = DateTimeField('Auction After', format='%Y-%m-%d %H:%M:%S',validators=[Optional()])
    suburb = SelectField('Suburb', validators=[Optional()])
    state = SelectField('State', validators=[Optional()])
    street = StringField('Street Name',validators=[Optional()])
    postcode = StringField('Postcode', validators=[Optional()])
    submit = SubmitField('Search')
    clear = SubmitField('Clear Filter')

class passwordForm(FlaskForm):
    old_password = PasswordField('Confirm Old Password',validators= [Optional()])
    password = PasswordField('Password', validators=[Optional(), 
        Regexp("^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$", 
        message="Minimum 8 letters and should contain at least one number, one lowercase letter, one Uppercase letter and one special character(@$!%*?&)")])
    password2 = PasswordField('Repeat Password',validators= [Optional(), EqualTo('password')])
    submit = SubmitField('Edit')

class AccountForm(FlaskForm):
    login_name = StringField('Login name', validators=[Optional()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    address = StringField('Address', validators=[DataRequired()])
    date_of_birth = DateTimeField('Date of birth', format = "%d/%m/%Y", validators=[DataRequired()])
    phone_number = StringField ('Phone Number',  validators=[ DataRequired(),Length(min=10, max=10) ] )
    id_confirmation = StringField ('Id Confirmation', validators=[Optional()])

    submit = SubmitField('Submit')

    def validate_username(self, login_name, user_id):
        user = User.query.filter( func.lower(User.login_name) == func.lower(login_name)).first()
        if user is not None:
            return False
        return True
        
    def validate_email(self, user_id):
        user = User.query.filter( User.email == self.email.data).first()
        if user is not None and str(user.id) != user_id:
            return False
        return True
    
    def validate_phone_number(self, user_id):
        user = User.query.filter( User.phone_number == self.phone_number.data).first()
        if user is not None and str(user.id) != user_id:
            return False
        return True

    def validate_date_of_birth(self, date_of_birth):
        if datetime.now() <= self.date_of_birth.data:
            return False
        return True

class SignupForm(FlaskForm):
    login_name = StringField('Login Name', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired(),
        Regexp("^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$", 
        message="Minimum 8 letters and should contain at least one number, one lowercase letter, one Uppercase letter and one special character @$!%*?&")])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    email = StringField('Email Address', validators = [DataRequired(), Email()]) 
    address = StringField('Address', validators=[DataRequired()])
    date_of_birth = DateTimeField('Date of Birth', format = "%d/%m/%Y", validators=[DataRequired()])
    phone_number = StringField('Phone Number', validators=[DataRequired(), Length(min=10, max=10),Regexp('^\d{10}$', message='Only numbers')])

    submit = SubmitField('Register')

    def validate_username(self, login_name):
        user = User.query.filter( func.lower(User.login_name) == func.lower(login_name)).first()
        if user is not None:
            return False
        return True

    def validate_email(self, email):
        user = User.query.filter( User.email == self.email.data).first()
        if user is not None:
            return False
        return True
    
    def validate_phone_number(self, phone_number):
        user = User.query.filter( User.phone_number == self.phone_number.data).first()
        if user is not None:
            return False
        return True

    def validate_date_of_birth(self, date_of_birth):
        if datetime.now() <= self.date_of_birth.data:
            return False
        return True

class LoginForm(FlaskForm):
    login_name = StringField('Login Name', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Log In')

class PropertyForm(FlaskForm):
    property_type = SelectField('Property Type', [DataRequired()],
                        choices=[('house', 'House'),
                                 ('unit', 'Apartments & Units'),
                                 ('townhouse', 'Townhouse'),
                                 ('villa', 'Villa'),
                                 ('land', 'Land'),
                                 ('acerage', 'Acerage'),
                                 ('rural', 'Rural'),
                                 ('blocks', 'Blocks of Units'),
                                 ('retirement', 'Retirement Living')])
    add_unit = StringField('Unit Number', validators=[Optional()])
    add_num = StringField('Street Number', validators=[DataRequired()])
    add_name = StringField('Street Name', validators=[DataRequired()])
    add_suburb = StringField('Suburb', validators=[DataRequired()])
    add_state = SelectField('State', [DataRequired()],
                        choices=[('ACT', 'ACT'),
                                 ('QLD', 'QLD'),
                                 ('NSW', 'NSW'),
                                 ('NT', 'NT'),
                                 ('SA', 'SA'),
                                 ('TAS', 'TAS'),
                                 ('WA', 'WA')])
    add_pc = StringField('Postcode', validators=[DataRequired()])
    num_bedrooms = StringField('Number of Bedrooms', validators=[DataRequired()])
    num_bathrooms = StringField('Number of Bathrooms', validators=[DataRequired()])
    num_parking = StringField('Number of Parking', validators=[DataRequired()])
    parking_features = StringField('Parking Features', validators=[DataRequired()])
    building_size = StringField('Building Size', validators=[DataRequired()])
    land_size = StringField('Land Size', validators=[DataRequired()])
    inspection_date = DateField('Date of Inspection')
    description = StringField('Property Description', validators=[DataRequired()])
    year_built = StringField('Year of Built', validators=[DataRequired()])
    submit = SubmitField('Submit')

class AddImageForm(FlaskForm):
    image = FileField('Add Image', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Submit')

class EditInspectionDate(FlaskForm):
    inspection_date = DateField('Date of Inspection')
    submit = SubmitField('Submit')

class RegistrationForm(FlaskForm):
    auctionStart = DateTimeField('Auction Start Time', validators=[DataRequired()])
    auctionEnd = DateTimeField('Auction End Time', validators=[DataRequired()])
    #HouseID = StringField('HouseID',validators=[DataRequired(), Length(min=2, max=20)])
    #SellerID = StringField('SellerID',validators=[DataRequired(), Length(min=2, max=20)])
    reservePrice = DecimalField('Reserve Price', validators=[DataRequired()])
    minBiddingGap = DecimalField('Bidding Gap', validators=[DataRequired()])
    submit = SubmitField('Save Auction')

class MakeBidForm(FlaskForm):
    newBid = DecimalField('Bidding Amount', validators=[DataRequired()])
    submitBid = SubmitField('Make Bid')