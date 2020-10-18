from userDetails import User, BankDetails, clear_session, AuctionDetails
from property import Property
from server import app, db, login_manager
from flask import render_template, request, redirect, url_for, flash
from flask_login import LoginManager, UserMixin, current_user, logout_user, login_required,login_user
from datetime import datetime
from forms import LoginForm, SignupForm, AccountForm, PropertyForm, RegistrationForm
import re
import random

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

    if form.validate_on_submit():
        if form.validate_username(form.login_name.data):
            if form.validate_DOB(form.date_of_birth.data):
                user = User(login_name=form.login_name.data, address = form.address.data, date_of_birth = datetime.strptime(form.date_of_birth.data,'%d/%m/%Y'), phone_number=form.phone_number.data)
                user.set_password(form.password.data)
                db.session.add(user)
                db.session.commit()
                flash('Congratulations, you are now a registered user!')
                return redirect(url_for('login'))
            else:
                flash('Please input DOB with valid format!')
        else:
            flash('The username has been taken, please input another one')
    return render_template('signup.html', title='signup', form=form)

@app.route('/account', methods=['POST','GET'])
def edit_account():
    
    if current_user.is_anonymous:
        flash('Please login first')
        return redirect(url_for('login'))

    form = AccountForm()
    user = User.query.filter_by(login_name=current_user.login_name).first()
    
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
            r=re.compile('.{2}/.{2}/.{4}')
            if r.match(date_of_birth):
                user.set_date_of_birth( datetime.strptime(date_of_birth,'%d/%m/%Y'))
                change=True
            else:
                flash("Please input DOB with valid format!")

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
            cards=BankDetails.query.filter_by(id=card_number).all()
            for c in cards:
                #the user has this card and going to change details
                if card_number == c.id:
                    new_card=False 
                    if c.user_id == current_user.id:
                        old_card = c
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
                            r=re.compile('.{2}/.{4}')
                            if r.match(expire_date):
                                old_card.set_expire_date(datetime.strptime(date_of_birth,'%m/%Y'))
                                change=True
                            else:
                                flash("Please input expire date with valid format!")
                        if id_confirmation:
                            old_card.set_id_confirmation(id_confirmation)
                            change=True
                    else:
                        new_card=False
                        flash("This card already registered by other user")

        #this is a new card, all the info should be inputed
        if new_card == True:
            r=re.compile('.{2}/.{4}')
            if holder_fname and holder_lname and cvc and expire_date and id_confirmation and r.match(expire_date):
                bank = BankDetails(id=card_number,id_confirmation=id_confirmation ,holder_fname=holder_fname, holder_lname=holder_lname,cvc=cvc, expire_date=datetime.strptime(expire_date,'%m/%Y'), author=user)
                flash("Congraduation! you add a new bank card to your account")
                change=True
                db.session.add(bank)
            else:
                flash("This is a new card, the full info of the card should be inserted! And please make sure the date format is correct")

        if change:
            db.session.commit()
            return redirect(url_for('home'))
    
    return render_template('account.html', title='account', form=form)

@app.route('/property', methods=['POST','GET'])
def property_details():
    if current_user.is_anonymous:
        flash('Please login first')
        return redirect(url_for('login'))

    form = PropertyForm()
    error = None

    if form.validate_on_submit():
        # Check values
        p_type = form.property_type.data
        p_add = form.address.data
        p_n_beds = form.num_bedrooms.data
        p_n_baths = form.num_bathrooms.data
        p_n_park = form.num_parking.data
        p_p_features = form.parking_features.data
        p_b_size = form.building_size.data
        p_l_size = form.land_size.data
        p_desc = form.description.data
        p_year = form.year_built.data
        p_i_date = form.inspection_date.data

        # Property Types
        if p_type == None:
            error = "Property Type error"
        print(p_type)

        # Address

        # Num bedrooms
        if not p_n_beds.isdigit():
            error = "Invalid data entered for a field"
            
        # Num bathrooms
        if not p_n_baths.isdigit():
            error = "Invalid data entered for a field"

        # Num Parking
        if not p_n_park.isdigit():
            error = "Invalid data entered for a field"

        # Parking Features

        # Building Size
        if not p_b_size.isdigit():
            error = "Invalid data entered for a field"

        # Land Size
        if form.building_size.data > form.land_size.data:
            error = "Building size exceeds land size"
            if not p_l_size.isdigit():
                error = "Invalid data entered for a field"

        # inspection date
        print(datetime.today().date())
        if not p_i_date > datetime.today().date():
            error = "Invalid date entered for a field"
            
        # description

        # year built
        if not p_year.isdigit():
            error = "Invalid year entered for a field"

        if error is None:
            property_p = Property(property_type = p_type, address = p_add, num_bedrooms = p_n_beds, num_bathrooms = p_n_baths, num_parking = p_n_park, parking_features = p_p_features, building_size = p_b_size, land_size = p_l_size, seller = User.login_name, inspection_date = p_i_date, description = p_desc, year_built = p_year)
            ## Not Working
            db.session.add(property_p)
            db.session.commit()
            return redirect(url_for('home'))

        return render_template('property.html', title = 'property', error = error, form = form)

    return render_template('property.html', title = 'property', form = form)
    
@app.route("/createAuction", methods=['GET', 'POST'])
def createAuction():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User.query.filter_by(login_name=current_user.login_name).first()
        auctionDetails = AuctionDetails(AuctionID = random.random(), PropertyID = random.random(), SellerID = current_user.login_name, AuctionStart = form.auctionStart.data, AuctionEnd = form.auctionEnd.data, 
            ReservePrice = form.reservePrice.data, MinBiddingGap = form.minBiddingGap.data)
        db.session.add(auctionDetails)
        db.session.commit()
        flash(f'Auction created for {form.reservePrice.data}!', 'success')
        return redirect(url_for('home'))

        cards=BankDetails.query.filter_by(id=card_number).all()
    return render_template('createAuction.html', form = form)