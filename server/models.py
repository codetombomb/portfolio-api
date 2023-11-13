from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy_serializer import SerializerMixin

from config import db

class Admin(db.Model, SerializerMixin):
    __tablename__ = "admins"

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    email = db.Column(db.String)

    _password_hash = db.Column(db.String)
    
    @hybrid_property
    def password_hash(self):
        import ipdb; ipdb.set_trace()
        return self._password_hash
        raise Exception("Cannot access password hashes")
    
    @password_hash.setter
    def password_hash(self, password):
        hashed_pw = bcrypt.generate_password_hash(password).decode("utf-8")
        self._password_hash = hashed_pw

    def authenticate(self, provided_password):
        return bcrypt.check_password_hash(self._password_hash, provided_password)

    def __repr__(self):
        return f"\n<Admin id={self.id},\nfirst_name={self.first_name},\nlast_name={self.last_name}\nemail={self.email}\n>"
    
class Chat(db.Model, SerializerMixin):
    __tablename__ = "chats"

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    admin_id = db.Column(db.Integer, db.ForeignKey("admins.id"))
    visitor_id = db.Column(db.Integer, db.ForeignKey("visitors.id"))

    serialize_rules = ("-admin.chats", "-visitor.chats")
    messages = db.relationship("Message", backref="chats")

    def __repr__(self):
        return f"\n<Chat id={self.id},\nadmin_id={self.admin_id},\nvisitor_id={self.visitor_id} >"
    

class Message(db.Model, SerializerMixin):
    __tablename__ = "messages"
    id = db.Column(db.Integer, primary_key=True)

    created_at = db.Column(db.DateTime, server_default=db.func.now())
    content = db.Column(db.String)

    chat_id = db.Column(db.Integer, db.ForeignKey("chats.id"))

    serialize_rules = ("message.chats")



    






class Visitor(db.Model, SerializerMixin):
    __tablename__ = "visitors"

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    email = db.Column(db.String)

    def __repr__(self):
        return f"\n<User id={self.id},\nfirst_name={self.first_name},\nlast_name={self.last_name}\nemail={self.email}\n>"
    

    