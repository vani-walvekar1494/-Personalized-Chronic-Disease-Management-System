# Personalized-Chronic-Disease-Management-System

## Overview
The Personalized Chronic Disease Management System (PCDMS) is a web application that allows users to register, log symptoms, and manage chronic diseases effectively. 

It provides a user-friendly interface for monitoring symptoms and helps in managing health better.

# Project Structure

- **pcdms/**
  - `app.py`                  # Main application file
  - `config.py`               # Configuration settings
  - `requirements.txt`        # Required packages
  - **templates/**            # HTML templates
    - `base.html`             # Base HTML template
    - `login.html`            # Login page
    - `register.html`         # Registration page
    - `dashboard.html`        # User dashboard
    - `log_symptoms.html`     # Symptom logging page
  - **static/**               # Static files (CSS, JS)
    - `styles.css`            # Stylesheet
    - `models.py`             # Database models
    - `forms.py`              # Forms for user input
    - `chatbot.py`            # AI chatbot logic (placeholder)




## Requirements
- Python 3.x
- Flask
- MySQL
- Flask-MySQLdb
- Flask-WTF
- Flask-Login
- bcrypt
- pandas
- numpy

## Getting Started

1. Clone this repository:
   git clone <repository-url>


2. Navigate to the project directory:
   cd pcdms

3. Create a virtual environment:
  python -m venv venv
  source venv/bin/activate  # On Windows use `venv\Scripts\activate`
  
4.Install the required packages:
  pip install -r requirements.txt

5. Set up the MySQL database using the provided SQL commands.

6. Run the application:
   python app.py

7. Open your web browser and visit http://127.0.0.1:5000/.

**Usage**
Register a new account.
Log in with your credentials.
Log symptoms as they occur.
View logged symptoms in the dashboard.

**Future Enhancements**
Integrate an AI chatbot for personalized health tips.
Expand symptom analysis features.
Implement data visualization for symptom trends.



### Final Note
Feel free to customize the code and README file as per your requirements. This guide provides a solid foundation for your PCDMS project using Flask and MySQL. Good luck with your development, and if you have any questions, don’t hesitate to ask!
