import uuid
import json
import requests
import os
import random
import datetime
import ipdb

from flask import request, make_response, session, render_template, redirect
from flask_restful import Resource
from werkzeug.exceptions import NotFound
from models import Visitor, Admin, Chat, Message, Notification, DeviceToken
from config import app, api, db, client
from serializers import (
    admin_schema,
    admins_schema,
    chats_schema,
    chat_schema,
    message_schema,
    messages_schema
)

# For developement (allow http for oauthlib) - remove from production
# os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

@app.route("/")
def index():
    return render_template("index.html")


class AdminsById(Resource):
    def get(self, id):
        admin = Admin.query.filter_by(id=id).first()
        if not admin:
            raise NotFound
        response = make_response(admin_schema.dump(admin), 200)

        return response


api.add_resource(AdminsById, "/admins/<int:id>")


class Chats(Resource):
    def get(self):
        chats = Chat.query.filter_by(is_active=True).all()
        response = make_response(
            chats_schema.dump(chats),
            200,
        )
        return response
    
    def offline_message(self, chat_id, message="Visitor is trying to chat!"):
        default_messages_content= ["Hey there!👋  I'm CodeTomBot, Tom is currently offline so I'm sending him a notification."]
        iso_date = datetime.datetime.now().isoformat()
        default_message = Message(
            content=random.choice(default_messages_content),
            sender_type="Admin",
            chat_id=chat_id,
            created_at=iso_date
        )

        tom = Admin.query.filter_by(last_name="Tobar").first()

        notification = Notification(
            admin_id=tom.id,
            message=message,
            status="unread"
        )

        db.session.add_all([default_message, notification])
        db.session.commit()
        return default_message

    def post(self):
        form_json = request.get_json()

        if form_json["visitor_id"] == "":
            new_visitor = Visitor(first_name="Visitor", last_name=str(uuid.uuid4()))

            db.session.add(new_visitor)
            db.session.commit()
            form_json["visitor_id"] = new_visitor.id

        admin = Admin.query.filter_by(id=form_json["admin_id"]).first()

        new_chat = Chat(
            admin_id=admin.id,
            visitor_id=form_json["visitor_id"],
            room_id=form_json["room_id"],
        )

        
        db.session.add(new_chat)
        db.session.commit()

        if admin.name == "CodeTomBot":
            self.offline_message(new_chat.id)
            db.session.add(new_chat)
            db.session.commit()

        response = make_response(
            chat_schema.dump(new_chat),
            201,
        )

        return response


api.add_resource(Chats, "/chats")


class ChatsById(Resource):
    def get(self, id):
        chat = Chat.query.filter_by(id=id).first()
        response = make_response(
            chat_schema.dump(chat),
            200,
        )
        return response

    def patch(self, id):
        form_json = request.get_json()
        chat = Chat.query.filter_by(id=id).first()
        for attr in form_json:
            setattr(chat, attr, form_json[attr])

        db.session.add(chat)
        db.session.commit()

        response = make_response(chat_schema.dump(chat), 200)

        return response


api.add_resource(ChatsById, "/chats/<int:id>")

@app.route("/chatroom-update", methods=["POST"])
def chatroom_update():
        form_json = request.get_json()
        rooms = Chat.query.filter(Chat.room_id.in_(form_json["rooms"])).all()
        for room in rooms:
            new_message = Message(
                    content=f"{form_json["admin_name"]} joined the chat",
                    sender_type="Update",
                    chat_id=room
            )
            room.messages.append(new_message)
            db.session.add(room)
            db.session.commit()
        return make_response(chats_schema.dump(rooms), 200)
        


class Messages(Resource):
    def get(self):
        pass

    def post(self):
        form_json = request.get_json()

        created_at = Message.parse_iso_datetime(form_json["created_at"])

        new_message = Message(
            content=form_json["content"],
            sender_type=form_json["sender_type"],
            chat_id=form_json["chat_id"],
            created_at=created_at
        )

        if form_json["sender_type"] == "Visitor":
            new_message.visitor_id = form_json["visitor_id"]
        else:
            new_message.admin_id = form_json["admin_id"]

        db.session.add(new_message)
        db.session.commit()

        response = make_response(
            message_schema.dump(new_message),
            201,
        )

        return response


api.add_resource(Messages, "/messages")

class DeviceTokens(Resource):
    def post(self):
        json_data = request.get_json()
        
        if DeviceToken.query.filter_by(token=json_data["token"]).first():
                return make_response({"errors": ["A device with that token already exists"]}, 400)
        
        device_token = DeviceToken(
            token=json_data["token"],
            admin_id=json_data.get("admin_id")
        )
        
        db.session.add(device_token)
        db.session.commit()
        return make_response({"message": "Device Token created successfully"}, 201)

api.add_resource(DeviceTokens, "/device_tokens")


class DeviceTokenById(Resource):
    def get(self, token):
        device_token = DeviceToken.query.filter_by(token=token).first()
        if device_token:
            return make_response(admin_schema.dump(device_token), 200)
        else: 
            return make_response({"errors": ["Device token not found"]}, 404)
        
    def put(self, token):
        json_data = request.get_json()
        print(json_data)
        device_token = DeviceToken.query.filter_by(token=token).first()
        print(json_data.get("token"))
        if device_token:
            if json_data.get("admin_id"):
                print("has admin_id")
                device_token.admin_id = json_data.get("admin_id")
            if json_data.get("token"):
                print("has token")
                device_token.token = json_data.get("token")
            db.session.add(device_token)
            db.session.commit()
            return make_response({"message": "Device token updated successfully."}, 200)
        return make_response({"errors": ["Device token not found"]}, 404)

    def delete(self, token):
        device_token = DeviceToken.query.filter_by(token=token).first()
        if device_token:
            db.session.delete(device_token)
            db.session.commit()
            return make_response({"message": "Device token deleted successfully."}, 200)
        return make_response({"message": "Device token not found"}, 404)

api.add_resource(DeviceTokenById, "/device_tokens/<string:token>")


def get_google_provider_cfg():
    return requests.get(os.environ.get("GOOGLE_DISCOVERY_URL")).json()

@app.route("/login")
def login():
    google_provider_cfg = get_google_provider_cfg()
    authorization_endpoint = google_provider_cfg["authorization_endpoint"]
    
    request_uri = client.prepare_request_uri(
        authorization_endpoint,
        redirect_uri=request.base_url + "/callback",
        scope=["openid", "email", "profile"]
    )

    return redirect(request_uri)


@app.route("/login/callback")
def callback():
    code = request.args.get("code")
    google_provider_cfg = get_google_provider_cfg()
    token_endpoint = google_provider_cfg["token_endpoint"]

    token_url, headers, body = client.prepare_token_request(
        token_endpoint,
        authorization_response=request.url,
        redirect_url=request.base_url,
        code=code
    )

    token_response = requests.post(
        token_url,
        headers=headers,
        data=body,
        auth=(os.environ.get("GOOGLE_CLIENT_ID"), os.environ.get("GOOGLE_CLIENT_SECRET"))
    )

    client.parse_request_body_response(json.dumps(token_response.json()))

    admininfo_endpoint = google_provider_cfg["userinfo_endpoint"]
    uri, headers, body = client.add_token(admininfo_endpoint)
    admininfo_response = requests.get(uri, headers=headers, data=body).json()

    email_whitelist = ["codetombomb@gmail.com", "ashton.s.tobar@gmail.com"]
    admin = Admin.query.filter_by(last_name=admininfo_response["family_name"]).first()
    if not admin and admininfo_response["email"] in email_whitelist:
        admin = Admin(
            email=admininfo_response["email"],
            first_name=admininfo_response["given_name"],
            last_name=admininfo_response["family_name"],
            picture=admininfo_response["picture"],
            name=admininfo_response["name"],
        )
        admin.is_active = True
        session["admin_id"] = admin.id
        db.session.add(admin)
        db.session.commit()
        redirect_url = f"{os.environ.get('FRONTEND_URL')}/admin/?admin={admin_schema.dumps(admin)}"
        return redirect(redirect_url)

    if admin and admin.email in email_whitelist:
        session["admin_id"] = admin.id
        admin.is_active = True
        db.session.add(admin)
        db.session.commit()
        redirect_url = f"{os.environ.get('FRONTEND_URL')}/admin/?admin={admin_schema.dumps(admin)}"
        return redirect(redirect_url)
    else:
        response = make_response({"errors": ["Not authorized"]}, 401)
        return response


@app.route("/logout/<int:id>", methods=["DELETE"])
def logout(id):
    admin = Admin.query.filter(Admin.id == id).first()
    admin.is_active = False
    db.session.add(admin)
    db.session.commit()
    session["admin_id"] = None

    tom_bot = Admin.query.filter_by(last_name="Bot").first()

    return make_response(admin_schema.dump(tom_bot), 200)


@app.route("/current_admin", methods=["GET"])
def current_admin():
    tom_tobar = Admin.query.filter_by(last_name="Tobar").first()
    if tom_tobar.is_active:
        return make_response(admin_schema.dump(tom_tobar), 200)
    else:
        tom_bot = Admin.query.filter_by(last_name="Bot").first()
        return make_response(admin_schema.dump(tom_bot), 200)

    
if __name__ == "__main__":
    app.run(port=5000, debug=True)
