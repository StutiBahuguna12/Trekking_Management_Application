from flask_security import SQLAlchemyUserDatastore
from models import User,Role


from extensions import db

user_datastore =SQLAlchemyUserDatastore(db,User,Role)
