from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db  # Importing the database instance from __init__.py
from flask_login import login_user, login_required, logout_user, current_user

# Create a Blueprint for authentication-related routes.
auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])#so the login page can get information and post info / edit info in teh database or where ever
def login():
    if request.method == 'POST':  # Check if the form has been submitted.
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()  # Retrieve user by email.
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)  # Log in the user and create a session.
                return redirect(url_for('views.home'))  # Redirect to the home page after login.
            
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Email does not exist.', category='error')

    return render_template("login.html", user=current_user)  # Render the login template.

@auth.route('/logout', methods=['GET', 'POST'])
def logout():
    logout_user()  # End the user session.
    return redirect(url_for('auth.login'))  # Redirect to the login page after logout.

@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':  # Check if the sign-up form has been submitted.
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(email=email).first()  # Check if the email already exists.
        if user:
            flash('Email already exists.', category='error')
        elif len(email) < 4:
            flash('Email must be greater than 3 characters.', category='error')
        elif len(first_name) < 2:
            flash('First name must be greater than 1 character.', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters.', category='error')
        else:
            # Create a new user instance and hash the password for security.
            new_user = User(email=email, first_name=first_name, password=generate_password_hash(password1))
            db.session.add(new_user)  # Add the new user to the database session.
            db.session.commit()  # Commit changes to the database.
            login_user(new_user, remember=True)  # Log in the new user.
            flash('Account created!', category='success')
            return redirect(url_for('views.home'))  # Redirect to the home page after signing up.

    return render_template('sign_up.html', user=current_user)  # Render the sign-up template.
