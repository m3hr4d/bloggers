from email_func_app import create_app, db
from email_func_app.models import User
from werkzeug.security import generate_password_hash, check_password_hash

def test_auth():
    app = create_app()
    with app.app_context():
        # First, let's check if the user exists
        user = User.query.filter_by(email='mehrad@gmail.com').first()
        
        if user:
            print("User exists, updating password...")
            # Update password
            user.password = generate_password_hash('mehrad@gmail.com', method='pbkdf2:sha256')
        else:
            print("User doesn't exist, creating new user...")
            # Create new user
            user = User(
                email='mehrad@gmail.com',
                password=generate_password_hash('mehrad@gmail.com', method='pbkdf2:sha256'),
                user_type='business',  # Default type
                onboarding_completed=True  # Set to True to avoid redirection
            )
            db.session.add(user)
        
        try:
            db.session.commit()
            print("User updated successfully!")
            
            # Verify the password works
            test_user = User.query.filter_by(email='mehrad@gmail.com').first()
            if check_password_hash(test_user.password, 'mehrad@gmail.com'):
                print("Password verification successful!")
            else:
                print("Password verification failed!")
                
        except Exception as e:
            print(f"Error: {e}")
            db.session.rollback()

if __name__ == '__main__':
    test_auth()
