from ipdb import set_trace
from faker import Faker
import random

from config import app, db
from models import Visitor, Admin, Chat, Message

fake = Faker()

with app.app_context():
    
    def clear_entries():
        db.drop_all()
        db.create_all()
        # Admin.query.delete()
        # Chat.query.delete()
        # Message.query.delete()
        # Visitor.query.delete()

    def create_admin():
        first_name = fake.first_name()
        last_name = fake.last_name()
        new_admin = Admin(
            first_name=first_name,
            last_name=last_name,
            email=f"{first_name.lower()}.{last_name.lower()}@gmail.com"
        )
        db.session.add(new_admin)
        db.session.commit()
        return new_admin

    def create_visitor():
        first_name = fake.first_name()
        last_name = fake.last_name()
        new_visitor = Visitor(
            first_name=first_name,
            last_name=last_name,
            email=f"{first_name.lower()}.{last_name.lower()}@gmail.com"
        )
        db.session.add(new_visitor)
        db.session.commit()
        return new_visitor
    
    def create_chat(admin_id, visitor_id):
        new_chat = Chat(
            admin_id=admin_id,
            visitor_id=visitor_id
        )

        db.session.add(new_chat)
        db.session.commit()
        return new_chat
    
    def create_message(content, sender_type, chat_id, visitor_id=None, admin_id=None):
        message = Message(
            content=content,
            sender_type=sender_type,
            chat_id=chat_id,
            visitor_id=visitor_id,
            admin_id=admin_id,
        )
        db.session.add(message)
        db.session.commit()
        return message

    def seed_db():
        print("Seeding 🌱")
        clear_entries()
        for _ in range(5):
            admin = create_admin() 
            visitor = create_visitor()
            new_chat = create_chat(admin.id,visitor.id)
            
            for _ in range(5):
                create_message(
                    fake.paragraph(nb_sentences=random.randint(0, 3)), 
                    "admin", 
                    new_chat.id,
                    admin_id=admin.id, 
                )

            # content=content,
            # sender_type=sender_type,
            # chat_id=chat_id,
            # visitor_id=visitor_id,
            # admin_id=admin_id,

                create_message(
                    fake.paragraph(nb_sentences=random.randint(0, 3)),
                    "visitor",
                    new_chat.id,
                    visitor.id
                )


        
        print("Done seeding ✅")

    # seed_db()
    clear_entries()
        



       

        
    

