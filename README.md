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

4. Create a `.env` file:
   - Copy the contents from [env.example](myproject/env.example) to a new file named `.env`.
   - Update the values in the `.env` file with your configuration. This file will contain sensitive information, so ensure it is kept secret and not shared.

5. Run migrations:
    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```

6. Create a superuser:
    ```bash
    python manage.py createsuperuser
    ```

7. Run the development server:
    ```bash
    python manage.py runserver
    ```

## API Documentation
Access the Swagger UI documentation at [http://localhost:8000/](http://localhost:8000/)

## Running Tests
Run tests using:
```bash
python manage.py test
