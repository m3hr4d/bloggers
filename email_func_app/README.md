# Bloggers Platform

A Flask-based platform connecting influencers with businesses for collaboration opportunities.

## Project Structure

```
email_func_app/
├── app/
│   ├── __init__.py              # Application factory
│   ├── blueprints/              # Route blueprints
│   │   ├── admin/              # Admin functionality
│   │   ├── auth/               # Authentication
│   │   ├── main/               # Main routes
│   │   └── offers/             # Offers functionality
│   ├── forms/                   # Form definitions
│   ├── models/                  # Database models
│   ├── static/                  # Static assets
│   ├── templates/               # HTML templates
│   └── utils/                   # Utility functions
├── config.py                    # Configuration
├── requirements.txt             # Project dependencies
└── README.md                    # This file
```

## Setup

1. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Create a `.env` file with the following variables:
   ```
   FLASK_APP=email_func_app
   FLASK_ENV=development
   SECRET_KEY=your-secret-key
   DATABASE_URL=sqlite:///your-database.db
   ```

4. Initialize the database:
   ```bash
   flask db upgrade
   ```

5. Run the application:
   ```bash
   flask run
   ```

## Features

- User authentication (login/register)
- Influencer profiles and travel plans
- Business profiles and collaboration offers
- Admin dashboard
- Image upload and management
- Responsive design

## Development

- Use `flask db migrate` to generate migrations after model changes
- Use `flask db upgrade` to apply migrations
- Run tests with `python -m pytest`

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request
