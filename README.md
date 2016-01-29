# OILS

## Setup

    # Install dependencies
    npm install
    pip install -r requirements.txt

    # Build Assets
    npm run build
    python manage.py collectstatic

    # Migrate Database
    python manage.py migrate

    # Run Server
    python manage.py runserver 0.0.0.0:8000
