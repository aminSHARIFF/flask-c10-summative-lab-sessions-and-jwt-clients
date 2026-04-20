from flask import Flask
from flask_restful import Api

from config import Config
from extensions import db, migrate, bcrypt
from routes.auth import Signup, Login, Logout, CheckSession
from routes.notes import NoteList, NoteDetail


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # connect extensions to the app
    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)

    api = Api(app)

    # auth routes
    api.add_resource(Signup,        "/signup")
    api.add_resource(Login,         "/login")
    api.add_resource(Logout,        "/logout")
    api.add_resource(CheckSession,  "/check_session")

    # notes routes
    api.add_resource(NoteList,   "/notes")
    api.add_resource(NoteDetail, "/notes/<int:note_id>")

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True, port=5555)