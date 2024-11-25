from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import (StringField, TextAreaField, SelectField, FloatField, 
                    BooleanField, IntegerField, FieldList, FormField,
                    DateTimeField, SelectMultipleField)
from wtforms.validators import DataRequired, Email, Length, Optional, URL, NumberRange

class SocialMediaAccountForm(FlaskForm):
    """Form for social media account details."""
    platform = SelectField('Platform', choices=[
        ('instagram', 'Instagram'),
        ('tiktok', 'TikTok'),
        ('youtube', 'YouTube'),
        ('twitter', 'Twitter'),
        ('facebook', 'Facebook'),
        ('linkedin', 'LinkedIn')
    ])
    username = StringField('Username', validators=[DataRequired()])
    profile_url = StringField('Profile URL', validators=[Optional(), URL()])

class PortfolioItemForm(FlaskForm):
    """Form for portfolio items."""
    title = StringField('Title', validators=[DataRequired(), Length(max=200)])
    description = TextAreaField('Description')
    media_type = SelectField('Media Type', choices=[
        ('image', 'Image'),
        ('video', 'Video'),
        ('link', 'Link')
    ])
    media_url = StringField('Media URL', validators=[Optional(), URL()])

class BasicProfileForm(FlaskForm):
    """Form for basic profile information."""
    name = StringField('Name', validators=[DataRequired(), Length(max=100)])
    profile_image = FileField('Profile Image', validators=[
        Optional(),
        FileAllowed(['jpg', 'png', 'jpeg'], 'Images only!')
    ])
    bio = TextAreaField('Bio')
    location = StringField('Location', validators=[DataRequired()])
    phone = StringField('Phone Number', validators=[Optional(), Length(max=20)])
    website = StringField('Website', validators=[Optional(), URL()])
    language = SelectField('Language', choices=[
        ('en', 'English'),
        ('es', 'Spanish'),
        ('fr', 'French')
    ])
    timezone = StringField('Timezone')

class InfluencerProfileForm(FlaskForm):
    """Form for influencer-specific details."""
    niche = StringField('Niche', validators=[DataRequired()])
    interests = TextAreaField('Interests')
    collaboration_types = SelectMultipleField('Collaboration Types', choices=[
        ('hotels', 'Hotels'),
        ('flights', 'Flights'),
        ('restaurants', 'Restaurants'),
        ('events', 'Events'),
        ('products', 'Products')
    ])
    preferred_categories = SelectMultipleField('Preferred Categories', choices=[
        ('travel', 'Travel'),
        ('food', 'Food & Dining'),
        ('lifestyle', 'Lifestyle'),
        ('fashion', 'Fashion'),
        ('tech', 'Technology')
    ])
    min_budget = FloatField('Minimum Budget', validators=[Optional(), NumberRange(min=0)])
    social_accounts = FieldList(FormField(SocialMediaAccountForm), min_entries=1)
    portfolio_items = FieldList(FormField(PortfolioItemForm), min_entries=0)

class BusinessProfileForm(FlaskForm):
    """Form for business-specific details."""
    business_name = StringField('Business Name', validators=[DataRequired()])
    business_registration = StringField('Business Registration Number')
    business_type = SelectField('Business Type', choices=[
        ('hotel', 'Hotel'),
        ('airline', 'Airline'),
        ('restaurant', 'Restaurant'),
        ('travel_agency', 'Travel Agency'),
        ('event_venue', 'Event Venue')
    ])
    industry = SelectField('Industry', choices=[
        ('hospitality', 'Hospitality'),
        ('travel', 'Travel'),
        ('food', 'Food & Beverage'),
        ('entertainment', 'Entertainment'),
        ('retail', 'Retail')
    ])
    company_size = SelectField('Company Size', choices=[
        ('1-10', '1-10 employees'),
        ('11-50', '11-50 employees'),
        ('51-200', '51-200 employees'),
        ('201-1000', '201-1000 employees'),
        ('1000+', '1000+ employees')
    ])
    founded_year = IntegerField('Founded Year', validators=[Optional()])
    business_description = TextAreaField('Business Description')
    services_offered = TextAreaField('Services Offered')
    service_locations = StringField('Service Locations')
    content_needs = SelectMultipleField('Content Needs', choices=[
        ('photos', 'Photography'),
        ('videos', 'Videos'),
        ('reviews', 'Reviews'),
        ('stories', 'Stories'),
        ('blogs', 'Blog Posts')
    ])
    annual_budget = SelectField('Annual Marketing Budget', choices=[
        ('0-10k', '$0 - $10,000'),
        ('10k-50k', '$10,000 - $50,000'),
        ('50k-100k', '$50,000 - $100,000'),
        ('100k-500k', '$100,000 - $500,000'),
        ('500k+', '$500,000+')
    ])

class NotificationPreferencesForm(FlaskForm):
    """Form for notification preferences."""
    email_notifications = BooleanField('Email Notifications', default=True)
    sms_notifications = BooleanField('SMS Notifications')
    new_offers = BooleanField('New Offers', default=True)
    messages = BooleanField('Messages', default=True)
    campaign_updates = BooleanField('Campaign Updates', default=True)
    marketing_emails = BooleanField('Marketing Emails')

class PrivacySettingsForm(FlaskForm):
    """Form for privacy settings."""
    profile_visibility = SelectField('Profile Visibility', choices=[
        ('public', 'Public'),
        ('registered', 'Registered Users Only'),
        ('private', 'Private')
    ])
    show_contact_info = BooleanField('Show Contact Information')
    show_analytics = BooleanField('Show Analytics')
    allow_messages = BooleanField('Allow Messages', default=True)
