from flask import session, request
from flask_restful import Resource
from models import Note
from extensions import db


def current_user_id():
    # helper to get the logged in user's id from the session
    return session.get("user_id")


class NoteList(Resource):
    def get(self):
        user_id = current_user_id()
        if not user_id:
            return {"error": "You need to log in first."}, 401

        # grab page and per_page from the URL e.g. /notes?page=1&per_page=5
        page = request.args.get("page", 1, type=int)
        per_page = request.args.get("per_page", 5, type=int)

        # only fetch notes that belong to the logged in user
        paginated = (
            Note.query
            .filter_by(user_id=user_id)
            .order_by(Note.created_at.desc())
            .paginate(page=page, per_page=per_page, error_out=False)
        )

        return {
            "notes": [note.to_dict() for note in paginated.items],
            "total": paginated.total,
            "pages": paginated.pages,
            "current_page": paginated.page,
        }, 200

    def post(self):
        user_id = current_user_id()
        if not user_id:
            return {"error": "You need to log in first."}, 401

        data = request.get_json()
        if not data:
            return {"error": "No data provided."}, 422

        try:
            note = Note(
                title=data.get("title", ""),
                content=data.get("content", ""),
                category=data.get("category", "General"),
                user_id=user_id,
            )
            db.session.add(note)
            db.session.commit()
        except ValueError as e:
            return {"error": str(e)}, 422

        return note.to_dict(), 201


class NoteDetail(Resource):

    def _get_my_note(self, note_id):
        # reusable helper - fetch note and verify it belongs to current user
        user_id = current_user_id()
        if not user_id:
            return None, ({"error": "You need to log in first."}, 401)

        note = Note.query.get(note_id)
        if not note:
            return None, ({"error": "Note not found."}, 404)

        # stop other users from touching this note
        if note.user_id != user_id:
            return None, ({"error": "That's not your note."}, 403)

        return note, None

    def get(self, note_id):
        # return a single note by id
        note, error = self._get_my_note(note_id)
        if error:
            return error
        return note.to_dict(), 200

    def patch(self, note_id):
        note, error = self._get_my_note(note_id)
        if error:
            return error

        data = request.get_json()
        if not data:
            return {"error": "No data provided."}, 422

        try:
            if "title" in data:
                note.title = data["title"]
            if "content" in data:
                note.content = data["content"]
            if "category" in data:
                note.category = data["category"]
            db.session.commit()
        except ValueError as e:
            return {"error": str(e)}, 422

        return note.to_dict(), 200

    def delete(self, note_id):
        note, error = self._get_my_note(note_id)
        if error:
            return error

        db.session.delete(note)
        db.session.commit()
        return {}, 204