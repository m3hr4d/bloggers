from email_func_app import create_app, db
from email_func_app.models import User
from werkzeug.security import generate_password_hash

def update_user_password():
    app = create_app()
    with app.app_context():
        # Find the user
        user = User.query.filter_by(email='mehrad@gmail.com').first()
        if user:
            # Update the password hash with the correct method
            new_password = 'mehrad@gmail.com'  # Using email as password
            user.password = generate_password_hash(new_password, method='pbkdf2:sha256')
            db.session.commit()
            print("Password updated successfully!")
        else:
            print("User not found!")

if __name__ == '__main__':
    update_user_password()
