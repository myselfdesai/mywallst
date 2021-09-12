from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
# from flask_wtf import FlaskForm
# from wtforms import StringField, PasswordField, BooleanField
# from wtforms.validators import InputRequired, Email, Length

app = Flask(__name__)
app.config.from_object("config.Config")

Bootstrap(app)
db = SQLAlchemy(app)

from stripeapp import routes