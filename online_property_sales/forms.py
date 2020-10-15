from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
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