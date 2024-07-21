from flask import Blueprint, request, redirect, url_for, flash, render_template
from flask_login import login_required, current_user
from .models import User, Meal
from . import db
from .forms import MealForm, GoalForm
from datetime import datetime

# Setting up a Blueprint named 'views'. This will handle the routes for the main functionality of the site.
views = Blueprint('views', __name__)

# Route for the home page which requires user to be logged in to access it.
@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    # Fetching all users, used for admin purposes or to display user-related data.
    users = User.query.all()
    
    # Initializing forms with prefixes to avoid naming conflicts.
    meal_form = MealForm(prefix='meal_form')
    goal_form = GoalForm(prefix='goal_form')

    # If the 'Add Meal' form is submitted in home.html and valid, process the form data.
    if 'meal_submit' in request.form and meal_form.validate_on_submit():
        # Create a new meal record for the current user.
        new_meal = Meal(
            date=datetime.utcnow().date(),  # Using UTC date as the standard.
            meal_type=meal_form.meal_type.data,
            protein=meal_form.protein.data,
            calories=meal_form.calories.data,
            user_id=current_user.id
        )
        db.session.add(new_meal)  # Adding the meal to the session.
        try:
            db.session.commit()  # Committing changes to the database.
            flash('Meal added successfully!', category='success')
        except Exception as e:
            db.session.rollback()  # Rolling back in case of error.
            flash(f'An error occurred: {e}', category='error')
        return redirect(url_for('views.home'))  # Refreshing the page to show updated info.

    # If the 'Set Goals' form is submitted and valid, process the form data.
    if 'goal_submit' in request.form and goal_form.validate_on_submit():
        # Update the current user's daily goals.
        current_user.daily_protein_goal = goal_form.daily_protein.data
        current_user.daily_calorie_goal = goal_form.daily_calories.data
        try:
            db.session.commit()  # Committing changes to the user's goals.
            flash('Your goals have been updated!', category='success')
        except Exception as e:
            db.session.rollback()
            flash(f'An error occurred: {e}', category='error')
        return redirect(url_for('views.home'))

    # Calculate the total protein and calories consumed by the user today.
    today = datetime.utcnow().date()
    meals = Meal.query.filter_by(user_id=current_user.id, date=today).all()
    total_protein = sum(meal.protein for meal in meals)
    total_calories = sum(meal.calories for meal in meals)

    # Pre-fill the goal form with current user's goals for easier updating.
    goal_form.daily_protein.data = current_user.daily_protein_goal
    goal_form.daily_calories.data = current_user.daily_calorie_goal

    # Render the home page template with all necessary data.
    return render_template("home.html", meal_form=meal_form, goal_form=goal_form, meals=meals, total_protein=total_protein, total_calories=total_calories, users=users, user=current_user)

# Route for the 'Data' page that shows the progress of all users.
# This route requires the user to be logged in to access it.
@views.route('/data', methods=['GET', "POST"])
@login_required
def data():
    # An empty list to store progress data for all users.
    users_progress = []
    
    # Query all users from the database.
    users = User.query.all()
    
    # Loop through each user to calculate their daily progress.
    for user in users:
        # Get all meals for the user for the current date.
        meals = Meal.query.filter_by(user_id=user.id, date=datetime.utcnow().date()).all()
        
        # Calculate the total protein and calories consumed by the user today.
        total_protein = sum(meal.protein for meal in meals)
        total_calories = sum(meal.calories for meal in meals)
        
        # Calculate the percentage of the protein and calorie goals achieved.
        # If the user hasn't set a goal, default the percentage to 0.
        protein_percentage = (total_protein / user.daily_protein_goal) * 100 if user.daily_protein_goal else 0
        calorie_percentage = (total_calories / user.daily_calorie_goal) * 100 if user.daily_calorie_goal else 0
        
        # Store the progress data in the list, ensuring the percentage doesn't exceed 100%.
        users_progress.append({
            'user': user,
            'protein_percentage': min(protein_percentage, 100),
            'calorie_percentage': min(calorie_percentage, 100),
        })

    # Render the 'data.html' template, passing the list of users and their progress.
    # This allows the template to display each user's progress visually,  with progress bars.
    return render_template("data.html", users=users, user=current_user, users_progress=users_progress)


#this code allows me to update user data in my data page
@views.route('/update_user/<int:user_id>', methods=['POST'])
@login_required
def update_user(user_id):
    # Only allow admins or the user themselves to update user info
    if current_user.id != user_id:
        flash('You do not have permission to update this user.', 'error')
        return redirect(url_for('views.data'))

    user_to_update = User.query.get_or_404(user_id)
    updated_name = request.form.get('name')
    updated_email = request.form.get('email')

    # may want to add additional validation for the updated values here

    user_to_update.first_name = updated_name
    user_to_update.email = updated_email

    try:
        db.session.commit()
        flash('User updated successfully!', 'success')
    except:
        db.session.rollback()
        flash('There was an issue updating the user.', 'error')
    
    return redirect(url_for('views.data'))  

#incase the user messes up on the home page they can restart their meal tracking and delete their meals that day
@views.route('/clear_daily_meals', methods=['POST'])
@login_required
def clear_daily_meals():
    today = datetime.utcnow().date()
    Meal.query.filter_by(user_id=current_user.id, date=today).delete()
    db.session.commit()
    flash('Your daily meals have been cleared.', 'info')
    return redirect(url_for('views.home'))

#THIS IS ONLY HERE TO DELETE USERS WHEN NECESARY 
@views.route('/delete_user/<int:user_id>', methods=['POST'])
@login_required
def delete_user(user_id):
    
    user = User.query.get(user_id)
    if user is None:
        flash('User not found.', category='error')
        return redirect(url_for('index'))  # Redirect if the user does not exist

    db.session.delete(user)#deleting that user 
    try:
        db.session.commit()
        flash('User deleted successfully.', category='success')
    except Exception as e:
        db.session.rollback()
        flash('Error deleting user.', category='error')
        print(e)  # Logging the exception can be helpful for debugging

    return redirect(url_for('views.data'))  # Redirect to the homepage or user list page

@views.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', user=current_user)

@views.route('/dash')
@login_required
def dash():
    return redirect(url_for('views.dash_with_user', user_id=current_user.id))

@views.route('/dash_app')
@login_required
def dash_app():
    return render_template('dash_app.html', user=current_user)

@views.route('/help')
def help():
    return render_template('help.html', user=current_user)

