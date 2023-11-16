from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy_serializer import SerializerMixin

from config import db

class Admin(db.Model):
    __tablename__ = "admins"

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    email = db.Column(db.String)

    chats = db.relationship("Chat", backref="admins")

    serialize_rules = ("-admins", )

    _password_hash = db.Column(db.String)
    
    @hybrid_property
    def password_hash(self):
        return self._password_hash
        raise Exception("Cannot access password hashes")
    
    @password_hash.setter
    def password_hash(self, password):
        hashed_pw = bcrypt.generate_password_hash(password).decode("utf-8")
        self._password_hash = hashed_pw

    def authenticate(self, provided_password):
        return bcrypt.check_password_hash(self._password_hash, provided_password)

    def __repr__(self):
        return f"\n<Admin id={self.id},\n\tfirst_name={self.first_name},\n\tlast_name={self.last_name}\n\temail={self.email}\n>"
    
class Chat(db.Model):
    __tablename__ = "chats"

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    admin_id = db.Column(db.Integer, db.ForeignKey("admins.id"))
    visitor_id = db.Column(db.Integer, db.ForeignKey("visitors.id"))

    messages = db.relationship("Message", backref="chats")

    def __repr__(self):
        return f"\n<Chat id={self.id},\n\tcreated_at={self.created_at},\n\tadmin_id={self.admin_id},\n\tvisitor_id={self.visitor_id} \n>"
    

class Message(db.Model):
    __tablename__ = "messages"
    id = db.Column(db.Integer, primary_key=True)

    created_at = db.Column(db.DateTime, server_default=db.func.now())
    content = db.Column(db.String)

    chat_id = db.Column(db.Integer, db.ForeignKey("chats.id"))

    sender_type = db.Column(db.String)

    admin_id = db.Column(db.Integer, db.ForeignKey("admins.id"), nullable=True)
    admin = db.relationship("Admin", foreign_keys=[admin_id], backref="admin_messages")

    visitor_id = db.Column(db.Integer, db.ForeignKey("visitors.id"), nullable=True)
    visitor = db.relationship("Visitor", foreign_keys=[visitor_id], backref="visitor_messages")

    def __repr__(self):
        return f"\n<Message id={self.id},\n\tcreated_at={self.created_at},\n\tcontent={self.content},\n\tchat_id={self.chat_id},\n\tsender_type={self.sender_type},\n\tadmin_id={self.admin_id},\n\tvisitor_id={self.visitor_id}\n>"


class Visitor(db.Model):
    __tablename__ = "visitors"

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    email = db.Column(db.String)

    chats = db.relationship("Chat", backref="visitors")

    def __repr__(self):
        return f"\n<User id={self.id},\n\tfirst_name={self.first_name},\n\tlast_name={self.last_name}\n\temail={self.email}\n>"
    
