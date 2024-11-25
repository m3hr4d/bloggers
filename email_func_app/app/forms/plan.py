"""Plan forms."""
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Optional
from flask_wtf import FlaskForm
from .fields import MultipleCheckboxField

class CreatePlanForm(FlaskForm):
    """Form for creating a new travel plan."""
    destination = StringField('مقصد', validators=[DataRequired()])
    location = StringField('موقعیت', validators=[DataRequired()])
    start_date = StringField('تاریخ شروع')  # No validators to allow client-side validation
    end_date = StringField('تاریخ پایان')    # No validators to allow client-side validation
    time = StringField('زمان', validators=[Optional()])
    services_requested = MultipleCheckboxField('خدمات مورد نیاز', choices=[
        ('hotel', 'هتل'),
        ('restaurant', 'رستوران'),
        ('shopping', 'خرید'),
        ('beauty', 'خدمات زیبایی'),
        ('tourism', 'گردشگری'),
        ('entertainment', 'سرگرمی')
    ], validators=[Optional()])
    topics_of_interest = TextAreaField('موضوعات مورد علاقه', validators=[Optional()])
    submit = SubmitField('ایجاد برنامه')
