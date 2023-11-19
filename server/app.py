from flask import request, make_response, session
from flask_restful import Resource
from werkzeug.exceptions import NotFound, Unauthorized

from models import Visitor, Admin, Chat

from config import app, api, db

from serializers import admin_schema, admins_schema, chats_schema, chat_schema, messages_schema, message_schema

import uuid

@app.route('/')
def index():
    return "<h1>Hello from root!</h1>"

class AdminsById(Resource):
    def get(self, id):
        admin = Admin.query.filter_by(id=id).first()
        if not admin:
            raise NotFound
        response = make_response(
            admin_schema.dump(admin),
            200
        )

        return response
api.add_resource(AdminsById, '/admins/<int:id>')

class Chats(Resource):

    def get(self):    
        chats = Chat.query.all()
        response = make_response(
            chats_schema.dump(chats),
            200,
        )
        return response
    

    def post(self):
        form_json = request.get_json()
        
        if form_json["visitor_id"] == "":
            new_visitor = Visitor(
                first_name="Visitor",
                last_name=str(uuid.uuid4())
            )

            db.session.add(new_visitor)
            db.session.commit()
            form_json["visitor_id"] = new_visitor.id

        if form_json["admin_id"] == "":
            new_admin = Admin(
                first_name="Admin",
                last_name=str(uuid.uuid4())
            )

            db.session.add(new_admin)
            db.session.commit()
            form_json["admin_id"] = new_admin.id


        new_chat = Chat(
            admin_id=form_json['admin_id'],
            visitor_id=form_json['visitor_id'],
            room_id=form_json['room_id']
        )

        db.session.add(new_chat)
        db.session.commit()

        response = make_response(
            chat_schema.dump(new_chat),
            201,
        )

        return response

api.add_resource(Chats, '/chats')
        

if __name__ == '__main__':
    app.run(port=5000, debug=True)