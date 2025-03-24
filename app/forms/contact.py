from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, TextAreaField
from wtforms.validators import DataRequired, Email, Length, ValidationError
import re

class ContactForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=2, max=100)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    subject = StringField('Subject', validators=[DataRequired(), Length(min=2, max=200)])
    message = TextAreaField('Message', validators=[DataRequired(), Length(min=10, max=2000)])
    recaptcha = RecaptchaField()
    
    def validate_email(self, field):
        # Check for disposable email providers
        disposable_domains = ['tempmail.com', 'throwawaymail.com', 'registry.godaddy']
  # Add more as needed
        domain = field.data.split('@')[1]
        if domain in disposable_domains:
            raise ValidationError('Disposable email addresses are not allowed')

