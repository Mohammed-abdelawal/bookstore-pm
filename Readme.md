# BookStore API

Bookstore API is a Django-based application that allows users to read and review books. This project includes user authentication, book management, and review functionality.

## Features

- User registration and login with JWT authentication
- Book management (view books, view book details)
- User reviews for books
- File upload validation for books (PDF or DOC only, size limit)
- Throttling to protect the API from abuse

## Setup Instructions

### Prerequisites

- Python 3.10 or higher as we use Django 5.0
- PostgreSQL

### Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/Mohammed-abdelawal/bookstore-pm.git
   cd bookstore-pm
   ```

2. **Create and activate a virtual environment:**

   ```bash
   python -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables:**

   Copy `.env.example` contents to your `.env` and edit the variables aas yours
      ```bash
   cp .env.example .env
   ```


5. **Apply migrations:**

   ```bash
   python manage.py migrate
   ```

6. **Create a superuser:**

   ```bash
   python manage.py createsuperuser
   ```

7. **Run the development server:**

   ```bash
   python manage.py runserver
   ```

### Running Tests

1. **Run tests:**

   ```bash
   python manage.py test
   ```

2. **Run tests with coverage:**

   ```bash
   coverage run --source='.' manage.py test
   coverage report
   ```

   To generate an HTML report:

   ```bash
   coverage html
   ```

   Open `htmlcov/index.html` in your web browser to view the coverage report.

### Configuration

#### Throttling

Throttling settings are configured in `settings.py` under the `REST_FRAMEWORK` settings. Adjust the rates as needed:

```python
REST_FRAMEWORK = {
    'DEFAULT_THROTTLE_CLASSES': (
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle',
    ),
    'DEFAULT_THROTTLE_RATES': {
        'anon': '100/day',
        'user': '1000/day'
    },
}
```

#### File Upload Validation

File upload validation settings are configured in `settings.py`:

```python
BOOK_FILE_SIZE_LIMIT_MB = 5.0  # Size limit in megabytes
BOOK_FILE_VALID_EXTENSIONS = ['.pdf']
```

### API Documentation

API documentation is available via Swagger and ReDoc.

- **Swagger UI**: [http://localhost:8000/swagger/](http://localhost:8000/swagger/)
- **ReDoc**: [http://localhost:8000/redoc/](http://localhost:8000/redoc/)
