"""Offer forms."""
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Optional
from flask_wtf import FlaskForm

class OfferForm(FlaskForm):
    """Form for creating a business offer."""
    service_offered = StringField('خدمات پیشنهادی', validators=[DataRequired()])
    description = TextAreaField('توضیحات', validators=[Optional()])
    submit = SubmitField('ارسال پیشنهاد')
