"""Plan forms."""
from wtforms import StringField, TextAreaField, FloatField, SelectMultipleField, DateTimeField
from wtforms.validators import DataRequired, Optional
from flask_wtf import FlaskForm

class PlanForm(FlaskForm):
    """Form for creating a new influencer plan."""
    title = StringField('عنوان', validators=[DataRequired()])
    description = TextAreaField('توضیحات', validators=[Optional()])
    location = StringField('موقعیت', validators=[DataRequired()])
    start_date = StringField('تاریخ شروع', validators=[DataRequired()])
    end_date = StringField('تاریخ پایان', validators=[DataRequired()])
    available_times = StringField('زمان‌های در دسترس', validators=[Optional()])
    content_suggestions = TextAreaField('پیشنهادات محتوا', validators=[Optional()])
    suggested_price = FloatField('قیمت پیشنهادی', validators=[Optional()])
    additional_notes = TextAreaField('یادداشت‌های اضافی', validators=[Optional()])
    custom_services = TextAreaField('خدمات سفارشی', validators=[Optional()])
    niches = SelectMultipleField('دسته‌بندی‌ها', coerce=int, validators=[Optional()])
    services = SelectMultipleField('خدمات', coerce=int, validators=[Optional()])
