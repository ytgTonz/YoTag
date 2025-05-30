from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms import TextAreaField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from wtforms.validators import Length
from pymongo import MongoClient
import os
import requests
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

@app.route('/')
@app.route('/index')
def index():
    return render_template('landing-freelancer.html', title='YoTag')

class MessageForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    message = TextAreaField('Message', validators=[Length(min=0, max=140)])
    submit = SubmitField('Submit')



def edit_profile():
    form = MessageForm()
    if form.validate_on_submit():
        form.username.data =  requests.form['name']  # Retrieve 'name' input
        form.email.data =  requests.form['email']  # Retrieve 'email' input
        form.message.data  = requests.form['message'] # Retrieve 'message' input
        
        message_data = {
            "username": form.username.data,
            "email": form.email.data,
            "message": form.message.data
        }
        collection.insert_one(message_data)
        print("Report saved to MongoDB Atlas")
    return render_template('landing-freelancer.html', title='YoTag', form=form)
    


# MongoDB Atlas connection
MONGO_URI = os.getenv("MONGO_URI")
client = MongoClient(MONGO_URI)
db = client["clientlist"]
collection = db["contacts"]

    
if __name__ == "__main__":
    app.run(debug=True, port=5000)

