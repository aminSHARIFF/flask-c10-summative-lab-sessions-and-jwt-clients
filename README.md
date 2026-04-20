# Notes App - Flask Backend

A simple REST API backend for a personal notes app. Users can sign up, log in, and manage their own notes. Built with Flask and session-based authentication.

## What it does
- Users can register and log in securely
- Each user can create, read, update and delete their own notes
- Users can only see their own notes, not other people's
- Notes can be filtered by page number

## Installation

1. Clone the repo and navigate to the notes-backend folder:
```bash
cd notes-backend
```

2. Install dependencies:
```bash
pipenv install
pipenv shell
```

3. Set up the database:
```bash
flask db init
flask db migrate -m "create tables"
flask db upgrade
```

4. Seed the database with sample data:
```bash
python seed.py
```

## Running the app
```bash
python app.py
```
App runs on http://localhost:5555

## Test credentials
- username: `amin` password: `password123`
- username: `testuser` password: `password123`

## Endpoints

### Auth
| Method | Route | Description |
|--------|-------|-------------|
| POST | /signup | Create a new account |
| POST | /login | Log in |
| DELETE | /logout | Log out |
| GET | /check_session | Check if logged in |

### Notes
| Method | Route | Description |
|--------|-------|-------------|
| GET | /notes | Get all my notes (paginated) |
| POST | /notes | Create a new note |
| PATCH | /notes/<id> | Update a note |
| DELETE | /notes/<id> | Delete a note |

## Tech used
- Python 3.8
- Flask 2.2.2
- Flask-SQLAlchemy
- Flask-Migrate
- Flask-Bcrypt
- Flask-RESTful