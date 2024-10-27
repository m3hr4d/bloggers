from email_func_app import create_app, db
from email_func_app.models import User, Plan, Offer
import sqlite3
from flask_migrate import Migrate
from sqlalchemy import text
import sys

def migrate_data():
    app = create_app()
    migrate = Migrate(app, db)
    sqlite_conn = None
    
    with app.app_context():
        try:
            # Clear existing data in MariaDB
            print("Clearing existing data...")
            db.session.execute(text('SET FOREIGN_KEY_CHECKS=0;'))
            db.session.execute(text('TRUNCATE TABLE user;'))
            db.session.execute(text('TRUNCATE TABLE plan;'))
            db.session.execute(text('TRUNCATE TABLE offer;'))
            db.session.execute(text('SET FOREIGN_KEY_CHECKS=1;'))
            db.session.commit()
            
            # Connect to SQLite database
            sqlite_conn = sqlite3.connect('instance/main_app.db')
            sqlite_conn.text_factory = str  # Handle non-ASCII characters
            sqlite_cursor = sqlite_conn.cursor()
            
            # Migrate Users
            print("Migrating users...")
            sqlite_cursor.execute('SELECT * FROM user')
            users = sqlite_cursor.fetchall()
            for user in users:
                try:
                    new_user = User(
                        id=user[0],
                        email=user[1],
                        password=user[2],
                        user_type=user[3],
                        name=user[4],
                        instagram_profile=user[5],
                        location=user[6],
                        niche=user[7],
                        followers=user[8],
                        engagement_rate=user[9],
                        business_name=user[10],
                        business_website=user[11]
                    )
                    db.session.add(new_user)
                    db.session.flush()
                    print(f"Migrated user: {user[1]}")
                except Exception as e:
                    print(f"Error migrating user {user[1]}: {str(e)}")
                    continue
            
            # Migrate Plans
            print("Migrating plans...")
            sqlite_cursor.execute('SELECT * FROM plan')
            plans = sqlite_cursor.fetchall()
            for plan in plans:
                try:
                    new_plan = Plan(
                        id=plan[0],
                        influencer_id=plan[1],
                        destination=plan[2],
                        location=plan[3],
                        start_date=plan[4],
                        end_date=plan[5],
                        time=plan[6],
                        services_requested=plan[7],
                        topics_of_interest=plan[8],
                        status=plan[9],
                        edit_count=plan[10]
                    )
                    db.session.add(new_plan)
                    db.session.flush()
                    print(f"Migrated plan: {plan[0]}")
                except Exception as e:
                    print(f"Error migrating plan {plan[0]}: {str(e)}")
                    continue
            
            # Migrate Offers
            print("Migrating offers...")
            sqlite_cursor.execute('SELECT * FROM offer')
            offers = sqlite_cursor.fetchall()
            for offer in offers:
                try:
                    new_offer = Offer(
                        id=offer[0],
                        plan_id=offer[1],
                        business_id=offer[2],
                        service_offered=offer[3],
                        description=offer[4],
                        status=offer[5]
                    )
                    db.session.add(new_offer)
                    db.session.flush()
                    print(f"Migrated offer: {offer[0]}")
                except Exception as e:
                    print(f"Error migrating offer {offer[0]}: {str(e)}")
                    continue
            
            # Commit all changes
            db.session.commit()
            print("Migration completed successfully!")
            
        except Exception as e:
            print(f"Error during migration: {str(e)}")
            db.session.rollback()
            sys.exit(1)
            
        finally:
            if sqlite_conn:
                sqlite_conn.close()

if __name__ == '__main__':
    migrate_data()
