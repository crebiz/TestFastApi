# TestFastApi Backend Project

This is a FastAPI backend project with PostgreSQL integration.

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Environment Variables:
Create a `.env` file in the root directory with the following variables:
```
DB_HOST=localhost
DB_NAME=postgres
DB_USER=postgres
DB_PASSWORD=your_password
DB_PORT=5432

# JWT Settings
SECRET_KEY="your_secret_key"
ALGORITHM="HS256"
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

# Add any other required environment variables
```

3. Make sure PostgreSQL is running with the configuration specified in your `.env` file.

4. Run the server:
```bash
uvicorn main:app --reload
```

5. Access the API documentation at:
- http://localhost:8000/docs
- http://localhost:8000/redoc

## Project Structure

- `main.py`: Entry point of the application
- `database/`: Database configuration and connection management
- `model/`: SQLAlchemy models
- `schemas/`: Pydantic schemas for request/response validation
- `controller/`: API route handlers
- `service/`: Business logic
- `middleware/`: Custom middleware components
