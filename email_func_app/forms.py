from flask_wtf import FlaskForm
from wtforms import (
    StringField, PasswordField, SubmitField, SelectField, TextAreaField,
    IntegerField, FloatField, FileField
)
from wtforms.validators import DataRequired, Email, Length, EqualTo, Optional, NumberRange, URL
from wtforms.widgets import CheckboxInput
from wtforms import SelectMultipleField, widgets

class MultipleCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()

class LoginForm(FlaskForm):
    email = StringField('ایمیل', validators=[DataRequired(), Email()])
    password = PasswordField('رمز عبور', validators=[DataRequired()])
    submit = SubmitField('ورود')

class RegistrationForm(FlaskForm):
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

class CreatePlanForm(FlaskForm):
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

class OfferForm(FlaskForm):
    service_offered = StringField('خدمات پیشنهادی', validators=[DataRequired()])
    description = TextAreaField('توضیحات', validators=[Optional()])
    submit = SubmitField('ارسال پیشنهاد')

class SettingsForm(FlaskForm):
    # Common fields
    name = StringField('نام', validators=[DataRequired(), Length(min=2, max=100)])
    email = StringField('ایمیل', validators=[DataRequired(), Email()])
    location = StringField('موقعیت مکانی', validators=[Optional(), Length(max=100)])
    avatar = FileField('تصویر پروفایل', validators=[Optional()])
    
    # Password change fields
    current_password = PasswordField('رمز عبور فعلی')
    new_password = PasswordField('رمز عبور جدید', validators=[Optional(), Length(min=6)])
    confirm_password = PasswordField('تکرار رمز عبور جدید', 
                                   validators=[EqualTo('new_password', message='رمز عبور و تکرار آن باید یکسان باشند')])
    
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
