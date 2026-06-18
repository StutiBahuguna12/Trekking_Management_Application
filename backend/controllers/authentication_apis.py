from flask_restful import Resource
from flask import request, jsonify, make_response
from flask_security import utils, auth_token_required
from controllers.user_datastore import user_datastore
from extensions import db
from flask_jwt_extended import create_access_token


class LoginAPI(Resource):
    def post(self):
        login_credentials=request.get_json()
        if not login_credentials:
            result={
                'message': 'Login credentials are required.'
            }
            return make_response(jsonify(result),400)
        email=login_credentials.get('email',None)
        password=login_credentials.get('password',None)

        if not email or not password:
            result={
                'message':'Email and password are required.'
            }
            return make_response(jsonify(result),400)
        
        user=user_datastore.find_user(email=email)

        if not user:
            result={
                'message': 'User not found'
            }
            return make_response(jsonify(result), 404)
        if not utils.verify_password(password, user.password):
            result={
                'message': 'Password invalid'
            }
            return make_response(jsonify(result), 401)
        auth_token=user.get_auth_token()

        utils.login_user(user)

        response={
            'message':'Login successfully',
             'user_details':{
                 'email': user.email,
                 'roles': [role.name for role in user.roles],
                 'auth_token': auth_token
             }
        }
        return make_response(jsonify(response), 200)

    
class RegisterAPI(Resource):

    def post(self):
        register_credentials = request.get_json()
        if not register_credentials:
            result = {
                'message': 'Register details are required'
            }
            return make_response(jsonify(result), 400)

        username = register_credentials.get('username')
        email = register_credentials.get('email')
        password = register_credentials.get('password')

        if not username or not email or not password:
            result = {
                'message': 'Enter all the information'
            }
            return make_response(jsonify(result), 400)

        existing_user = user_datastore.find_user(email=email)
        if existing_user:
            result = {
                'message': 'Email already registered'
            }
            return make_response(jsonify(result), 409)

        role_obj = user_datastore.find_role('user')
        user = user_datastore.create_user(
            username=username,
            email=email,
            password=utils.hash_password(password),
            roles=[role_obj]
        )
        db.session.add(user)
        db.session.commit()

        return make_response(jsonify({
            'message': 'Registration successful',
            'user_details': {
                'username': user.username,
                'email': user.email,
                'role': 'user'
            }
        }), 201)
        
class LogoutAPI(Resource):
    @auth_token_required
    def post(self):
        utils.logout_user()
        response={
            'message':'Logout successful.'
        }
        return make_response(jsonify(response),200)

        
        
        


