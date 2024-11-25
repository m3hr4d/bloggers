from flask_wtf import FlaskForm
from wtforms import BooleanField, SelectField, SubmitField, StringField, TextAreaField, PasswordField
from wtforms.validators import DataRequired, Email, Length, EqualTo, URL, Optional

class ProfileSettingsForm(FlaskForm):
    location = StringField('موقعیت مکانی', validators=[Optional()])
    phone_number = StringField('شماره تماس', validators=[Optional(), Length(min=10, max=15)])
    bio = TextAreaField('درباره من', validators=[Optional(), Length(max=500)])
    services_interested_in = TextAreaField('خدمات مورد علاقه', validators=[Optional(), Length(max=500)])
    business_website = StringField('وب‌سایت', validators=[Optional(), URL()])
    instagram_profile = StringField('پروفایل اینستاگرام', validators=[Optional()], description='آدرس پروفایل یا نام کاربری اینستاگرام خود را وارد کنید')

class SecuritySettingsForm(FlaskForm):
    current_password = PasswordField('رمز عبور فعلی', validators=[DataRequired()])
    new_password = PasswordField('رمز عبور جدید', validators=[
        DataRequired(),
        Length(min=8, message='رمز عبور باید حداقل ۸ کاراکتر باشد')
    ])
    confirm_password = PasswordField('تکرار رمز عبور جدید', validators=[
        DataRequired(),
        EqualTo('new_password', message='رمز عبور و تکرار آن باید یکسان باشند')
    ])

class NotificationPreferencesForm(FlaskForm):
    # Communication Channels
    email_notifications = BooleanField('Email Notifications')
    sms_notifications = BooleanField('SMS Notifications')
    
    # Notification Types
    new_offers = BooleanField('Collaboration Offers')
    messages = BooleanField('Messages')
    campaign_updates = BooleanField('Campaign Updates')
    marketing_emails = BooleanField('Marketing Communications')
    
    submit = SubmitField('Save Preferences')

class PrivacySettingsForm(FlaskForm):
    # Profile Visibility
    profile_visibility = SelectField(
        'Profile Visibility',
        choices=[
            ('public', 'Public'),
            ('registered', 'Registered Users Only'),
            ('private', 'Private')
        ],
        validators=[DataRequired()]
    )
    
    # Information Display
    show_contact_info = BooleanField('Show Contact Information')
    show_analytics = BooleanField('Show Analytics')
    
    # Communication Settings
    allow_messages = BooleanField('Allow Messages')
    
    submit = SubmitField('Save Settings')
