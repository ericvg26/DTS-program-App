#these are the forms being used on my home page
# FlaskForm is an extension of Flask that adds support for quickly building web forms with WTForms.
from flask_wtf import FlaskForm
# These are the field types included from WTForms that you'll use to create form classes.
from wtforms import StringField, IntegerField, SelectField, SubmitField
# Validators are used to apply validation rules to the fields.
from wtforms.validators import DataRequired, NumberRange

# MealForm class inherits from FlaskForm. It's a form for submitting meals with validation rules.
class MealForm(FlaskForm):
    # StringField corresponds to an <input type="text"> in HTML.
    # 'Meal Description' is the label for the field.
    # DataRequired validator ensures that the field cannot be submitted empty.
    meal_type = StringField('Meal Description', validators=[DataRequired()])
    
    # IntegerField is for numeric inputs. It will return a Python `int` type.
    # It ensures that the data entered is an integer and is required.
    protein = IntegerField('Protein (grams)', validators=[DataRequired()])
    
    # Similar to the protein field, but for calories.
    calories = IntegerField('Calories', validators=[DataRequired()])
    
    # SubmitField represents an <input type="submit">, used to submit the form.
    submit = SubmitField('Add Meal')

# GoalForm class allows users to set their daily nutritional goals.
class GoalForm(FlaskForm):
    # Field for daily protein goal. NumberRange ensures value is >= 0. although this does not work for some reason you can still add negative numbers, weird
    daily_protein = IntegerField('Protein  (grams)', validators=[DataRequired(), NumberRange(min=0)])
    
    # Field for daily calorie goal with similar validation.
    daily_calories = IntegerField('Calories (calories)', validators=[DataRequired(), NumberRange(min=0)])
    
    # Submit button for the form.
    submit = SubmitField('Update Goals')
