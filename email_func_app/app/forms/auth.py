"""Authentication forms."""
from wtforms import (
    StringField, PasswordField, SubmitField, SelectField,
    IntegerField, FloatField
)
from wtforms.validators import (
    DataRequired, Email, Length, EqualTo, Optional,
    NumberRange
)
from flask_wtf import FlaskForm

class LoginForm(FlaskForm):
    """Form for user login."""
    email = StringField('ایمیل', validators=[DataRequired(), Email()])
    password = PasswordField('رمز عبور', validators=[DataRequired()])
    submit = SubmitField('ورود')

class RegistrationForm(FlaskForm):
    """Form for user registration."""
    email = StringField('ایمیل', validators=[DataRequired(), Email()])
    password = PasswordField('رمز عبور', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField(
        'تکرار رمز عبور',
        validators=[DataRequired(), EqualTo('password', message='رمز عبور و تکرار آن باید یکسان باشند')]
    )
    user_type = SelectField(
        'نوع کاربر',
        choices=[('influencer', 'اینفلوئنسر'), ('business', 'کسب و کار')],
        validators=[DataRequired()]
    )
    name = StringField('نام و نام خانوادگی', validators=[DataRequired()])
    instagram_profile = StringField('پروفایل اینستاگرام', validators=[Optional()])
    location = StringField('موقعیت', validators=[Optional()])
    
    # Influencer-specific fields
    niche = StringField('حوزه فعالیت', validators=[Optional()])
    followers = IntegerField('تعداد دنبال‌کنندگان', validators=[Optional()])
    engagement_rate = FloatField(
        'نرخ تعامل',
        validators=[Optional(), NumberRange(min=0, max=100)]
    )
    
    # Business-specific fields
    business_name = StringField('نام کسب و کار', validators=[Optional()])
    business_website = StringField('وب‌سایت', validators=[Optional()])
    
    submit = SubmitField('ثبت نام')
