<xaiArtifact artifact_id="331bd63b-9262-4ef7-8b97-f90867ae5d37" artifact_version_id="2f04d4f3-bc89-4cd3-b240-12f48f34388e" title="README for FastAPI User Management API" contentType="text/markdown">
FastAPI User Management API

## Overview
This project is a FastAPI-based RESTful API for managing user accounts, including signup, login, retrieval, update, and deletion of user data. It uses JWT for authentication, SQLAlchemy for database operations, and Pydantic for data validation.

## Features
- **User Signup**: Create a new user with a username, email, and password.
- **User Login**: Authenticate users and return a JWT token.
- **User Retrieval**: Fetch user details by ID (authenticated).
- **User Update**: Modify user details (authenticated).
- **User Deletion**: Remove a user from the database (authenticated).

## Requirements
- Python 3.8+
- FastAPI
- SQLAlchemy
- Pydantic
- Passlib (for password hashing)
- PyJWT (for JWT handling)
- A relational database (e.g., SQLite, PostgreSQL)

## Installation
1. **Clone the Repository**
   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```

2. **Install Dependencies**
   ```bash
   pip install fastapi uvicorn sqlalchemy pydantic passlib[bcrypt] pyjwt
   ```

3. **Database Setup**
   - Ensure a database is configured (e.g., SQLite by default).
   - Update the `database.py` file with your database URL if using a different database (e.g., PostgreSQL).
   - Run the script to create tables:
     ```python
     from database import engine
     import models
     models.Base.metadata.create_all(bind=engine)
     ```

4. **Run the Application**
   ```bash
   uvicorn main:app --reload
   ```
   The API will be available at `http://127.0.0.1:8000`.

## API Endpoints

### 1. User Signup
- **Endpoint**: `POST /users/signup`
- **Description**: Register a new user.
- **Request Body**:
  ```json
  {
    "username": "rohit",
    "email": "roh@gmail.com",
    "password": "asdf"
  }
  ```
- **Response**:
  - **201 Created**: `{"message": "User created successfully", "user_id": <id>}`
  - **400 Bad Request**: If username already exists.

### 2. User Login
- **Endpoint**: `POST /users/login`
- **Description**: Authenticate a user and return a JWT token.
- **Request Body**:
  ```json
  {
    "email": "roh@gmail.com",
    "password": "asdf"
  }
  ```
- **Response**:
  - **200 OK**: JWT token for authentication.
  - **401 Unauthorized**: If credentials are invalid.

### 3. Get User
- **Endpoint**: `GET /users/{user_id}`
- **Description**: Retrieve user details by ID.
- **Authentication**: Requires JWT token in the `Authorization` header (Bearer token).
- **Response**:
  - **200 OK**: User data.
  - **404 Not Found**: If user does not exist.

### 4. Update User
- **Endpoint**: `PUT /users/{user_id}`
- **Description**: Update user details.
- **Authentication**: Requires JWT token in the `Authorization` header.
- **Request Body**:
  ```json
  {
    "username": "roh",
    "email": "rohit@google.com",
    "password": "qwert"
  }
  ```
- **Response**:
  - **200 OK**: Updated user data.
  - **404 Not Found**: If user does not exist.
  - **400 Bad Request**: If data is invalid.

### 5. Delete User
- **Endpoint**: `DELETE /users/{user_id}`
- **Description**: Delete a user by ID.
- **Authentication**: Requires JWT token in the `Authorization` header.
- **Response**:
  - **204 No Content**: User deleted successfully.
  - **404 Not Found**: If user does not exist.

## Authentication
- Uses JWT (JSON Web Tokens) for securing endpoints.
- Protected endpoints (`GET /users/{user_id}`, `PUT /users/{user_id}`, `DELETE /users/{user_id}`) require a Bearer token in the `Authorization` header.
- Obtain the token via the `/users/login` endpoint.

## Database
- Uses SQLAlchemy ORM for database operations.
- Default setup uses SQLite, but can be configured for other databases (e.g., PostgreSQL) by modifying `database.py`.

## Security
- Passwords are hashed using `bcrypt` via the `passlib` library.
- JWT tokens are used for authentication, validated by the `jwtBearer` dependency.

## Dependencies
- **FastAPI**: Web framework for building the API.
- **SQLAlchemy**: ORM for database interactions.
- **Pydantic**: Data validation and serialization.
- **Passlib**: Password hashing.
- **PyJWT**: JWT token generation and validation.

## Running the API
- Start the server with:
  ```bash
  uvicorn main:app --host 127.0.0.1 --port 8000 --reload
  ```
- Access the interactive API docs at `http://127.0.0.1:8000/docs`.

## Notes
- Ensure the `models.py` and `database.py` files are correctly configured for your database.
- The `auth` module (e.g., `jwt_handler.py`, `bearer.py`) must be implemented for JWT functionality.
- Handle exceptions appropriately in production (e.g., database connection errors).

</xaiArtifact>
