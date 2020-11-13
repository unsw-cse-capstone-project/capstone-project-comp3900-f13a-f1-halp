from models import *
from server import app, db, login_manager, mail
from flask import render_template, request, redirect, url_for, flash
from flask_login import LoginManager,UserMixin, current_user, logout_user, login_required,login_user
from datetime import datetime, timedelta
from sqlalchemy import func, desc
from forms import *
from validateProperty import *
from flask_mail import Message
# from PIL import Image
import random
import sys
import os
import secrets
from apscheduler.schedulers.background import BackgroundScheduler
from schedule import hourlyEmail
from datetime import datetime, timedelta

# initial_db()

# def end(AuctionID_):

#     auction = AuctionDetails.query.filter_by(id = AuctionID_).first_or_404()
#     seller =  User.query.filter_by(id = auction.SellerID).first_or_404()

#     msg = Message("Hello", sender = 'AuctionWorldWideWeb@gmail.com', recipients=[seller.email])
#     msg.body = "Auction " +  str(AuctionID_) + " has ended"
#     mail.send(msg)

# def hourlyEmail():
#     end(1)

sched = BackgroundScheduler(daemon=True)
sched.add_job(hourlyEmail,'interval',minutes=1)
sched.start()

@app.route('/')
@app.route('/home')
def home():

    # msg = Message("Hello", 
    #                 sender = 'AuctionWorldWideWeb@gmail.com',
    #                 recipients=["unswroy@gmail.com"])

    # msg.body = "Hello Flask message sent from Flask-Mail"
    # mail.send(msg)
    since = datetime.now() - timedelta(hours=1)
    auctions = AuctionDetails.query.filter(AuctionDetails.AuctionEnd<=datetime.now(), AuctionDetails.AuctionEnd>=since)
    for auction in auctions:
        flash(auction.id)
    # flash(f"Users are able to login with case insensitive login name, which means Tom123@g and tOM123@G is the same user. We have two users who have same password as their login_name in our db: Tom123@g and Cloudia0@g",'info')
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

            if not form.validate_date_of_birth(form.date_of_birth.data):
                flash(f'The date of birth should be smaller than current time','danger')
                return render_template('signup.html', title='signup', form=form)

            user = User(login_name=form.login_name.data, email=form.email.data, address = form.address.data, date_of_birth = form.date_of_birth.data, phone_number=form.phone_number.data)
            user.set_password(form.password.data)
            db.session.add(user)
            db.session.commit()
            flash('Congratulations, you are now a registered user!','success')
            return redirect(url_for('login'))
        else:
            flash('The username has been taken, please input another one','danger')
    return render_template('signup.html', title='signup', form=form)

@app.route('/search', methods=['POST','GET'])
@login_required
def search():
    form=searchForm()
    available_suburbs=db.session.query(Property.add_suburb).distinct(Property.add_suburb)
    #load all suburbs in db and initial with an empty value
    form.suburb.choices=[("")]+[(i.add_suburb) for i in available_suburbs]

    full_list = db.session.query(Property,AuctionDetails,func.max(Bid.Amount).label('highestBid'))\
                        .outerjoin(AuctionDetails, AuctionDetails.PropertyID==Property.id)\
                        .outerjoin(Bid, Bid.AuctionID == AuctionDetails.id)\
                        .group_by(Property.id)
    property_Id=[]

    #auction time -> auction id list -> property id list
    #suburb -> property id list
    #property id list -> property, AuctionDetails objects left?join(AuctionDetails)
    if form.validate_on_submit():
        if form.clear.data:
            form.auction_before.raw_data=['']
            form.auction_after.raw_data=['']
            form.suburb.data=''
            return render_template('search.html', title='search', form=form, properties=full_list)

        elif form.submit.data:
            input_form=False
            before=form.auction_before.data
            after=form.auction_after.data
            suburb = form.suburb.data
            
            if before or after:
                input_form=True
                if before and not after :
                    temp = db.session.query(AuctionDetails.PropertyID).filter(AuctionDetails.AuctionStart<=before)
                    property_Id = property_Id + [int(i.PropertyID) for i in temp]
                elif after and not before:
                    temp = db.session.query(AuctionDetails.PropertyID).filter(AuctionDetails.AuctionEnd>=after)
                    property_Id = property_Id + [int(i.PropertyID) for i in temp]
                elif before and after:
                    temp = db.session.query(AuctionDetails.PropertyID).filter(AuctionDetails.AuctionStart<=before,
                        AuctionDetails.AuctionEnd>=after)
                    property_Id = property_Id + [int(i.PropertyID) for i in temp]

            if suburb:
                temp= db.session.query(Property.id).filter(Property.add_suburb==suburb)
                suburb_Id=[int(i.id) for i in temp]

                if input_form==True:
                    list_as_set=set(property_Id)
                    intersection = list_as_set.intersection(suburb_Id)
                    property_Id= list(intersection)
                else:
                    property_Id = property_Id + suburb_Id

                input_form=True

            if input_form==True:
                property_with_auction = db.session.query(Property,AuctionDetails,func.max(Bid.Amount).label('highestBid'))\
                                                    .filter(Property.id.in_(property_Id))\
                                                    .outerjoin(AuctionDetails, AuctionDetails.PropertyID==Property.id)\
                                                    .outerjoin(Bid, Bid.AuctionID == AuctionDetails.id)\
                                                    .group_by(Property.id)
                        
            else: 
                property_with_auction =full_list

            return render_template('search.html', title='search', form=form, properties=property_with_auction)

    return render_template('search.html', title='search', form=form, properties=full_list)

@app.route('/viewProperty/<property_id>', methods=['POST','GET'])
def viewProperty(property_id):
    
    property_info = Property.query.filter_by(id=property_id).first_or_404()
    seller = User.query.get(property_info.seller)
    auction = AuctionDetails.query.filter_by(PropertyID = property_id).first()
    if auction:
        highestBid = Bid.query.filter_by(AuctionID = auction.id).order_by(desc(Bid.Amount)).first()
        registered = RegisteredAssociation.query.filter_by(PropertyID = property_id, RegisteredBidderID=current_user.id).first()
    else:
        highestBid = None
        registered = None
    
    return render_template('viewProperty.html', title='View Property', property=property_info, seller= seller, auction=auction, highestBid=highestBid, registered=registered)


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
                    return redirect(url_for('home'))
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
    cards = BankDetails.query.filter_by(user_id = current_user.id).all()

    if form.validate_on_submit():
        #change password after confirmming old password first
        if form.login_name.data:
            if form.validate_username(form.login_name.data, user.id):
                user.set_login_name(form.login_name.data)
            else:
                return render_template('account.html', title='account', form=form, user=user, cards = cards)

        user.set_address(form.address.data)
        user.set_phone_number(form.phone_number.data)
        user.set_date_of_birth( datetime.strptime(form.date_of_birth.data,'%d/%m/%Y'))
        user.set_email(form.email.data)
        user.set_id_confirmation(form.id_confirmation.data)
        db.session.commit()

        if not form.id_confirmation.data or len(cards) == 0:
            flash(f'To do more actions in our system, it is required to enter the your identification and have at least one card', 'danger')
            return render_template('account.html', title='account', form=form, user=user, cards = cards)
        
        return redirect(url_for('home'))

    elif request.method == 'GET':
        form.address.data = current_user.address
        form.date_of_birth.data = current_user.date_of_birth.strftime("%d/%m/%Y")
        form.phone_number.data = current_user.phone_number
        form.email.data = current_user.email
        form.id_confirmation.data = current_user.id_confirmation
        if len(current_user.cards.all()) == 0:
            flash(f'You have not entered a credit card before, please upload one with full bank details.', 'info')

    return render_template('account.html', title='account', form=form, user=user, cards = cards)

@app.route('/editBankDetails/<card_id>', methods=['POST','GET'])
@login_required
def editBankDetails(card_id):

    form = BankDetailsForm()
    card = db.session.query(BankDetails).get(card_id)
    user = User.query.filter_by(login_name=current_user.login_name).first_or_404()

    if form.validate_on_submit():
        
        holder_fname =  form.holder_fname.data
        holder_lname =  form.holder_lname.data
        cvc =  form.cvc.data
        expire_date =  form.expire_date.data

        if not form.validate_expire_date(expire_date):
            flash(f'The expire date should be greater than current time','danger')
            return render_template('editBankDetails.html', title='editBankDetails', form=form, card = card)

        if holder_fname:
            card.set_fname(holder_fname)
        if holder_lname:
            card.set_lname(holder_lname)
        if cvc:
            card.set_cvc(cvc)
        if expire_date:
            card.set_expire_date(expire_date)

        db.session.commit()
        cards = BankDetails.query.filter_by(user_id = current_user.id).all()
        return redirect(url_for('account', form=form, user=user, cards = cards, login_name = current_user.login_name))

    elif request.method == 'GET':
        form.card_number.data = card.id
        form.holder_fname.data = card.holder_fname
        form.holder_lname.data = card.holder_lname
        form.expire_date.data = card.expire_date
        form.cvc.data = card.cvc

    return render_template('editBankDetails.html', title='editBankDetails', form=form, card = card)

@app.route('/addBankDetail', methods=['POST','GET'])
@login_required
def addBankDetail():

    form = BankDetailsForm()
    user = User.query.filter_by(login_name=current_user.login_name).first_or_404()

    if form.validate_on_submit():
        
        card_number = form.card_number.data
        holder_fname =  form.holder_fname.data
        holder_lname =  form.holder_lname.data
        cvc =  form.cvc.data
        expire_date =  form.expire_date.data

        if not form.validate_expire_date(expire_date):
            flash(f'The expire date should be greater than current time','danger')
            return render_template('addBankDetail.html', title='addBankDetail', form=form)

        if len(card_number)>0:
            new_card=True
            old_card=BankDetails.query.get(card_number)
            #this card already in our database
            if old_card!=None:
                new_card=False
                flash(f"This card already registered by other user", 'danger')
                return render_template('addBankDetail.html', title='addBankDetail', form=form)

            #this is a new card, all the info should be inputed
            if new_card == True:
                if holder_fname and holder_lname and cvc and expire_date  and expire_date:
                    bank = BankDetails(id=card_number,holder_fname=holder_fname, holder_lname=holder_lname,cvc=cvc, expire_date=expire_date, user=user)
                    flash("Congraduation! you add a new credit card to your account",'success')
                    db.session.add(bank)
                    db.session.commit()
                    cards = BankDetails.query.filter_by(user_id = current_user.id).all()
                    return redirect(url_for('account', form=form, user=user, cards = cards, login_name = current_user.login_name))
                else:
                    flash(f"This is a new card, the full info of the card should be inserted! And please make sure the date format is correct",'danger')
                    return render_template('addBankDetail.html', title='addBankDetail', form=form)

    return render_template('addBankDetail.html', title='addBankDetail', form=form)

@app.route("/removetBankDetails/<card_id>")
@login_required
def removetBankDetails(card_id):
    BankDetails.query.filter_by(id=card_id).delete()
    db.session.commit()

    form = AccountForm()
    user = User.query.filter_by(login_name=current_user.login_name).first_or_404()
    cards = BankDetails.query.filter_by(user_id = current_user.id).all()

    return redirect(url_for('account', form=form, user=user, cards = cards, login_name = current_user.login_name))


@app.route('/addProperty', methods=['GET', 'POST'])
@login_required
def add_property():
    form = PropertyForm()

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
                            land_size = p_l_size, seller = current_user.id, inspection_date = p_i_date,
                            description = p_desc, year_built = p_year, status = 'auction')

            db.session.add(p_to_db)
            db.session.commit()

            # if everything is successful, redirects to property list
            return redirect(url_for('property_list'))
        else:
            flash(f"One or more fields have been entered incorrectly. Please try again.",'danger')
            return render_template('addProperty.html', title = 'addProperty', form = form)
    
    return render_template('addProperty.html', title = 'addProperty', form = form)

@app.route('/editProperty/<p_id>', methods=['POST','GET'])
@login_required
def edit_property(p_id):
    # edits property of selected user's one

    p = Property.query.filter_by(seller=current_user.id, id=p_id).all()
    print(p)

    form = PropertyForm()

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
            flash(f'One or more fields have been entered incorrectly. Please try again.','danger')
            return render_template('editProperty.html', title = 'editProperty', form = form, property = p)

    return render_template('editProperty.html', title = 'editProperty', form = form, property = p)
    
@app.route("/property")
def property_list():
    # returns list of properties from user

    my_properties = db.session.query(Property,AuctionDetails,func.max(Bid.Amount).label('highestBid'))\
                        .filter(Property.seller==current_user.id)\
                        .outerjoin(AuctionDetails, AuctionDetails.PropertyID==Property.id)\
                        .outerjoin(Bid, Bid.AuctionID == AuctionDetails.id)\
                        .group_by(Property.id)

    propertiesID_registered=RegisteredAssociation.query.filter_by(RegisteredBidderID=current_user.id).all()
    registeredID_list = [ i.PropertyID for i in propertiesID_registered ]
    if len(registeredID_list) == 0:
        registered_properties =None
    else:
        registered_properties = db.session.query(Property,AuctionDetails,func.max(Bid.Amount).label('highestBid'))\
                                .filter(Property.id.in_(registeredID_list))\
                                .outerjoin(AuctionDetails, AuctionDetails.PropertyID==Property.id)\
                                .outerjoin(Bid, Bid.AuctionID == AuctionDetails.id)\
                                .group_by(Property.id)

    time_shift_1hr = datetime.now() + timedelta(hours=1)
    # needs to add in auction start time and end time

    return render_template('property.html', properties = my_properties,registered_properties=registered_properties, now_date = time_shift_1hr)

@app.route("/changeStatus/<p_id>")
def change_status(p_id):
    to_change = Property.query.filter_by(id=p_id).all()
    if to_change[0].status == "auction":
        to_change[0].status = "sold"
    else:
        to_change[0].status = "auction"
    db.session.commit()
    return redirect(url_for('property_list'))

@app.route("/removeProperty/<p_id>")
def remove_property(p_id):
    to_remove = Property.query.filter_by(id=p_id).delete()
    db.session.commit()
    return redirect(url_for('property_list'))

@app.route("/removeRegisteredProperty/<p_id>")
def removeRegisteredProperty(p_id):
    to_remove = RegisteredAssociation.query.filter_by(PropertyID=p_id, RegisteredBidderID=current_user.id).delete()
    db.session.commit()
    return redirect(url_for('property_list'))

@app.route('/propertyImage/<p_id>', methods=['POST','GET'])
@login_required
def property_image(p_id):

    p = Property.query.filter_by(seller=current_user.id, id=p_id).all()
    # address = p[0].add_unit + '/' + p[0].add_num + ' ' + p[0].add_name + ' ' + p[0].add_suburb + ' ' + p[0].add_state + ' ' + p[0].add_pc
    # print(address)

    img = Photos.query.filter_by(property_id=p_id).all()
    
    form = AddImageForm()
    if form.validate_on_submit():
        print("adding Image")
        print(form.image.data)
        pic = Photos(photo = save_pic(form.image.data), property_id = p_id)
        db.session.add(pic)
        db.session.commit()

        return redirect(url_for('property_list'))

    return render_template('propertyImage.html', form=form, image=img, property=p_id)

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

@app.route("/removeImage/<p_id>/<i_id>")
def remove_image(p_id, i_id):
    img = Photos.query.get(i_id)
    os.remove(os.path.join('static/propertyImage/', img.photo))
    Photos.query.filter_by(id=i_id).delete()
    db.session.commit()
    return redirect(url_for('property_image', p_id = p_id))
    
@app.route("/createAuction", methods=['GET', 'POST'])
@login_required
def createAuction():
    if current_user.is_anonymous:
        flash('Please login first')
        return redirect(url_for('login'))

    PropertyID_ = request.args.get('PropertyID')

    if PropertyID_ == None:
        flash('Please Create the property first')
        return redirect(url_for('add_property'))

    auction = AuctionDetails.query.filter_by(PropertyID = PropertyID_).first()
    if auction != None:
        return redirect(url_for('changeAuctionDetails', AuctionID_ = auction.id))

    form = RegistrationForm()
    if form.validate_on_submit():
        if form.auctionStart.data < datetime.now() or form.auctionStart.data > form.auctionEnd.data:
            flash('Please set valid auction time', 'danger')
            return render_template('createAuction.html', form = form)
        user = User.query.filter_by(login_name=current_user.login_name).first_or_404()
        auctionDetails = AuctionDetails(PropertyID = PropertyID_, SellerID = current_user.id, AuctionStart = form.auctionStart.data, AuctionEnd = form.auctionEnd.data, 
            ReservePrice = form.reservePrice.data, MinBiddingGap = form.minBiddingGap.data)
        db.session.add(auctionDetails)
        db.session.commit()
        flash('The auction was successfully created.', 'success')
        return redirect(url_for('home'))

        cards=BankDetails.query.filter_by(id=card_number).all()
    return render_template('createAuction.html', form = form)

@app.route("/auction", methods=['GET', 'POST'])
def auctions():
    if current_user.is_anonymous:
        flash('Please login first')
        return redirect(url_for('login'))

    auctions = AuctionDetails.query.filter_by(SellerID = current_user.id).all()
    return render_template('auctions.html', auctions=auctions)

@app.route("/editAuction/<AuctionID_>", methods=['GET', 'POST'])
def changeAuctionDetails(AuctionID_):
    if current_user.is_anonymous:
        flash('Please login first')
        return redirect(url_for('login'))

    auction = AuctionDetails.query.filter_by(id = AuctionID_).first_or_404()

    form = RegistrationForm()
    if form.validate_on_submit():
        auction = AuctionDetails.query.filter_by(id = AuctionID_).first_or_404()
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
    
@app.route("/deleteAuction/<AuctionID_>", methods=['GET', 'POST'])
@login_required
def deleteAuction(AuctionID_):
    if current_user.is_anonymous:
        flash('Please login first')
        return redirect(url_for('login'))

    auction = AuctionDetails.query.filter_by(id = AuctionID_).first_or_404()
    db.session.delete(auction)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('home'))

@app.route("/viewAuction/<AuctionID_>", methods=['GET', 'POST'])
@login_required
def viewAuction(AuctionID_):

    user = User.query.filter_by(login_name=current_user.login_name).first_or_404()
    auction = AuctionDetails.query.filter_by(id = AuctionID_).first_or_404()
    property_ = Property.query.get(auction.PropertyID)

    if auction.SellerID == current_user.id:
        return redirect(url_for('changeAuctionDetails', AuctionID_ = auction.id))

    if auction.AuctionEnd > datetime.now():
        registeredBefore = RegisteredAssociation.query.filter_by(RegisteredBidderID=user.id, PropertyID =property_.id).first()
        if not registeredBefore:
            flash(f'Congrats! You registered the auction successfully, this property is in your watching list right now.', 'success')
            register = RegisteredAssociation(RegisteredBidderID=user.id, PropertyID = property_.id)
            db.session.add(register)
            db.session.commit()
    else:
        flash(f'This auction has already ended', 'warning')
        return redirect(url_for('home'))

    if auction.AuctionStart > datetime.now():
        flash(f'This auction has not started yet', 'info')
        registered = RegisteredAssociation.query.filter_by(PropertyID = property_.id, RegisteredBidderID=current_user.id).first()
        return render_template('viewProperty.html', title='View Property', property=property_, seller= auction.SellerID, auction=auction, highestBid= None, registered=registered)


    highestBid = Bid.query.filter_by(AuctionID = AuctionID_).order_by(Bid.Amount)
    highestAmount = 0
    for amount in highestBid:
        highestAmount = amount.Amount

    myBid = 0
    myBids = Bid.query.filter_by(AuctionID = AuctionID_, BidderID = user.id).order_by(Bid.Amount)
    for amount in myBids:
        myBid = amount.Amount

    nextLow = auction.MinBiddingGap + highestAmount

    form = MakeBidForm()
    if form.validate_on_submit():
        if form.newBid.data < nextLow:
            flash(f'Please input the correct amount', 'danger')
            bid=None
        else:
            bid = Bid(BidderID = current_user.id, AuctionID = AuctionID_, Amount = form.newBid.data)
            db.session.add(bid)
            db.session.commit()
            flash(f'Your Bid has been accepted!', 'success')

        return render_template('viewProperty.html', title='View Property', property=property_, seller= auction.SellerID, auction=auction, highestBid= bid)

    return render_template('viewAuction.html', form = form, highestBid = highestAmount, myBid = myBid, nextLow = nextLow)

@app.route("/endAuction/<AuctionID_>", methods=['GET', 'POST'])
@login_required
def endAuction(AuctionID_):
    hourlyEmail()
    return redirect(url_for('home'))
    # auction = AuctionDetails.query.filter_by(id = AuctionID_).first_or_404()
    # seller =  User.query.filter_by(id = auction.SellerID).first_or_404()

    # msg = Message("Hello", sender = 'AuctionWorldWideWeb@gmail.com', recipients=[seller.email])
    # msg.body = "Auction " +  str(AuctionID_) + " has ended"
    # mail.send(msg)

    # highestBid = Bid.query.filter_by(AuctionID = AuctionID_).order_by(desc(Bid.Amount)).first()
    # highestBidder = User.query.filter_by(id = highestBid.BidderID).first_or_404()
    # msg = Message("Hello", sender = 'AuctionWorldWideWeb@gmail.com', recipients=[highestBidder.email])
    # msg.body = "You are highest Bidder for auction " + str(AuctionID_)
    # mail.send(msg)

    # otherBids = Bid.query.filter_by(AuctionID = AuctionID_)
    # for otherBid in otherBids:
    #     otherBidder = User.query.filter_by(id = otherBid.BidderID).first_or_404()
    #     if otherBidder != highestBidder:
    #         otherBidder = User.query.filter_by(id = highestBid.BidderID).first_or_404()
    #         msg = Message("Hello", sender = 'AuctionWorldWideWeb@gmail.com', recipients=[otherBidder.email])
    #         msg.body = "You have not worn auction " + str(AuctionID_)
    #         mail.send(msg)

    # return redirect(url_for('home'))



# should call this function twice. one for all passed bidders, one for the winner
# recipients_id should be a list of user id who are bidders in this auction
# if win is true -> send success email with info
# else -> bad luck email
def send_email(recipients_id, win, auctionId):

    auction_info = AuctionDetails.query.get(auctionId)
    property_info = Property.query.get(auction_info.PropertyID)
    seller = User.query.get(auction_info.SellerID)
    recipients_info = db.session.query(User.email,User.login_name).filter(User.id.in_(recipients_id))

    if win == True:
        emails = [i for (i,j) in recipients_info]
        login_names = [j for (i,j) in recipients_info]

        msg = Message("Congradulations! You win the auction",
                        recipients=emails)
        msg.html=render_template('successFeedback.html',
                                            receiver=login_names, seller=seller, property=property_info, auction=auction_info )
        mail.send(msg)
    else:
        for (x,y) in recipients_info:
            msg = Message("Unfortunately! You did not win the auction",recipients=[x])
            msg.html = render_template('unfortunatelyFeedback.html',receiver=y, seller=seller, property=property_info, auction=auction_info )
            mail.send(msg)

def if_have_cards(user_id):
    user=db.session.query(User).get(user_id)
    cards = user.cards.count()
    if cards > 0 and user.id_confirmation:
        return True
    else:
        return False