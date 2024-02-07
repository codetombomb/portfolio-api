from config import ma
from models import Admin, Chat, Message, Visitor, DeviceToken

class MessageSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Message
    id = ma.auto_field()
    created_at = ma.auto_field()
    content = ma.auto_field()
    sender_type = ma.auto_field()
    admin_id = ma.auto_field()
    visitor_id = ma.auto_field()

message_schema = MessageSchema()
messages_schema = MessageSchema(many=True)
    

class ChatSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Chat

    id = ma.auto_field()
    admin_id = ma.auto_field()
    visitor_id = ma.auto_field()

    is_active = ma.auto_field()
    room_id =  ma.auto_field()
    is_active = ma.auto_field()

    messages = ma.Nested(MessageSchema(only=("id", "created_at", "content", "sender_type", "admin_id", "visitor_id")),many=True)

chat_schema = ChatSchema()
chats_schema = ChatSchema(many=True)


class AdminSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Admin
    id = ma.auto_field()
    first_name = ma.auto_field()
    last_name = ma.auto_field()
    email = ma.auto_field()
    picture = ma.auto_field()
    name = ma.auto_field()
    is_active = ma.auto_field()
    
admin_schema = AdminSchema()
admins_schema = AdminSchema(many=True)


class VisitorSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Visitor
    id = ma.auto_field()
    first_name = ma.auto_field()
    last_name = ma.auto_field()
    email = ma.auto_field()

    chats = ma.Nested(ChatSchema(only=("id", "visitor_id", "messages", "room_id")),many=True)
    
visitor_schema = VisitorSchema()
visitors_schema = VisitorSchema(many=True)

class DeviceTokenSchema(ma.SQLAlchemySchema):
    class Meta:
        model = DeviceToken
    
    id = ma.auto_field()
    token = ma.auto_field()
    admin_id = ma.auto_field()
    created_at = ma.auto_field()
    updated_at = ma.auto_field()

device_token_schema = DeviceTokenSchema()
device_tokens_schema = DeviceTokenSchema(many=True)
