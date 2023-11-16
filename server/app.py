from flask import request, make_response, session
from flask_restful import Resource
from werkzeug.exceptions import NotFound, Unauthorized

from models import Visitor, Admin

from config import app, api, db

from serializers import admin_schema, admins_schema

@app.route('/')
def index():
    return "<h1>Hello from root!</h1>"

class AdminsById(Resource):
    def get(self, id):
        admin = Admin.query.filter_by(id=id).first()
        # import ipdb; ipdb.set_trace()
        if not admin:
            raise NotFound
        response = make_response(
            admin_schema.dump(admin),
            200
        )

        return response

api.add_resource(AdminsById, '/admins/<int:id>')
        

if __name__ == '__main__':
    app.run(port=5000, debug=True)