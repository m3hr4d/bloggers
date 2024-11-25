from email_func_app import create_app, db
from email_func_app.models import User
from werkzeug.security import generate_password_hash, check_password_hash

def verify_user():
    app = create_app()
    with app.app_context():
        email = 'mehrad@gmail.com'
        password = 'mehrad@gmail.com'
        
        # Find the user
        user = User.query.filter_by(email=email).first()
        if user:
            print(f"User found: {user.email}")
            print(f"User type: {user.user_type}")
            
            # Test current password
            is_valid = check_password_hash(user.password, password)
            print(f"Current password valid: {is_valid}")
            
            if not is_valid:
                # Update password if invalid
                print("Updating password...")
                user.password = generate_password_hash(password, method='pbkdf2:sha256')
                db.session.commit()
                
                # Verify new password
                user = User.query.filter_by(email=email).first()
                is_valid = check_password_hash(user.password, password)
                print(f"New password valid: {is_valid}")
        else:
            print("User not found!")

if __name__ == '__main__':
    verify_user()
