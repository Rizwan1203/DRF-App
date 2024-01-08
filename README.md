# My Project

## Table of Contents
- [Setup](#setup)
- [API Documentation](#api-documentation)
- [Running Tests](#running-tests)

## Setup
1. Create and activate a virtual environment:
    ```bash
    python3 -m venv venv
    source venv/bin/activate   # On Unix or MacOS
    # OR
    .\venv\Scripts\activate    # On Windows
    ```

2. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
3. Move into the `myproject` directory:
    ```bash
    cd myproject
    ```

4. Run migrations:
    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```

5. Create a superuser:
    ```bash
    python manage.py createsuperuser
    ```

6. Run the development server:
    ```bash
    python manage.py runserver
    ```

## API Documentation
Access the Swagger UI documentation at [http://localhost:8000/](http://localhost:8000/)

## Running Tests
Run tests using:
```bash
python manage.py test
