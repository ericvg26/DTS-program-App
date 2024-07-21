# models.py contains the database schema for the application.
from . import db  # Importing the database instance from the package
from flask_login import UserMixin  # Provides default implementations for methods expected by Flask-Login
from sqlalchemy import Date  # Importing Date type from SQLAlchemy for date fields
from datetime import datetime  # Importing datetime to use in default date values

# User model, each instance represents a user in the database
class User(db.Model, UserMixin):  # Inherits from db.Model for ORM and UserMixin for user management
    # User goals for daily intake, nullable to allow goals to be optional, with default values if not set
    daily_protein_goal = db.Column(db.Integer, nullable=True, default=100)
    daily_calorie_goal = db.Column(db.Integer, nullable=True, default=1000)
    # Primary key for user records
    id = db.Column(db.Integer, primary_key=True)
    # Unique email for user authentication
    email = db.Column(db.String(150), unique=True)
    # Hashed password for security
    password = db.Column(db.String(150))
    # User's first name for personalization
    first_name = db.Column(db.String(150))
    # One-to-many relationship with the Meal model, 'dynamic' lazy loading allows querying
    meals = db.relationship('Meal', backref='user', lazy='dynamic')

# Meal model, each instance represents a meal recorded by a user
class Meal(db.Model):  # Inherits from db.Model for ORM
    # Primary key for meal records
    id = db.Column(db.Integer, primary_key=True)
    # Date of the meal, defaults to the current date, only date no time needed
    date = db.Column(Date, default=datetime.utcnow().date)
    # The type of meal or a short description
    meal_type = db.Column(db.String, nullable=False)
    # Amount of protein in grams, must be a non-negative number
    protein = db.Column(db.Integer, nullable=False)
    # Caloric content of the meal, must be a non-negative number
    calories = db.Column(db.Integer, nullable=False)
    # Foreign key linking a meal to a user, establishing a many-to-one relationship
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    # The backref in the User model creates a reverse link from Meal back to User
