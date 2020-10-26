from userDetails import User, BankDetails, clear_session, AuctionDetails
from server import app, db, login_manager
from flask import render_template, request, redirect, url_for, flash
from flask_login import LoginManager,UserMixin, current_user, logout_user, login_required,login_user
from datetime import datetime
from forms import LoginForm, SignupForm, AccountForm, PropertyForm, RegistrationForm
import re
import random
import sys

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
            flash('Invalid username or password','danger')
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
                flash('Congratulations, you are now a registered user!','success')
                return redirect(url_for('login'))
            else:
                flash('Please input DOB with valid format!','danger')
        else:
            flash('The username has been taken, please input another one','danger')
    return render_template('signup.html', title='signup', form=form)

@app.route('/account/<login_name>', methods=['POST','GET'])
@login_required
def account(login_name):
    
    if current_user.is_anonymous:
        flash('Please login first','danger')
        return redirect(url_for('login'))

    form = AccountForm()
    user = User.query.filter_by(login_name=login_name).first_or_404()
    
    if form.validate_on_submit():

        user.set_address(form.address.data)
        user.set_phone_number(form.phone_number.data)
        date_of_birth = form.date_of_birth.data
        user.set_date_of_birth( datetime.strptime(date_of_birth,'%d/%m/%Y'))
        if form.password.data:
            user.set_password(form.password.data)

        card_number = form.card_number.data
        holder_fname =  form.holder_fname.data
        holder_lname =  form.holder_lname.data
        id_confirmation =  form.id_confirmation.data
        cvc =  form.cvc.data
        expire_date =  form.expire_date.data

        if len(card_number)>0:
            new_card=True
            old_card=BankDetails.query.get(card_number)
            #this card already in our database
            if old_card!=None:
                #this card belongs to current user
                if old_card.user_id == user.id:
                    new_card=False 
                    if holder_fname:
                        old_card.set_fname(holder_fname)
                    if holder_lname:
                        old_card.set_lname(holder_lname)
                    if cvc:
                        old_card.set_cvc(cvc)
                    if expire_date:
                        old_card.set_expire_date(datetime.strptime(expire_date,'%m/%Y'))
                    if id_confirmation:
                        old_card.set_id_confirmation(id_confirmation)
                #this card does not belong to current user
                else:
                    new_card=False
                    flash(f"This card already registered by other user", 'danger')
                    return render_template('account.html', title='account', form=form, user=user)

            #this is a new card, all the info should be inputed
            if new_card == True:
                if holder_fname and holder_lname and cvc and expire_date and id_confirmation and expire_date:
                    bank = BankDetails(id=card_number,id_confirmation=id_confirmation ,holder_fname=holder_fname, holder_lname=holder_lname,cvc=cvc, expire_date=datetime.strptime(expire_date,'%m/%Y'), author=user)
                    flash("Congraduation! you add a new credit card to your account",'success')
                    db.session.add(bank)
                else:
                    flash(f"This is a new card, the full info of the card should be inserted! And please make sure the date format is correct",'danger')
                    db.session.commit()
                    return render_template('account.html', title='account', form=form, user=user)
               
        #only change user details with no errors
        db.session.commit()
        return redirect(url_for('home'))

    elif request.method == 'GET':
        form.address.data = current_user.address
        form.date_of_birth.data = current_user.date_of_birth.strftime("%d/%m/%Y")
        form.phone_number.data = current_user.phone_number
        if len(current_user.cards.all()) == 0:
            flash(f'You have not inputted a credit card before, please upload one with full bank details.', 'info')
        else:
            flash(f'To edit parts or whole details of your uploaded credit cards, you have to input the card name correctly.','info')

    return render_template('account.html', title='account', form=form, user=user)

@app.route('/property', methods=['POST','GET'])
def property_details():
    form = PropertyForm()
    if form.validate_on_submit():
        # Check values

        # Property Types
        if form.property_type.data == "house":
            print("House")
        elif form.property_type.data == "unit":
            print("Apartments")
        elif form.property_type.data == "townhouse":
            print("Townhouse")
        elif form.property_type.data == "villa":
            print("Villa")
        elif form.property_type.data == "land":
            print("Land")
        elif form.property_type.data == "acerage":
            print("Acerage")
        elif form.property_type.data == "rural":
            print("Rural")
        elif form.property_type.data == "blocks":
            print("Blocks of Units")
        elif form.property_type.data == "retirement":
            print("Retirement")
        else:
            print("Error")

        # Address

        # Num bedrooms
        if form.num_bedrooms.data.isdigit():
            print(form.num_bedrooms.data)
            # Else statement

        # Num bathrooms
        if form.num_bathrooms.data.isdigit():
            print(form.num_bathrooms.data)
            # Else statement

        # Num Parking
        if form.num_parking.data.isdigit():
            print(form.num_parking.data)
            # Else statement

        # Parking Features

        # Building Size
        if form.building_size.data.isdigit():
            print(form.building_size.data)
            # Else statement

        # Land Size
        if form.land_size.data.isdigit():
            print(form.land_size.data)
            # Else statement

        # inspection date
        
        # description

        # year built
        if form.year_built.data.isdigit():
            print(form.year_built.data)






        return redirect(url_for('home'))

    return render_template('property.html', title = 'property', form = form)
    
@app.route("/createAuction", methods=['GET', 'POST'])
def createAuction():
    if current_user.is_anonymous:
        flash('Please login first')
        return redirect(url_for('login'))

    form = RegistrationForm()
    if form.validate_on_submit():
        user = User.query.filter_by(login_name=current_user.login_name).first()
        auctionDetails = AuctionDetails(AuctionID = random.random(), PropertyID = random.random(), SellerID = current_user.login_name, AuctionStart = form.auctionStart.data, AuctionEnd = form.auctionEnd.data, 
            ReservePrice = form.reservePrice.data, MinBiddingGap = form.minBiddingGap.data)
        db.session.add(auctionDetails)
        db.session.commit()
        flash('Auction created for {form.reservePrice.data}!', 'success')
        return redirect(url_for('home'))

    return render_template('createAuction.html', form = form)

@app.route("/auctions", methods=['GET', 'POST'])
def auctions():
    if current_user.is_anonymous:
        flash('Please login first')
        return redirect(url_for('login'))

    auctions = AuctionDetails.query.filter_by(SellerID = current_user.login_name)
    return render_template('auctions.html', auctions=auctions)

@app.route("/changeAuctionDetails", methods=['GET', 'POST'])
def changeAuctionDetails():
    if current_user.is_anonymous:
        flash('Please login first')
        return redirect(url_for('login'))

    AuctionID_=request.args.get('auctionID')
    print(AuctionID_)
    auction = AuctionDetails.query.filter_by(AuctionID = AuctionID_).first()

    form = RegistrationForm()

    if form.validate_on_submit():
        auction = AuctionDetails.query.filter_by(AuctionID = AuctionID_).first()
        auction.AuctionStart = form.auctionStart.data
        auction.AuctionEnd = form.auctionEnd.data
        auction.ReservePrice = form.reservePrice.data
        auction.MinBiddingGap = form.minBiddingGap.data
        db.session.commit()
        flash(f'Auction edited for {form.reservePrice.data}!', 'success')
        return redirect(url_for('home'))

    elif request.method == 'GET':
        form.auctionStart.data = auction.AuctionStart
        form.auctionEnd.data = auction.AuctionEnd
        form.reservePrice.data = auction.ReservePrice
        form.minBiddingGap.data = auction.MinBiddingGap

    return render_template('changeAuctionDetails.html', form=form)
    
@app.route("/deleteAuction", methods=['GET', 'POST'])
@login_required
def deleteAuction():
    if current_user.is_anonymous:
        flash('Please login first')
        return redirect(url_for('login'))

    AuctionID_=request.args.get('auctionID')
    print(AuctionID_)
    auction = AuctionDetails.query.filter_by(AuctionID = AuctionID_).first()

    #post = Post.query.get_or_404(post_id)

    #if auction.SellerID != current_user.login_name:
    #    abort(403)
    db.session.delete(auction)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('home'))