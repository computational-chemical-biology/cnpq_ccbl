from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import Length, Email, InputRequired

# Form ORM
class JournalForm(FlaskForm):
    journal_name = StringField('Journal Name')
    twitter = StringField('Twitter handle')
    submit = SubmitField('Submit')
