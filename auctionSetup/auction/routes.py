from flask import render_template, url_for, flash, redirect
from auction import app
from auction.forms import *
from auction.models import *
import random

@app.route("/")
@app.route("/home")
def home():
    return "<h1>Home Page</h1>"

@app.route("/createAuction", methods=['GET', 'POST'])
def createAuction():
	form = RegistrationForm()
	if form.validate_on_submit():
		auctionDetails = AuctionDetails(AuctionID = random.random(), PropertyID = random.random(), SellerID = random.random(), AuctionStart = form.auctionStart.data, AuctionEnd = form.auctionEnd.data, 
			ReservePrice = form.reservePrice.data, MinBiddingGap = form.minBiddingGap.data)
		db.session.add(auctionDetails)
		db.session.commit()
		flash(f'Auction created for {form.reservePrice.data}!', 'success')
		return redirect(url_for('home'))

		cards=BankDetails.query.filter_by(id=card_number).all()
	return render_template('createAuction.html', form = form)


@app.route("/about")
def about():
	return "<h1>About Page</h1>"

@app.route("/register")
def register():
	return "<h1>Register Page</h1>"

@app.route("/login")
def login():
	return "<h1>Login Page</h1>"