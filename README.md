# Fitness progressive web app
This project is very personal to me, I am a weightlifter and gym enthusiast. I go to the gym at least 4 times a week, and anyone who knows anything about weightlifting, body building, or resistance training knows that the hardest part about making progress is not putting in the work at the gym but rather keeping consistent and maintaining a healthy and suitable diet to help you reach your goals.

A full-stack web application built with Python, Flask, and SQLite, designed to help fitness enthusiasts and health-conscious individuals track their daily protein and calorie intake, set personalized goals, and monitor dietary progress.

Features
User Authentication: Secure sign-up and login with password hashing.
Meal Logging: Add and manage meals with custom protein and calorie values.
Goal Setting: Set daily protein and calorie targets with real-time progress tracking.
Progress Visualization: Interactive dashboards using Dash and Plotly to display intake trends and goal completion.
Responsive UI: Clean, mobile-friendly interface built with Bootstrap.
Data Export: Automatically generates downloadable Word (.docx) reports of user and meal data for backup and sharing (powered by python-docx).
Admin Tools: Structured data export and database backup capabilities for administrators.

Tech Stack
Backend: Python, Flask, SQLAlchemy (ORM)
Frontend: HTML, CSS, Bootstrap, Chart.js (via Dash)
Database: SQLite
Tools & Libraries: Flask-Login, Flask-WTF, python-docx, Dash, Plotly, WTForms

Project Structure
├── main.py               # App entry point

├── __init__.py           # Flask app initialization & DB setup

├── models.py             # Database models (User, Meal)

├── views.py              # Main routes (dashboard, logging)

├── auth.py               # Authentication routes (login, signup)

├── forms.py              # WTForms for meal and goal input

├── dash_app.py           # Interactive data visualization dashboard

├── docx_handling.py      # Generates Word reports from user data

└── templates/            # HTML templates (Jinja2)
