from flask import Flask, render_template, redirect, url_for, request
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length
import random
import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'

# Define quote categories
quote_categories = {
    "Inspirational": [
        "The only way to do great work is to love what you do. - Steve Jobs",
        "Believe you can and you're halfway there. - Theodore Roosevelt",
        "It does not matter how slowly you go as long as you do not stop. - Confucius"
    ],
    "Motivational": [
        "The future belongs to those who believe in the beauty of their dreams. - Eleanor Roosevelt",
        "The only limit to our realization of tomorrow will be our doubts of today. - Franklin D. Roosevelt"
    ],
    "Love": [
        "The best thing to hold onto in life is each other. - Audrey Hepburn",
        "Love is composed of a single soul inhabiting two bodies. - Aristotle"
    ],
    "Funny": [
        "I'm not lazy, I'm on energy-saving mode.",
        "I'm not arguing, I'm just explaining why I'm right."
    ]
}

# Define get_quote_of_the_day function
def get_quote_of_the_day():
    # Get today's date
    today = datetime.date.today()
    
    # Use today's date as a seed to ensure the same quote is shown for the entire day
    seed = today.toordinal()
    
    # Select a random category from the quote_categories dictionary
    random_category = random.choice(list(quote_categories.keys()))
    
    # Get quotes for the selected category
    quotes = quote_categories[random_category]
    
    # Use the seed to select a random quote
    random.seed(seed)
    quote_of_the_day = random.choice(quotes)
    
    return quote_of_the_day

# Define forms
class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

# Define routes
@app.route('/')
def home():
    # Fetch the quote of the day
    quote_of_the_day = get_quote_of_the_day()
    
    # Render the homepage template and pass the quote of the day to it
    return render_template('index.html', quote_of_the_day=quote_of_the_day)

@app.route('/<category>')
def get_quote_by_category(category):
    # Check if the category exists
    if category in quote_categories:
        # Generate a random quote from the selected category
        random_quote = random.choice(quote_categories[category])
        # Render the homepage template and pass the random quote and categories to it
        return render_template('index.html', quote=random_quote, categories=list(quote_categories.keys()))
    else:
        # If the category does not exist, redirect to the homepage
        return redirect('/')

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        # Process form data (e.g., create new user)
        # Redirect to login page after successful registration
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        # Process form data (e.g., authenticate user)
        # Redirect to homepage after successful login
        return redirect(url_for('home'))
    return render_template('login.html', form=form)

if __name__ == '__main__':
    app.run(debug=True)
