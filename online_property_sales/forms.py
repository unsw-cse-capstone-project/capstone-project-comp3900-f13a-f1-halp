from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, BooleanField, SubmitField, DecimalField, DateTimeField, SelectField, DateField
from wtforms.validators import ValidationError, DataRequired, EqualTo, Length, Regexp, Optional, Email
from flask import flash
from models import User
from sqlalchemy import func
import re

class searchForm(FlaskForm):
    auction_before =  DateTimeField('Auction Before', format='%Y-%m-%d %H:%M:%S', validators=[Optional()])
    # auctionStart_before = BooleanField('before')
    # auctionStart_after = BooleanField('after')

    auction_after = DateTimeField('Auction After', format='%Y-%m-%d %H:%M:%S',validators=[Optional()])
    # auctionEnd_before = BooleanField('before')
    # auctionEnd_after = BooleanField('after')

    suburb = StringField('Suburb', validators=[Optional()])
    submit = SubmitField('Search')

class passwordForm(FlaskForm):
    old_password = PasswordField('Confirm Old Password',validators= [Optional()])
    password = PasswordField('Password', validators=[Optional(), 
        Regexp("^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$", 
        message="Minimum 8 letters and should contain at least one number, one lowercase letter, one Uppercase letter and one special character(@$!%*?&)")])
    password2 = PasswordField('Repeat Password',validators= [Optional(), EqualTo('password')])
    submit = SubmitField('Edit')

class AccountForm(FlaskForm):
    login_name = StringField('login_name', validators=[Optional()])
    email = StringField('Email', validators=[Optional(), Email()])
    address = StringField('Address')
    date_of_birth = StringField('Date of Birth',validators=[ Optional(),Regexp('^[0-9]{2}/[0-9]{2}/[0-9]{4}$', message='Please input following the fomat dd/mm/yyyy e.g. 01/06/2022 ')])
    holder_fname = StringField ('Holder First Name')
    holder_lname = StringField ('Holder Last Name')

    card_number = StringField ( 'Card Number',validators=[ Optional(),Length(min=16, max=16), Regexp('^[0-9]{16}$', message='Please input exact 16 digits')  ] )
    phone_number = StringField ('Phone Number',  validators=[ Optional(),Length(min=10, max=10) ] )
    id_confirmation = StringField ('Id Confirmation')
    cvc = StringField ( 'CVC', validators=[ Optional(),Length(min=3, max=3), Regexp('^[0-9]{3}$', message='Please input exact 3 digits') ] )
    expire_date = StringField ('Expire Date',validators=[ Optional(),Regexp('^[0-9]{2}/[0-9]{4}$', message='Please input following the fomat mm/yyyy e.g. 06/2022 ') ] )

    submit = SubmitField('Edit')

    # cancel = SubmitField('Cancel')
    def validate_username(self, login_name, user_id):
        user = User.query.filter( func.lower(User.login_name) == func.lower(login_name)).first()
        if user is not None:
            if user.id == user_id:
                flash(f"Please select another unique name or leave the slot empty for not changing your login name", 'danger')
            else:
                flash(f"Please select another unique name!", 'danger')
            return False
        return True
    

class SignupForm(FlaskForm):
    login_name = StringField('login_name', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired(),
        Regexp("^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$", 
        message="Minimum 8 letters and should contain at least one number, one lowercase letter, one Uppercase letter and one special character @$!%*?&")])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    email = StringField('Email address', validators = [DataRequired(), Email()]) 
    address = StringField('address', validators=[DataRequired()])
    date_of_birth = StringField('date_of_birth', validators=[DataRequired(), Regexp('^[0-9]{2}/[0-9]{2}/[0-9]{4}$', message='Please input following the fomat dd/mm/yyyy e.g. 01/06/2022 ') ])
    phone_number = StringField('phone_number', validators=[DataRequired(), Length(min=10, max=10),Regexp('^\d{10}$', message='Only numbers')])

    submit = SubmitField('Register')

    def validate_username(self, login_name):
        user = User.query.filter( func.lower(User.login_name) == func.lower(login_name)).first()
        if user is not None:
            flash("Please select another unique name!")
            return False
        return True

    def validate_DOB(self, data):
        r=re.compile('.{2}/.{2}/.{4}')
        if r.match(data):
            return True
        flash("Please input date with valid format!")
        return False

class LoginForm(FlaskForm):
    login_name = StringField('login_name', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('logIn')

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
    # old address version
    address = StringField('Address')

    # new address version
    add_unit = StringField('Unit Number', validators=[DataRequired()])
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
    
class RegistrationForm(FlaskForm):
    auctionStart = DateTimeField('Auction Start Time, Form = "%Y-%m-%d %H:%M:%S"', validators=[DataRequired()])
    auctionEnd = DateTimeField('Auction End Time, Form = "%Y-%m-%d %H:%M:%S"', validators=[DataRequired()])
    #HouseID = StringField('HouseID',validators=[DataRequired(), Length(min=2, max=20)])
    #SellerID = StringField('SellerID',validators=[DataRequired(), Length(min=2, max=20)])
    reservePrice = DecimalField('Reserve Price', validators=[DataRequired()])
    minBiddingGap = DecimalField('Bidding Gap', validators=[DataRequired()])
    submit = SubmitField('CreateClass')
