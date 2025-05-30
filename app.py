from flask import Flask, render_template, request, flash, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms import TextAreaField
from wtforms.validators import DataRequired, Length
from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'

class MessageForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired() ])
    message = TextAreaField('Message', validators=[Length(min=0, max=140)])
    submit = SubmitField('Submit')

@app.route('/index', methods=['GET', 'POST'])
def index():
    form = MessageForm()  
    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        message = form.message.data

        contact_data = {
            "username": username,
            "email": email,
            "message": message
        }
        collection.insert_one(contact_data)
        print("DATA IS CAPUTRED AND SAVED TO MONGODB")
    else:
        flash("Your message has not been sent!")
    
    return render_template('landing-freelancer.html', title='YoTag', form=form)

# MongoDB Atlas connection
MONGO_URI = os.getenv("MONGO_URI")
if not MONGO_URI:
    raise ValueError("No MONGO_URI environment variable found")

try:
    client = MongoClient(MONGO_URI)
    # Verify connection
    client.server_info()
    db = client["clientlist"]
    collection = db["contacts"]
    print("Successfully connected to MongoDB")
except Exception as e:
    print(f"Error connecting to MongoDB: {e}")

if __name__ == "__main__":
    app.run(debug=True, port=5000)

