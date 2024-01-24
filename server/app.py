import uuid
import json
import requests
import os

from flask import request, make_response, session, render_template, redirect
from flask_restful import Resource
from werkzeug.exceptions import NotFound
from models import Visitor, Admin, Chat, Message
from config import app, api, db, client
from serializers import (
    admin_schema,
    admins_schema,
    chats_schema,
    chat_schema,
    message_schema,
)

# For developement (allow http for oauthlib) - remove from production
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

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

    def post(self):
        form_json = request.get_json()

        if form_json["visitor_id"] == "":
            new_visitor = Visitor(first_name="Visitor", last_name=str(uuid.uuid4()))

            db.session.add(new_visitor)
            db.session.commit()
            form_json["visitor_id"] = new_visitor.id

        if form_json["admin_id"] == "":
            new_admin = Admin(first_name="Admin", last_name=str(uuid.uuid4()))

            db.session.add(new_admin)
            db.session.commit()
            form_json["admin_id"] = new_admin.id

        new_chat = Chat(
            admin_id=form_json["admin_id"],
            visitor_id=form_json["visitor_id"],
            room_id=form_json["room_id"],
        )

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

        print(chat_schema.dump(chat))

        return response


api.add_resource(ChatsById, "/chats/<int:id>")


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

def get_google_provider_cfg():
    return requests.get(os.environ.get("GOOGLE_DISCOVERY_URL")).json()

@app.route("/login")
def login():
    print("Logging in")
    google_provider_cfg = get_google_provider_cfg()
    authorization_endpoint = google_provider_cfg["authorization_endpoint"]
    
    request_uri = client.prepare_request_uri(
        authorization_endpoint,
        redirect_uri=request.base_url + "/callback",
        scope=['openid', 'email', 'profile']
    )

    return redirect(request_uri)


@app.route("/login/callback")
def callback():

    print("in the callback")

    code = request.args.get("code")
    print("This is the code", code)
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
        auth=(os.environ.get('GOOGLE_CLIENT_ID'), os.environ.get('GOOGLE_CLIENT_SECRET'))
    )

    client.parse_request_body_response(json.dumps(token_response.json()))

    admininfo_endpoint = google_provider_cfg["userinfo_endpoint"]
    uri, headers, body = client.add_token(admininfo_endpoint)
    admininfo_response = requests.get(uri, headers=headers, data=body).json()

    email_whitelist = ["codetombomb@gmail.com", "ashton.s.tobar@gmail.com"]

    admin = Admin.query.filter(Admin.email == admininfo_response["email"]).first()

    if not admin and admininfo_response["email"] in email_whitelist:
        print("creating admin")
        admin = Admin(
            email=admininfo_response["email"],
            first_name=admininfo_response["first_name"],
            last_name=admininfo_response["last_name"],
            picture=admininfo_response["picture"],
            name=admininfo_response["name"],
        )
        admin.is_active = True
        session["admin_id"] = admin.id
        db.session.add(admin)
        db.session.commit()
        redirect_url = f"{os.environ.get('FRONTEND_URL')}/?admin={admin_schema.dumps(admin)}"
        return redirect(redirect_url)

    if admin and admin.email in email_whitelist:
        print("Admin exists and email whitelisted")
        session["admin_id"] = admin.id
        admin.is_active = True
        db.session.add(admin)
        db.session.commit()
        redirect_url = f"{os.environ.get('FRONTEND_URL')}/?admin={admin_schema.dumps(admin)}"
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

    return {}, 204


@app.route("/current_admins", methods=["GET"])
def current_admins():
    admins = Admin.query.filter(Admin.is_active == True).all()
    response = make_response(admins_schema.dump(admins), 200)
    return response


if __name__ == "__main__":
    app.run(port=5000, debug=True)
