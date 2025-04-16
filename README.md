# FastAPI Purchase API

A FastAPI-based REST API for purchase management with user authentication and role-based access control.

## Features

- User authentication with JWT
- Role-based access control
- PostgreSQL database with SQLAlchemy ORM
- Alembic for database migrations
- Modular project structure

## Prerequisites

- Python 3.8+
- PostgreSQL
- pip (Python package manager)

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd WebApiPurchase
```

2. Create and activate a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up the database:
- Create a PostgreSQL database named `purchase_db`
- Update the database connection settings in `app/core/config.py` if needed

5. Run database migrations:
```bash
alembic upgrade head
```

## Running the Application

Start the FastAPI server:
```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

## API Documentation

Once the server is running, you can access:
- Swagger UI documentation: `http://localhost:8000/docs`
- ReDoc documentation: `http://localhost:8000/redoc`

## Project Structure

```
app/
├── api/
│   ├── v1/
│   │   ├── endpoints/
│   │   │   ├── users.py
│   │   │   └── roles.py
│   │   └── api.py
│   └── deps.py
├── core/
│   ├── config.py
│   └── security.py
├── crud/
│   ├── crud_user.py
│   └── crud_role.py
├── db/
│   ├── base_class.py
│   └── session.py
├── models/
│   ├── user.py
│   └── role.py
├── schemas/
│   ├── user.py
│   └── role.py
└── main.py
```

## API Endpoints

### Users
- POST /api/v1/users/ - Create a new user
- GET /api/v1/users/ - Get all users
- GET /api/v1/users/{user_id} - Get a specific user
- PUT /api/v1/users/{user_id} - Update a user
- DELETE /api/v1/users/{user_id} - Delete a user

### Roles
- POST /api/v1/roles/ - Create a new role
- GET /api/v1/roles/ - Get all roles
- GET /api/v1/roles/{role_id} - Get a specific role
- PUT /api/v1/roles/{role_id} - Update a role
- DELETE /api/v1/roles/{role_id} - Delete a role

## License

This project is licensed under the MIT License. 