from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
from flask_migrate import Migrate

# Initialize SQLAlchemy for database management
db = SQLAlchemy()
DB_NAME = 'database.db'

def create_app():
    # Create an instance of the Flask application
    app = Flask(__name__)
    
    # Set secret key for session management and CSRF protection, not going to lie this is just good practice but not sure what is going on here :(
    app.config['SECRET_KEY'] = 'JEELER'
    
    # Configure the SQLAlchemy part of the app instance
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    
    # Initialize the app with SQLAlchemy
    db.init_app(app)

    # Import Blueprints for views and authentication
    from .veiws import views
    from .auth import auth

    # Register Blueprints
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    # Import models to ensure they are registered with SQLAlchemy
    from .models import User, Meal

    # Create the database if it doesn't exist
    create_database(app)
    
    # Set up Flask-Login
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'  # Redirect to login page if user is not authenticated
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        # Load the user from the database by user ID
        return User.query.get(int(id))
    
    # Set up Flask-Migrate for database migrations
    migrate = Migrate(app, db)
    
    # Import and create the Dash app within the Flask app context
    from .dash_app import create_dash_app
    create_dash_app(app)

    return app

def create_database(app):
    if not path.exists('website/' + DB_NAME):
        # Create the database within the application context
        with app.app_context():
            db.create_all()
        print('Created Database!')
