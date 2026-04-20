import os

class Config:
    # Secret key signs the session cookie so it can't be tampered with
    SECRET_KEY = os.environ.get("SECRET_KEY", "my-notes-app-secret-key")

    # SQLite database file stored in the project folder
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL", "sqlite:///notes.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Makes session cookies more secure
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"