"""Settings forms."""
from wtforms import (
    StringField, PasswordField, SubmitField, TextAreaField,
    IntegerField, FloatField, FileField
)
from wtforms.validators import (
    DataRequired, Email, Length, EqualTo, Optional,
    NumberRange, URL
)
from flask_wtf import FlaskForm

class SettingsForm(FlaskForm):
    """Form for user settings."""
    # Common fields
    name = StringField('نام', validators=[DataRequired(), Length(min=2, max=100)])
    email = StringField('ایمیل', validators=[DataRequired(), Email()])
    location = StringField('موقعیت مکانی', validators=[Optional(), Length(max=100)])
    avatar = FileField('تصویر پروفایل', validators=[Optional()])
    
    # Password change fields
    current_password = PasswordField('رمز عبور فعلی')
    new_password = PasswordField('رمز عبور جدید', validators=[Optional(), Length(min=6)])
    confirm_password = PasswordField(
        'تکرار رمز عبور جدید',
        validators=[EqualTo('new_password', message='رمز عبور و تکرار آن باید یکسان باشند')]
    )
    
    # Influencer-specific fields
    instagram_profile = StringField('پروفایل اینستاگرام', validators=[Optional(), Length(max=100)])
    niche = StringField('زمینه تخصصی', validators=[Optional(), Length(max=100)])
    followers = IntegerField('تعداد دنبال‌کنندگان', validators=[Optional(), NumberRange(min=0)])
    engagement_rate = FloatField('نرخ تعامل (درصد)', validators=[Optional(), NumberRange(min=0, max=100)])
    phone_number = StringField('شماره تماس', validators=[Optional(), Length(max=20)])
    social_links = TextAreaField('لینک‌های شبکه‌های اجتماعی', validators=[Optional()])
    bio = TextAreaField('بیوگرافی', validators=[Optional()])
    services_interested_in = TextAreaField('خدمات مورد علاقه', validators=[Optional()])
    
    # Business-specific fields
    business_name = StringField('نام کسب‌وکار', validators=[Optional(), Length(max=100)])
    business_website = StringField('وبسایت', validators=[Optional(), URL()])
    
    submit = SubmitField('ذخیره تغییرات')
