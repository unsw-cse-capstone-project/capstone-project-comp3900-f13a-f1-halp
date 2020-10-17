from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, DecimalField, DateTimeField, SelectField, DateField
from wtforms.validators import ValidationError, DataRequired, EqualTo, Length, Regexp, Optional
from flask import flash
from userDetails import User
import re

class AccountForm(FlaskForm):
    password = PasswordField('Password')
    password2 = PasswordField('Repeat Password',validators= [EqualTo('password')])
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
   
    

class SignupForm(FlaskForm):
    login_name = StringField('login_name', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])

    address = StringField('address', validators=[DataRequired()])
    date_of_birth = StringField('date_of_birth', validators=[DataRequired(), Regexp('^[0-9]{2}/[0-9]{2}/[0-9]{4}$', message='Please input following the fomat dd/mm/yyyy e.g. 01/06/2022 ') ])
    phone_number = StringField('phone_number', validators=[DataRequired(), Length(min=10, max=10)])

    submit = SubmitField('Register')

    def validate_username(self, login_name):
        user = User.query.filter_by(login_name=self.login_name.data).first()
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
    address = StringField('Address', validators=[DataRequired()])
    num_bedrooms = StringField('Number of Bedrooms', validators=[DataRequired()])
    num_bathrooms = StringField('Number of Bathrooms', validators=[DataRequired()])
    num_parking = StringField('Number of Parking', validators=[DataRequired()])
    parking_features = StringField('Parking Features', validators=[DataRequired()])
    building_size = StringField('Building Size', validators=[DataRequired()])
    land_size = StringField('Land Size', validators=[DataRequired()])
    inspection_date = DateField('Date of Inspection')
    description = StringField('Property Description', validators=[DataRequired()])
    year_built = StringField('Year of Built', validators=[DataRequired()])
    #photos haha
    submit = SubmitField('Submit')
    
class RegistrationForm(FlaskForm):
    auctionStart = DateTimeField('Auction Start Time, Form = "%Y-%m-%d %H:%M:%S"', validators=[DataRequired()])
    auctionEnd = DateTimeField('Auction End Time, Form = "%Y-%m-%d %H:%M:%S"', validators=[DataRequired()])
    #HouseID = StringField('HouseID',validators=[DataRequired(), Length(min=2, max=20)])
    #SellerID = StringField('SellerID',validators=[DataRequired(), Length(min=2, max=20)])
    reservePrice = DecimalField('Reserve Price', validators=[DataRequired()])
    minBiddingGap = DecimalField('Bidding Gap', validators=[DataRequired()])
    submit = SubmitField('CreateClass')
