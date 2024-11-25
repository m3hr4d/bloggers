# Bloggers Application

A Flask-based web application for managing blogs and email functionality.

## Project Structure

```
bloggers/
├── email_func_app/           # Main application package
│   ├── admin/               # Admin module
│   ├── auth/                # Authentication module
│   ├── main/                # Main routes and views
│   ├── offers/              # Offers module
│   ├── static/              # Static files (CSS, JS, images)
│   ├── templates/           # Jinja2 templates
│   ├── models.py            # Database models
│   └── forms.py             # WTForms definitions
├── migrations/              # Database migrations
├── tests/                   # Test suite
├── config.py               # Configuration settings
├── requirements.txt        # Project dependencies
└── run.py                 # Application entry point
```

## Setup and Installation

1. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Create a `.env` file in the project root with the following variables:
   ```
   FLASK_APP=run.py
   FLASK_ENV=development
   SECRET_KEY=your-secret-key-here
   DATABASE_URL=mysql+pymysql://user:password@localhost/dbname
   ```

4. Initialize the database:
   ```bash
   flask db upgrade
   ```

5. Run the development server:
   ```bash
   flask run
   ```

## Features

- User authentication and authorization
- Blog post management
- Email functionality
- Offer management
- Admin interface
- Persian date support

## Development

### Database Migrations

To create a new migration:
```bash
flask db migrate -m "Migration description"
flask db upgrade
```

### Running Tests

```bash
python -m pytest tests/
```

### Code Style

This project follows PEP 8 style guide. To check your code:
```bash
pylint email_func_app
```

## Security Notes

- Always use environment variables for sensitive data
- CSRF protection is enabled in production
- Database credentials should never be committed to version control
- Keep dependencies updated for security patches

## Contributing

1. Create a new branch for your feature
2. Write tests for new functionality
3. Ensure all tests pass
4. Submit a pull request

## License

This project is proprietary and confidential.
