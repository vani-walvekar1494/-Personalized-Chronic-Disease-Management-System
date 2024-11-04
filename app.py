from flask import Flask, render_template, redirect, url_for, flash, request
from flask_mysqldb import MySQL
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from forms import RegistrationForm, LoginForm, SymptomForm
from models import User, Symptom
from flask import jsonify
import bcrypt
import secrets
secrets.token_hex(16)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Legend@123'
app.config['MYSQL_DB'] = 'pcdms_db'

mysql = MySQL(app)
login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM users WHERE id = %s", (user_id,))
    user = cur.fetchone()
    return User(user[0], user[1], user[2]) if user else None

@app.route('/')
def home():
    return render_template('base.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.hashpw(form.password.data.encode('utf-8'), bcrypt.gensalt())
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (form.username.data, hashed_password))
        mysql.connection.commit()
        cur.close()
        flash('Account created successfully!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM users WHERE username = %s", (form.username.data,))
        user = cur.fetchone()
        if user and bcrypt.checkpw(form.password.data.encode('utf-8'), user[2].encode('utf-8')):
            user_obj = User(user[0], user[1], user[2])
            login_user(user_obj)
            return redirect(url_for('dashboard'))
        else:
            flash('Login unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', form=form)

@app.route('/dashboard')
@login_required
def dashboard():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM symptoms WHERE user_id = %s", (current_user.id,))
    symptoms = cur.fetchall()
    cur.close()
    return render_template('dashboard.html', symptoms=symptoms)

@app.route('/log_symptom', methods=['GET', 'POST'])
@login_required
def log_symptom():
    form = SymptomForm()
    if form.validate_on_submit():
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO symptoms (user_id, symptom) VALUES (%s, %s)", (current_user.id, form.symptom.data))
        mysql.connection.commit()
        cur.close()
        flash('Symptom logged successfully!', 'success')
        return redirect(url_for('dashboard'))
    return render_template('log_symptoms.html', form=form)

# Function to get recommendations based on symptoms
def get_recommendations(symptoms):
    recommendations = []
    if 'fatigue' in symptoms:
        recommendations.append("Consider taking short breaks and stay hydrated.")
    if 'high stress' in symptoms:
        recommendations.append("Practice relaxation techniques like deep breathing or meditation.")
    # Add more symptom-recommendation mappings here.
    return recommendations


@app.route('/get_symptom_data', methods=['GET'])
def get_symptom_data():
    cur = mysql.connection.cursor()
    cur.execute("SELECT date, severity FROM symptoms WHERE user_id = %s", (current_user.id,))
    data = cur.fetchall()
    cur.close()

    # Transform data into a format suitable for Chart.js
    dates = [str(row[0]) for row in data]  # Assuming the first column is the date
    severities = [row[1] for row in data]  # Assuming the second column is the severity

    return jsonify({"dates": dates, "severities": severities})


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/generate_plan', methods=['POST'])
def generate_plan():
    recommendations = get_recommendations(user_symptoms)
    plan_text = "\n".join(recommendations)
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO personalized_plans (user_id, plan_text) VALUES (%s, %s)", (session['user_id'], plan_text))
    mysql.connection.commit()
    return redirect(url_for('dashboard'))

@app.route('/get_recommendations', methods=['GET'])
def get_recommendations():
    # Here you would typically analyze the user's symptoms from the database
    # and generate personalized recommendations.

    # For example purposes, let's return a static list of recommendations.
    recommendations = [
        "Consider increasing your water intake.",
        "Try to exercise at least 30 minutes a day.",
        "Practice mindfulness or meditation to manage stress."
    ]
    
    return jsonify(recommendations)

if __name__ == '__main__':
    app.run(debug=True)
