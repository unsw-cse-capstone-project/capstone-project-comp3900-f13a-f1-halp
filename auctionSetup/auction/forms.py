from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, DecimalField, DateTimeField
from wtforms.validators import DataRequired, Length, Email, EqualTo

class RegistrationForm(FlaskForm):
    auctionStart = DateTimeField('Auction Start Time', validators=[DataRequired()])
    auctionEnd = DateTimeField('Auction End Time', validators=[DataRequired()])
    HouseID = StringField('HouseID',validators=[DataRequired(), Length(min=2, max=20)])
    SellerID = StringField('SellerID',validators=[DataRequired(), Length(min=2, max=20)])
    reservePrice = DecimalField('Reserve Price', validators=[DataRequired()])
    MinBiddingGap = DecimalField('Bidding Gap', validators=[DataRequired()])