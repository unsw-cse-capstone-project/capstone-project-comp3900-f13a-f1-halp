from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, DecimalField, DateTimeField, SelectField, DateField
from wtforms.validators import ValidationError, DataRequired, EqualTo
from flask import flash
from userDetails import User
import re

class AccountForm(FlaskForm):
    password = PasswordField('password')
    password2 = PasswordField('Repeat Password')

    address = StringField('address')
    date_of_birth = StringField('date_of_birth')

    holder_fname = StringField ('holder_fname')
    holder_lname = StringField ('holder_lname')

    card_number = StringField ('card_number')
    phone_number = StringField ('phone_number')
    id_confirmation = StringField ('id_confirmation')
    cvc = StringField ('cvc')
    expire_date = StringField ('expire_date')

    # cancel = SubmitField('Cancel')
    submit = SubmitField('Edit')
    

class SignupForm(FlaskForm):
    login_name = StringField('login_name', validators=[DataRequired()])
    
    password = PasswordField('password', validators=[DataRequired()])

    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])

    address = StringField('address', validators=[DataRequired()])
    date_of_birth = StringField('date_of_birth', validators=[DataRequired()])
    phone_number = StringField('phone_number', validators=[DataRequired()])

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
