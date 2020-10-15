from userDetails import User, BankDetails, clear_session
from server import app, db, login_manager
from flask import render_template, request, redirect, url_for, flash
from flask_login import LoginManager,UserMixin, current_user, logout_user, login_required,login_user
from datetime import datetime
from forms import LoginForm, SignupForm, AccountForm
import re

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/login', methods = ['GET','POST'])
def login():
    
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    
    form = LoginForm()
    if form.validate_on_submit():

        user = User.query.filter_by(login_name=form.login_name.data).first()

        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))

        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('home'))

    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/signup', methods=['GET','POST'])
def signup():

    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = SignupForm()

    if form.validate_on_submit() and form.validate_username(form.login_name.data) and form.validate_DOB(form.date_of_birth.data):
        user = User(login_name=form.login_name.data, address = form.address.data, date_of_birth = datetime.strptime(form.date_of_birth.data,'%d/%m/%Y'), phone_number=form.phone_number.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')

        return redirect(url_for('login'))

    return render_template('signup.html', title='signup', form=form)

@app.route('/account', methods=['POST','GET'])
def edit_account():
    
    if current_user.is_anonymous:
        flash('Please login first')
        return redirect(url_for('login'))

    form = AccountForm()
    user = User.query.filter_by(login_name=current_user.login_name).first()
    cards= user.cards.all()
    change=False
    if form.validate_on_submit():

        password = form.password.data
        password2 = form.password2.data
        if password:
            if password2:
                if password==password2:
                    user.set_password(password)
                    change=True
                else:
                    flash('Please repeat the same password')
            else:
                flash('Please repeat the same password')

        address =  form.address.data
        if address:
            user.set_address(address)
            change=True

        date_of_birth = form.date_of_birth.data
        if date_of_birth:
            if form.validate_DOB(date_of_birth):
                user.set_date_of_birth( datetime.strptime(date_of_birth,'%d/%m/%Y'))
                change=True
            else:
                flash("Please input the DOB following the format dd/mm/yyy")

        phone_number =  form.phone_number.data
        if phone_number:
            user.set_phone_number(phone_number)
            change=True

        card_number = form.card_number.data
        holder_fname =  form.holder_fname.data
        holder_lname =  form.holder_lname.data
        id_confirmation =  form.id_confirmation.data
        cvc =  form.cvc.data
        expire_date =  form.expire_date.data

        new_card=True
        if card_number:
            for c in cards:
                #the user has this card and going to change details
                if card_number == c.card_number:
                    new_card=False 
                    old_card = cards.query.get(card_number)
                    if holder_fname:
                        old_card.set_fname(holder_fname)
                        change=True
                    if holder_lname:
                        old_card.set_lname(holder_lname)
                        change=True
                    if cvc:
                        old_card.set_cvc(cvc)
                        change=True
                    if expire_date:
                        old_card.set_expire_date(expire_date)
                        change=True
                    if id_confirmation:
                        old_card.set_id_confirmation(id_confirmation)
                        change=True

        #this is a new card, all the info should be inputed
        if new_card == True and holder_fname and holder_lname and cvc and expire_date and id_confirmation:
            bank = BankDetails(id=card_number,id_confirmation=id_confirmation ,holder_fname=holder_fname, holder_lname=holder_lname,cvc=cvc, expire_date=datetime.strptime(expire_date,'%m/%Y'), author=user)
            change=True
            db.session.add(bank)

        if change:
            db.session.commit()
            return redirect(url_for('home'))
    
    return render_template('account.html', title='account', form=form)

@app.route('/property')
def property_details():
    
    if current_user.is_anonymous:
        flash('Please login first')
        return redirect(url_for('login'))

    return render_template('property.html')