# FastAPI Purchase API

A FastAPI-based REST API for purchase management with user authentication and role-based access control.

## Features

- User authentication with JWT
- Role-based access control (Admin, Supervisor, User)
- SQL Server database with SQLAlchemy ORM
- Alembic for database migrations
- Purchase request management
- Request status tracking
- Comment system for requests
- Audit trail for request changes
- CSV report generation
- Modular project structure

## Prerequisites

- Python 3.8+
- SQL Server
- pip (Python package manager)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/ifbriceno1996br/back-api-web-purchase.git
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
- Create a SQL Server database
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
│   │   │   ├── roles.py
│   │   │   ├── requests.py
│   │   │   ├── comments.py
│   │   │   └── audits.py
│   │   └── api.py
│   └── deps.py
├── core/
│   ├── config.py
│   └── security.py
├── crud/
│   ├── crud_user.py
│   ├── crud_role.py
│   └── crud_request.py
├── db/
│   ├── base_class.py
│   └── session.py
├── models/
│   ├── user.py
│   ├── role.py
│   ├── request.py
│   ├── comment.py
│   └── audit.py
├── schemas/
│   ├── user.py
│   ├── role.py
│   └── request.py
└── main.py
```

## API Endpoints

### Authentication
- POST /api/v1/login/access-token - Login and get access token
- POST /api/v1/login/test-token - Test access token

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

### Requests
- POST /api/v1/requests/ - Create a new request
- GET /api/v1/requests/ - Get all requests (filtered by user/supervisor)
- GET /api/v1/requests/{request_id} - Get a specific request
- PUT /api/v1/requests/{request_id} - Update a request
- PUT /api/v1/requests/{request_id}/status - Change request status (supervisor only)
- DELETE /api/v1/requests/{request_id} - Delete a request
- GET /api/v1/requests/report/csv - Download request report in CSV format

### Comments
- POST /api/v1/comments/ - Create a new comment
- GET /api/v1/comments/ - Get all comments
- GET /api/v1/comments/{comment_id} - Get a specific comment
- PUT /api/v1/comments/{comment_id} - Update a comment
- DELETE /api/v1/comments/{comment_id} - Delete a comment

### Audits
- GET /api/v1/audits/ - Get all audit records
- GET /api/v1/audits/{audit_id} - Get a specific audit record

## Request Status Flow

1. **Created** - Initial state when a request is created
2. **Pending** - Request is waiting for supervisor review
3. **Approved** - Request has been approved by supervisor
4. **Rejected** - Request has been rejected by supervisor
5. **Completed** - Request has been fulfilled

## Role Permissions

- **Admin**: Full access to all endpoints
- **Supervisor**: Can approve/reject requests, view all requests, and generate reports
- **User**: Can create and view their own requests

## Report Generation

The API provides a CSV report generation feature that includes:
- Request details
- User information
- Status history
- Comments
- Audit trail
- Metrics (days since creation, days until expected date)

Reports can be filtered by:
- Date range
- Status
- User ID

## License

This project is licensed under the MIT License. 