from config import ma
from models import Admin, Chat, Message

class MessageSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Message
    id = ma.auto_field()
    created_at = ma.auto_field()
    content = ma.auto_field()
    sender_type = ma.auto_field()
    admin_id = ma.auto_field()
    visitor_id = ma.auto_field()
    

class ChatSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Chat

    id = ma.auto_field()
    created_at = ma.auto_field()
    admin_id = ma.auto_field()
    visitor_id = ma.auto_field()

    messages = ma.Nested(MessageSchema(only=("id", "created_at", "content", "sender_type", "admin_id", "visitor_id", )),many=True)


class AdminSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Admin
    id = ma.auto_field()
    first_name = ma.auto_field()
    last_name = ma.auto_field()
    email = ma.auto_field()

    chats = ma.Nested(ChatSchema(only=("id", "created_at", "visitor_id", "messages")),many=True)
    
admin_schema = AdminSchema()
admins_schema = AdminSchema(many=True)