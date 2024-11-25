from threading import Thread
from flask import current_app, render_template, url_for
from flask_mail import Message
from email_func_app import mail

def send_async_email(app, msg):
    """Send email asynchronously.
    
    Args:
        app: Flask application context
        msg: Email message to send
    """
    with app.app_context():
        mail.send(msg)

def send_email(subject, sender, recipients, text_body, html_body=None, attachments=None):
    """Send an email.
    
    Args:
        subject (str): Email subject
        sender (str): Email sender
        recipients (list): List of recipients
        text_body (str): Plain text email body
        html_body (str, optional): HTML email body
        attachments (list, optional): List of attachments
    """
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    if html_body:
        msg.html = html_body
        
    if attachments:
        for attachment in attachments:
            msg.attach(*attachment)
    
    Thread(
        target=send_async_email,
        args=(current_app._get_current_object(), msg)
    ).start()

def send_password_reset_email(user):
    """Send password reset email to user.
    
    Args:
        user: User object
    """
    token = user.get_reset_password_token()
    send_email(
        'بازنشانی رمز عبور',
        sender=current_app.config['MAIL_DEFAULT_SENDER'],
        recipients=[user.email],
        text_body=f'''برای بازنشانی رمز عبور خود روی لینک زیر کلیک کنید:

{url_for('auth.reset_password', token=token, _external=True)}

اگر شما درخواست بازنشانی رمز عبور نداده‌اید، لطفاً این ایمیل را نادیده بگیرید.
''',
        html_body=render_template('email/reset_password.html',
                                user=user, token=token)
    )
