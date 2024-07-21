import dash
from dash import dcc, html, Input, Output
import plotly.express as px
import pandas as pd
from datetime import datetime
from .models import User, Meal
from flask import current_app as app
from flask_login import current_user

def get_user_data(user_id):
    user_meals = Meal.query.filter_by(user_id=user_id).all()
    return user_meals

def calculate_goal_achievement(user, date):
    meals_today = Meal.query.filter_by(user_id=user.id, date=date).all()
    total_protein = sum(meal.protein for meal in meals_today)
    total_calories = sum(meal.calories for meal in meals_today)
    
    protein_goal_met = int(total_protein >= user.daily_protein_goal)
    calorie_goal_met = int(total_calories >= user.daily_calorie_goal)
    
    return protein_goal_met, calorie_goal_met

def get_goal_achievement_data(user_id):
    user_meals = get_user_data(user_id)
    
    data = {
        'date': [],
        'goal': [],
        'met': []
    }
    
    user = User.query.get(user_id)
    
    unique_dates = set([meal.date for meal in user_meals])
    
    for date in unique_dates:
        protein_goal_met, calorie_goal_met = calculate_goal_achievement(user, date)
        
        data['date'].append(date)
        data['goal'].append('Protein')
        data['met'].append(protein_goal_met)
        
        data['date'].append(date)
        data['goal'].append('Calories')
        data['met'].append(calorie_goal_met)
    
    df = pd.DataFrame(data)
    return df

def get_nutrition_data(user_id):
    user_meals = get_user_data(user_id)
    
    data = {
        'date': [],
        'protein': [],
        'calories': []
    }
    
    meal_by_date = {}
    for meal in user_meals:
        if meal.date not in meal_by_date:
            meal_by_date[meal.date] = {'protein': 0, 'calories': 0}
        meal_by_date[meal.date]['protein'] += meal.protein
        meal_by_date[meal.date]['calories'] += meal.calories
    
    for date, totals in meal_by_date.items():
        data['date'].append(date)
        data['protein'].append(totals['protein'])
        data['calories'].append(totals['calories'])
    
    df = pd.DataFrame(data)
    return df

def get_meal_type_data(user_id):
    user_meals = get_user_data(user_id)
    
    # Normalize meal types by converting to lowercase and stripping whitespace
    meal_types = [meal.meal_type.strip().lower() for meal in user_meals]
    meal_type_counts = pd.Series(meal_types).value_counts().reset_index()
    meal_type_counts.columns = ['meal_type', 'count']
    
    return meal_type_counts

def create_dash_app(flask_app):
    dash_app = dash.Dash(
        __name__,
        server=flask_app,
        url_base_pathname='/dash_app/',
        external_stylesheets=['https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/css/bootstrap.min.css']
    )
    
    dash_app.layout = html.Div([
        dcc.Dropdown(id='user-dropdown'),
        dcc.Graph(id='goal-achievement-bar-graph'),
        dcc.Graph(id='nutrition-dot-plot'),
        dcc.Graph(id='meal-type-pie-chart')
    ])
    
    @dash_app.callback(
        [Output('user-dropdown', 'options'),
         Output('user-dropdown', 'value')],
        Input('user-dropdown', 'id')
    )
    def update_user_dropdown(_):
        if current_user.is_authenticated:
            user_options = [{'label': current_user.first_name, 'value': current_user.id}]
            return user_options, current_user.id
        else:
            return [], None
    
    @dash_app.callback(
        [Output('goal-achievement-bar-graph', 'figure'),
         Output('nutrition-dot-plot', 'figure'),
         Output('meal-type-pie-chart', 'figure')],
        Input('user-dropdown', 'value')
    )
    def update_graphs(user_id):
        if not user_id:
            return {}, {}, {}
        
        goal_df = get_goal_achievement_data(user_id)
        nutrition_df = get_nutrition_data(user_id)
        meal_type_df = get_meal_type_data(user_id)
        
        # Goal Achievement Line Plot
        goal_fig = px.scatter(goal_df, x='date', y='goal', color='met', symbol='goal', 
                              title='Goal Achievement', labels={'met': 'Goal Met'}, 
                              category_orders={'goal': ['Protein', 'Calories']})
        goal_fig.update_traces(marker=dict(size=12, opacity=0.7), selector=dict(mode='markers+lines'))
        goal_fig.update_layout(yaxis=dict(tickmode='array', tickvals=['Protein', 'Calories']))
        
        # Nutrition Dot Plot
        nutrition_fig = px.scatter(nutrition_df, x='date', y=['protein', 'calories'], title='Protein and Calorie Intake', labels={'value': 'Intake'})
        
        # Meal Type Pie Chart
        meal_type_fig = px.pie(meal_type_df, names='meal_type', values='count', title='Most Eaten Meal Types')
        
        return goal_fig, nutrition_fig, meal_type_fig
    
    return dash_app
