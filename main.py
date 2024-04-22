
# Import necessary modules
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

# Create a Flask application
app = Flask(__name__)

# Configure the database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

# Define the User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    preferences = db.Column(db.String(255))

# Define the Match model
class Match(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    match_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    compatibility_score = db.Column(db.Float)

# Create the database tables
db.create_all()

# Landing page route
@app.route('/')
def index():
    return render_template('index.html')

# User registration route
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Get form data
        username = request.form['username']
        password = request.form['password']
        preferences = request.form['preferences']

        # Create a new user
        user = User(username=username, password=password, preferences=preferences)

        # Add the user to the database
        db.session.add(user)
        db.session.commit()

        # Redirect to the login page
        return redirect(url_for('login'))

    return render_template('register.html')

# User login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Get form data
        username = request.form['username']
        password = request.form['password']

        # Query the database for the user
        user = User.query.filter_by(username=username, password=password).first()

        # If the user exists, redirect to the profile page
        if user:
            return redirect(url_for('profile'))

        # Otherwise, display an error message
        else:
            return render_template('login.html', error="Invalid credentials.")

    return render_template('login.html')

# User profile route
@app.route('/profile')
def profile():
    # Get the current user
    user = current_user

    # Get the user's matches
    matches = Match.query.filter_by(user_id=user.id).all()

    # Render the profile page
    return render_template('profile.html', user=user, matches=matches)

# Matches route
@app.route('/matches')
def matches():
    # Get the current user
    user = current_user

    # Get all the users in the database
    users = User.query.all()

    # Calculate the compatibility score for each user
    for user in users:
        compatibility_score = calculate_compatibility_score(user.preferences, user.preferences)

        # Create a new match if the compatibility score is high enough
        if compatibility_score > 0.5:
            match = Match(user_id=user.id, match_id=user.id, compatibility_score=compatibility_score)
            db.session.add(match)

    # Commit the changes to the database
    db.session.commit()

    # Get the user's matches
    matches = Match.query.filter_by(user_id=user.id).all()

    # Render the matches page
    return render_template('matches.html', user=user, matches=matches)

# Chat route
@app.route('/chat/<match_id>', methods=['GET', 'POST'])
def chat(match_id):
    # Get the current user
    user = current_user

    # Get the match
    match = Match.query.filter_by(user_id=user.id, match_id=match_id).first()

    # If the match does not exist, redirect to the matches page
    if not match:
        return redirect(url_for('matches'))

    # Get the messages for the chat
    messages = Message.query.filter_by(match_id=match.id).all()

    # Render the chat page
    return render_template('chat.html', user=user, match=match, messages=messages)

# Run the application
if __name__ == '__main__':
    app.run(debug=True)
