from models import User, BankDetails, clear_session, AuctionDetails, initial_db, Property, Photos
from server import app, db, login_manager
from flask import render_template, request, redirect, url_for, flash
from flask_login import LoginManager,UserMixin, current_user, logout_user, login_required,login_user
from datetime import datetime
from sqlalchemy import func
from forms import LoginForm, SignupForm, AccountForm, PropertyForm, RegistrationForm, passwordForm, searchForm, AddImageForm
from validateProperty import *
from PIL import Image
import random
import os
import secrets


# initial_db()

@app.route('/')
@app.route('/home')
def home():
    flash(f"Users are able to login with case insensitive login name, which means Tom123@g and tOM123@G is the same user. We have two users who have same password as their login_name in our db: Tom123@g and Cloudia@g",'info')
    return render_template('home.html')

@app.route('/login', methods = ['GET','POST'])
def login():
    
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter( func.lower(User.login_name) == func.lower(form.login_name.data)).first()
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
                user = User(login_name=form.login_name.data, email=form.email.data, address = form.address.data, date_of_birth = datetime.strptime(form.date_of_birth.data,'%d/%m/%Y'), phone_number=form.phone_number.data)
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
#HERE!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#HERE!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#HERE!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
@app.route('/search', methods=['POST','GET'])
# @login_required
def search():
    form=searchForm()
    auctions=[]
    
    if form.validate_on_submit():

        before=form.auction_before.data
        after=form.auction_after.data
        suburb = form.suburb.data
        
        if before and not after :
            auctions = AuctionDetails.query.filter(AuctionDetails.AuctionStart<=before).all()
        elif after and not before:
            auctions = AuctionDetails.query.filter(AuctionDetails.AuctionEnd>=after).all()
        elif before and after:
            auctions = AuctionDetails.query.filter(AuctionDetails.AuctionStart<=before,
                AuctionDetails.AuctionEnd>=after).all()

        return render_template('search.html', title='search', form=form, auctions=auctions)


    return render_template('search.html', title='search', form=form)
    
@app.route('/changePassword/<login_name>', methods=['POST','GET'])
@login_required
def changePassword(login_name):

    form = passwordForm()
    user = User.query.filter_by(login_name=login_name).first_or_404()

    if form.validate_on_submit():
        if form.old_password.data:
            if user.check_password(form.old_password.data):
                if form.password.data:
                    user.set_password(form.password.data)
                    db.session.commit()
                    return redirect('home')
                else:
                    flash(f'Please input your new password','info')
            else:
                flash(f'Please input correct original password','danger')
        else:
            flash(f'Please input correct original password and new password','info')

    return render_template('changePassword.html', title='Change Password', form=form, login_name=login_name)


@app.route('/account/<login_name>', methods=['POST','GET'])
@login_required
def account(login_name):
    
    form = AccountForm()
    user = User.query.filter_by(login_name=login_name).first_or_404()
    
    if form.validate_on_submit():
        #change password after confirmming old password first
        if form.login_name.data:
            if form.validate_username(form.login_name.data, user.id):
                user.set_login_name(form.login_name.data)
            else:
                return render_template('account.html', title='account', form=form, user=user)

        user.set_address(form.address.data)
        user.set_phone_number(form.phone_number.data)
        user.set_date_of_birth( datetime.strptime(form.date_of_birth.data,'%d/%m/%Y'))
        user.set_email(form.email.data)

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
        form.login_name.data = current_user.login_name
        form.address.data = current_user.address
        form.date_of_birth.data = current_user.date_of_birth.strftime("%d/%m/%Y")
        form.phone_number.data = current_user.phone_number
        form.email.data = current_user.email
        if len(current_user.cards.all()) == 0:
            flash(f'You have not inputted a credit card before, please upload one with full bank details.', 'info')
        else:
            flash(f'To edit parts or whole details of your uploaded credit cards, you have to input the card name correctly.','info')

    return render_template('account.html', title='account', form=form, user=user)

@app.route('/addProperty', methods=['GET', 'POST'])
def add_property():
    if current_user.is_anonymous:
        flash('Please login first')
        return redirect(url_for('login'))

    form = PropertyForm()
    error = None

    if form.validate_on_submit():
        if check_all_details(form):
            p_type = form.property_type.data
            p_add_unit = form.add_unit.data
            p_add_num = form.add_num.data
            p_add_name = form.add_name.data
            p_add_suburb = form.add_suburb.data
            p_add_state = form.add_state.data
            p_add_pc = form.add_pc.data
            p_n_beds = form.num_bedrooms.data
            p_n_baths = form.num_bathrooms.data
            p_n_park = form.num_parking.data
            p_p_features = form.parking_features.data
            p_b_size = form.building_size.data
            p_l_size = form.land_size.data
            p_desc = form.description.data
            p_year = form.year_built.data
            p_i_date = form.inspection_date.data

            p_to_db = Property(property_type = p_type, add_unit = p_add_unit,
                            add_num = p_add_num, add_name = p_add_name, add_suburb = p_add_suburb,
                            add_state = p_add_state, add_pc = p_add_pc, num_bedrooms = p_n_beds,
                            num_parking = p_n_park, num_bathrooms = p_n_baths,
                            parking_features = p_p_features, building_size = p_b_size,
                            land_size = p_l_size, seller = current_user.login_name, inspection_date = p_i_date,
                            description = p_desc, year_built = p_year)

            db.session.add(p_to_db)
            db.session.commit()

            # if everything is successful, redirects to property list
            return redirect(url_for('property_list'))
        else:
            error = "One or more fields have been entered incorrectly. Please try again."
            return render_template('addProperty.html', title = 'addProperty', error = error, form = form)
    
    return render_template('addProperty.html', title = 'addProperty', form = form)

@app.route('/editProperty/<p_id>', methods=['POST','GET'])
def edit_property(p_id):
    # edits property of selected user's one
    if current_user.is_anonymous:
        flash('Please login first')
        return redirect(url_for('login'))

    p = Property.query.filter_by(seller=current_user.login_name, id=p_id).all()
    print(p)

    form = PropertyForm()
    error = None

    if form.validate_on_submit():
        if check_edited_updates(form):
            # Success
            p_type = form.property_type.data
            p_add_unit = form.add_unit.data
            p_add_num = form.add_num.data
            p_add_name = form.add_name.data
            p_add_suburb = form.add_suburb.data
            p_add_state = form.add_state.data
            p_add_pc = form.add_pc.data
            p_n_beds = form.num_bedrooms.data
            p_n_baths = form.num_bathrooms.data
            p_n_park = form.num_parking.data
            p_p_features = form.parking_features.data
            p_b_size = form.building_size.data
            p_l_size = form.land_size.data
            p_desc = form.description.data
            p_year = form.year_built.data
            p_i_date = form.inspection_date.data

            # Cheap hack
            if p_type:
                p[0].property_type = p_type
            
            if p_add_unit or p_add_num or p_add_name or p_add_suburb or p_add_state or p_add_pc:
                p[0].add_unit = p_add_unit
                p[0].add_num = p_add_num
                p[0].add_name = p_add_name
                p[0].add_suburb = p_add_suburb
                p[0].add_state = p_add_state
                p[0].add_pc = p_add_pc

            if p_n_beds:
                p[0].num_bedrooms = p_n_beds

            if p_n_baths:
                p[0].num_bathrooms = p_n_baths

            if p_n_park:
                p[0].num_parking = p_n_park

            if p_p_features:
                p[0].parking_features = p_p_features

            if p_b_size:
                p[0].building_size = p_b_size

            if p_l_size:
                p[0].land_size = p_l_size

            if p_desc:
                p[0].description = p_desc

            if p_year:
                p[0].year_built = p_year

            if p_i_date:
                p[0].inspection_date = p_i_date

            db.session.commit()
            return redirect(url_for('property_list'))

        else:
            error = "One or more fields have been entered incorrectly. Please try again."
            return render_template('editProperty.html', title = 'editProperty', error = error, form = form, property = p)

    return render_template('editProperty.html', title = 'editProperty', form = form, property = p)
    
@app.route("/property")
def property_list():
    # returns list of properties from user

    properties = Property.query.filter_by(seller=current_user.login_name).all()
    
    return render_template('property.html', properties = properties)

@app.route("/removeProperty/<p_id>")
def remove_property(p_id):
    to_remove = Property.query.filter_by(id=p_id).delete()
    db.session.commit()
    return redirect(url_for('property_list'))


@app.route('/propertyImage/<p_id>', methods=['POST','GET'])
def property_image(p_id):
    if current_user.is_anonymous:
        flash('Please login first')
        return redirect(url_for('login'))

    p = Property.query.filter_by(seller=current_user.login_name, id=p_id).all()
    address = p[0].add_unit + '/' + p[0].add_num + ' ' + p[0].add_name + ' ' + p[0].add_suburb + ' ' + p[0].add_state + ' ' + p[0].add_pc
    print(address)

    img = Photos.query.filter_by(property_id=p_id).all()
    
    form = AddImageForm()
    error = None
    if form.validate_on_submit():
        print("adding Image")
        print(form.image.data)
        pic = Photos(photo = save_pic(form.image.data), property_id = p_id)
        db.session.add(pic)
        db.session.commit()

        return redirect(url_for('property_list'))

    return render_template('propertyImage.html', form=form, error=error, address=address, image=img)

def save_pic(form_pic):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_pic.filename)
    pic_fmt = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/propertyImage', pic_fmt)

    output_size = (1280, 720)
    i = Image.open(form_pic)
    i.thumbnail(output_size)
    i.save(picture_path)

    return pic_fmt

@app.route("/createAuction", methods=['GET', 'POST'])
@login_required
def createAuction():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User.query.filter_by(login_name=current_user.login_name).first()
        #id is automatically generated by database
        auctionDetails = AuctionDetails(PropertyID = random.random(), SellerID = current_user.login_name, AuctionStart = form.auctionStart.data, AuctionEnd = form.auctionEnd.data, 
            ReservePrice = form.reservePrice.data, MinBiddingGap = form.minBiddingGap.data)
        db.session.add(auctionDetails)
        db.session.commit()
        flash('Auction created for {form.reservePrice.data}!', 'success')
        return redirect(url_for('home'))

        cards=BankDetails.query.filter_by(id=card_number).all()
    return render_template('createAuction.html', form = form)