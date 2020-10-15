from flask import render_template, url_for, flash, redirect
from auction import app
from auction.forms import *
from auction.models import *

@app.route("/")
@app.route("/home")
def home():
    return "<h1>Home Page</h1>"

@app.route("/createAuction", methods=['GET', 'POST'])
def createAuction():
	form = RegistrationForm()
	if form.validate_on_submit():
		flash(f'Account created for {form.reservePrice.data}!', 'success')
		return redirect(url_for('home'))

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