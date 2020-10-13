from userDetails import User, BankDetails, clear_session
from server import app, db, login_manager
from flask import render_template, request, redirect, url_for, flash
from flask_login import LoginManager,UserMixin, current_user, logout_user, login_required,login_user
from datetime import datetime
from forms import LoginForm

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


@app.route('/signup')
def signup():
    return render_template('signup.html')

    

# @app.route('logout')
# def logout():
#     logout_user()
#     return redirect(url_for('home'))

# @app.route('/signup', methods=['POST'])
# def signup():
#     try:
#         login_name = request.form['login_name']
#         password_1 = request.form['password1']
#         password_2 = request.form['password2']
#         address = request.form['address']

#         date_of_birth = request.form['date_of_birth']
#         user = User.query.filter_by(login_name=login_name).first()

#         if user or password_1!=password_2: # if a user is found, we want to redirect back to signup page so user can try again
#             return redirect(url_for('signup'))

#         # create a new user with the form data. Hash the password so the plaintext version isn't saved.
#         new_user = User(id=login_name, password=password_1, address=address, date_of_birth=datetime.strptime(date_of_birth,'%d%M%Y'))

#         # add the new user to the database
#         db.session.add(new_user)
#         db.session.commit()
#        return redirect('/home')