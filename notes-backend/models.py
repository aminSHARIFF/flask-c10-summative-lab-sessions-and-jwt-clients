from extensions import db, bcrypt
from sqlalchemy.orm import validates


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    # underscore means don't access this directly
    _password_hash = db.Column(db.String(128), nullable=False)

    # one user has many notes, delete notes if user is deleted
    notes = db.relationship("Note", backref="user", cascade="all, delete-orphan", lazy=True)

    @property
    def password_hash(self):
        raise AttributeError("You can't read the password hash directly.")

    @password_hash.setter
    def password_hash(self, plain_password):
        # hash the password before saving it
        self._password_hash = bcrypt.generate_password_hash(plain_password).decode("utf-8")

    def authenticate(self, plain_password):
        # check if the given password matches the stored hash
        return bcrypt.check_password_hash(self._password_hash, plain_password)

    @validates("username")
    def validate_username(self, key, username):
        if not username or len(username.strip()) < 3:
            raise ValueError("Username must be at least 3 characters.")
        return username.strip()

    def to_dict(self):
        return {"id": self.id, "username": self.username}


class Note(db.Model):
    __tablename__ = "notes"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    content = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(60), nullable=False, default="General")
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now())

    # foreign key links each note to its owner
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    @validates("title")
    def validate_title(self, key, title):
        if not title or len(title.strip()) == 0:
            raise ValueError("Title can't be empty.")
        return title.strip()

    @validates("content")
    def validate_content(self, key, content):
        if not content or len(content.strip()) == 0:
            raise ValueError("Content can't be empty.")
        return content.strip()

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "content": self.content,
            "category": self.category,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "user_id": self.user_id,
        }