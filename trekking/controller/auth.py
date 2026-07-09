from flask import request
from flask_jwt_extended import (create_access_token,jwt_required,get_jwt_identity)
from flask_restful import Resource
from model import db, User




class RegisterAPI(Resource):
    def post(self):
        data = request.get_json()
        name = data.get("name")
        email = data.get("email")
        password = data.get("password")
        phone = data.get("phone")
        if not all([name, email, password, phone]):
            return {"message": "All fields are required."}, 400
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            return {"message": "Email already exists."}, 400
        user = User(
            name=name,
            email=email,
            phone=phone,
            role="user"
        )
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        return {"message": "Registration successful."}, 201



class LoginAPI(Resource):

    def post(self):
        data = request.get_json()
        if not data:
            return {"message": "No data received."}, 400
        email = data.get("email")
        password = data.get("password")
        if not all([email, password]):
            return {"message": "Email and password are required."}, 400
        user = User.query.filter_by(email=email).first()
        if not user:
            return {"message": "Invalid email or password."}, 401
        if not user.check_password(password):
            return {"message": "Invalid email or password."}, 401
        if not user.active:
            return {"message": "Your account has been deactivated."}, 403
        access_token = create_access_token(identity=str(user.id))
        return {
            "message": "Login successful.",
            "access_token": access_token,
            "role": user.role,
            "name": user.name
        }, 200
    
class ProfileAPI(Resource):

    @jwt_required()
    def get(self):

        user_id = int(get_jwt_identity())

        user = db.session.get(User, user_id)

        if not user:
            return {
                "success": False,
                "message": "User not found."
            }, 404

        return {
            "success": True,
            "user": {
                "id": user.id,
                "name": user.name,
                "email": user.email,
                "phone": user.phone,
                "role": user.role
            }
        }, 200