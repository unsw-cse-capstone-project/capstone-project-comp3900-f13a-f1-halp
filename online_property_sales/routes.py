from models/userDetails import app, db, User, BankDetails, login_manager
from flask import render_template, request, redirect, url_for
from flask_login import LoginManager,UserMixin
from datetime import datetime


@login_manager.user_loader
def load_user(id):
    return User.query.get(id)

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')


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