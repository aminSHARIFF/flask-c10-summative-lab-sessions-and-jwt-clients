from flask import session, request
from flask_restful import Resource
from models import User
from extensions import db


class Signup(Resource):
    def post(self):
        data = request.get_json()

        # make sure username and password were sent
        if not data or not data.get("username") or not data.get("password"):
            return {"error": "Username and password are required."}, 422

        # check if username is already taken
        if User.query.filter_by(username=data["username"]).first():
            return {"error": "Username already taken."}, 422

        try:
            user = User(username=data["username"])
            user.password_hash = data["password"]
            db.session.add(user)
            db.session.commit()
        except ValueError as e:
            return {"error": str(e)}, 422

        # log the user in right after signing up
        session["user_id"] = user.id
        return user.to_dict(), 201


class Login(Resource):
    def post(self):
        data = request.get_json()

        if not data or not data.get("username") or not data.get("password"):
            return {"error": "Username and password are required."}, 422

        user = User.query.filter_by(username=data["username"]).first()

        if user and user.authenticate(data["password"]):
            session["user_id"] = user.id
            return user.to_dict(), 200

        return {"error": "Wrong username or password."}, 401


class Logout(Resource):
    def delete(self):
        # clear the session
        session.pop("user_id", None)
        return {}, 204


class CheckSession(Resource):
    def get(self):
        user_id = session.get("user_id")

        if not user_id:
            return {"error": "Not logged in."}, 401

        user = User.query.get(user_id)

        if not user:
            session.pop("user_id", None)
            return {"error": "User not found."}, 401

        return user.to_dict(), 200