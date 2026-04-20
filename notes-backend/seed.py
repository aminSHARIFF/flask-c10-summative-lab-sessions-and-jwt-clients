from faker import Faker
from app import app
from extensions import db
from models import User, Note

fake = Faker()

CATEGORIES = ["Work", "Personal", "Ideas", "Shopping", "Health", "Study"]

def seed():
    with app.app_context():
        print("Seeding database...")

        db.drop_all()
        db.create_all()

        # create two demo users with easy passwords for testing
        amin = User(username="amin")
        amin.password_hash = "password123"
        db.session.add(amin)

        testuser = User(username="testuser")
        testuser.password_hash = "password123"
        db.session.add(testuser)

        # create 3 more random users
        extra_users = []
        for _ in range(3):
            u = User(username=fake.unique.user_name())
            u.password_hash = "password123"
            db.session.add(u)
            extra_users.append(u)

        db.session.commit()

        all_users = [amin, testuser] + extra_users

        # give each user some notes
        for user in all_users:
            for _ in range(5):
                note = Note(
                    title=fake.sentence(nb_words=4).rstrip("."),
                    content=fake.paragraph(nb_sentences=2),
                    category=fake.random_element(CATEGORIES),
                    user_id=user.id,
                )
                db.session.add(note)

        db.session.commit()
        print("Done! Login with username: amin, password: password123")

if __name__ == "__main__":
    seed()