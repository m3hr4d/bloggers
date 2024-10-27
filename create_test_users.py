from email_func_app import create_app, db
from email_func_app.models import User
from werkzeug.security import generate_password_hash

app = create_app()

def create_users():
    with app.app_context():
        # Check if users already exist
        if not User.query.filter_by(email='mehrad@gmail.com').first():
            # Create influencer user
            influencer = User(
                email='mehrad@gmail.com',
                password=generate_password_hash('mehrad@gmail.com'),
                user_type='influencer',
                name='Mehrad',
                instagram_profile='mehrad',
                location='Tehran',
                niche='Technology',
                followers=1000,
                engagement_rate=5.5
            )
            db.session.add(influencer)

        if not User.query.filter_by(email='brand@gmail.com').first():
            # Create business user
            business = User(
                email='brand@gmail.com',
                password=generate_password_hash('brand@gmail.com'),
                user_type='business',
                business_name='Brand Company',
                business_website='https://brand.com',
                location='Tehran'
            )
            db.session.add(business)

        try:
            db.session.commit()
            print("Test users created successfully!")
        except Exception as e:
            db.session.rollback()
            print(f"Error creating users: {e}")

if __name__ == '__main__':
    create_users()
