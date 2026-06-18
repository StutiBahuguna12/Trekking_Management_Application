from flask import Flask
from flask_security import Security
from flask_restful import Api
import os
from dotenv import load_dotenv
from flask_cors import CORS
from controllers.authentication_apis import LoginAPI,RegisterAPI

from models import db
from controllers.config import config
from controllers.user_datastore import user_datastore



# https://dev.to/frontendmentor/16-front-end-projects-with-designs-to-help-improve-your-coding-skills-5ajl
def create_app():
    load_dotenv()
    app = Flask(__name__)
    app.config.from_object(config)

    db.init_app(app)
    security = Security(app, user_datastore)
    CORS(app)
    api = Api(app, prefix='/api')

    with app.app_context():
        db.create_all()

        admin_role = user_datastore.find_or_create_role(name='admin', description='Administrator')
        user_role = user_datastore.find_or_create_role(name='user', description='Regular User')
        if not user_datastore.find_user(email='email@email.com'):
            user_datastore.create_user(
                username="admin1",
                email="email@email.com",
                password="email@123",
                roles=[admin_role]
            )
        db.session.commit()

    api.add_resource(LoginAPI, '/login')
    api.add_resource(RegisterAPI, '/register')

    return app, api


app, api = create_app()

if __name__ == '__main__':
    app.run(debug=True)