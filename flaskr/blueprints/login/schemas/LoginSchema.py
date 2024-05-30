from flask_wtf import FlaskForm
from wtforms import validators, EmailField, PasswordField, SubmitField


class LoginSchema(FlaskForm):
    email = EmailField('Email', [validators.length(min=8, max=80)])
    password = PasswordField('Password', [validators.length(min=8)])