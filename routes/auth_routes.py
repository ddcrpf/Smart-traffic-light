from flask import Blueprint, render_template, redirect, url_for, request, session
from werkzeug.security import check_password_hash

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # Validate user (implement user validation here)
        if valid_user(username, password):
            session['user'] = username
            return redirect(url_for('dashboard.dashboard'))
    return render_template('login.html')

@auth_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))

users = {
    "admin": "admin123",
    "policeman": "policeman123"
}

def valid_user(username, password):
    # Check if the username exists and the password matches
    return username in users and users[username] == password
