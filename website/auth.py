from flask import Blueprint, render_template, request, flash, redirect, url_for
from .model import User
from werkzeug.security import generate_password_hash, check_password_hash # This is a way of securing the password such that you are never storing password in plain text
#Hasing fcuntion is a one way func that does not have an inverse, we can only generate the hash with the password. We can only check if the password we typed in is correct by making it go through the hashing function.
from . import db
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth',__name__)

#How to pass the values to the templates,
# We want to make sure login and sign up are able to handle the post request
@auth.route('/login', methods = ['GET','POST'])
def login():
    if request.method == 'POST':
        #Verifying if the user exists in our database
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in Successfully!', category='success')
                login_user(user, remember=True ) # Remembers the fact that the user logged in until the user clears the browsing history or the session, the user doesnot have to login everytime
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect Password, try again', category='error')
        else:
            flash('User Does Not Exist', category = 'error')
    return render_template('login.html', user = current_user)

@auth.route('/logout')
@login_required #All this does is make sure that we cannot access this root untill we login
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/sign-up',methods = ['GET','POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        firstName = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        #Verifying that the user doesnot already exist in out database
        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email Already Exists', category='error')
        elif len(email) < 4 :
            flash('Email must be greater than 4 characters', category = 'error')
        elif len(firstName) < 2:
            flash('firstName must be greater than 1 characters', category = 'error')
        elif password1 != password2:
            flash('Your passwords don\'t match', category = 'error')
        elif len(password1) < 7:
            flash('Your Password must be atleast 7 characters', category = 'error')
        else:
            new_user = User(email = email, first_name=firstName, password=generate_password_hash(password1,method='sha256'))
            #Adding the account to the database
            db.session.add(new_user)
            db.session.commit() # this will create a new user for us and then we will redirect it to the new page
            flash('Account Created', category = 'success')
            login_user(new_user, remember=True )
            return redirect(url_for('views.home'))

    return render_template('sign_up.html', user=current_user)