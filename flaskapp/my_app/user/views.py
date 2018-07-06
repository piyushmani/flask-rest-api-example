import json
from flask import request, jsonify, Blueprint, abort
from flask.views import MethodView
from flask import make_response
from my_app import db, app
from my_app.user.models import User
 
user_blueprint = Blueprint('user', __name__)
 
@user_blueprint.route('/')
@user_blueprint.route('/home')
def home():
    return "Welcome to the library Home."

@user_blueprint.route('/profile')
def profile():
    auth_header = request.headers.get('Authorization')
    access_token = auth_header.split(" ")[0]

    if access_token:
         # Attempt to decode the token and get the User ID
            user_id = User.decode_token(access_token)
            user=User.query.filter_by(id=user_id).first()
            res = {
                'name': user.name,
                'username': user.username,
            }
            return jsonify(res)
 
 
class UserView(MethodView):
 
    def get(self, id=None ):
        auth_header = request.headers.get('Authorization')
        access_token = auth_header.split(" ")[0]

        if access_token:
         # Attempt to decode the token and get the User ID
            user_id = User.decode_token(access_token)
            user=User.query.filter_by(id=user_id).first()
            if user.isAdmint == True :
                if not id:
                    res={}
                    users = User.query.all()
                    res = {}
                    for usr in users:
                        res[usr.id] = {
                            'name': usr.name,
                            'username': str(usr.username),
                        }
                    return jsonify(res)
                else:
                    usr = User.query.filter_by(id=id).first()
                    if not usr:
                        abort(404)
                    res = {
                        'name': usr.name,
                        'username': str(usr.username),
                    }
                return jsonify(res)
            else :
                response = {
                     'message': 'you are not authorized to see the page.'
                 }

                return jsonify(response)    
                    
 
    def post(self):
        name = request.form.get('name')
        username = request.form.get('username')
        exit_user = User.query.filter_by(username=username).first()
        if not exit_user:
            password = request.form.get('password')
            usr = User(name, username,password)
            db.session.add(usr)
            db.session.commit()
            return jsonify({usr.id: {

                'name': usr.name,
                'username': str(usr.username),
            }})
        else :
            response = {
                 'message': 'User already exists. Please login.'
             }

            return jsonify(response)
                 
 
    def put(self, id):
        # Update the record for the provided id
        # with the details provided.
        return
 
    def delete(self, id):
        if User.isAdmin(request) :
            user = User.query.filter_by(id=id).first()
            if user :
                user.delete()
                return jsonify({'msg': 'user deleted'})
            else :
                return jsonify({'msg': 'user not found'})

        else :
            response = {
                 'message': 'you are not allowed to delete user.'
             }

            return jsonify(response)

class LoginView(MethodView):
    """This class-based view handles user login and access token generation."""

    def post(self):
        """Handle POST request for this view. Url ---> /auth/login"""
        try:
            # Get the user object using their email (unique to every user)
            user = User.query.filter_by(username=request.form.get('username')).first()
            # Try to authenticate the found user using their password
            if user and user.password == request.form.get('password'):
                # Generate the access token. This will be used as the authorization header
                access_token = user.generate_token(user.id)
                if access_token:
                    response = {
                        'message': 'You logged in successfully.',
                        'access_token': access_token.decode()
                    }
                    return make_response(jsonify(response)), 200
            else:
                # User does not exist. Therefore, we return an error message
                response = {
                    'message': 'Invalid email or password, Please try again'
                }
                return make_response(jsonify(response)), 401

        except Exception as e:
            # Create a response containing an string error message
            response = {
                'message': str(e)
            }
            # Return a server error using the HTTP Error Code 500 (Internal Server Error)
            return make_response(jsonify(response)), 500

    def put(self):
        # Update the user password for login user
        # with the details provided.
        auth_header = request.headers.get('Authorization')
        access_token = auth_header.split(" ")[0]

        if access_token:
            user_id = User.decode_token(access_token)
            user=User.query.filter_by(id=user_id).first()
            if user : 
                password = request.form.get('password')
                confirm_password = request.form.get('confirm_password')
                if password and len(password) >= 5 :
                    if password == confirm_password:
                        user.password=password 
                        user.save()
                        return jsonify({'msg': 'Password changed successfully'})
                    else :
                        return jsonify({'msg': 'Both password did not matched '}) 
                else :
                     return jsonify({'msg': 'Minimum length of password should be 5'})      
            else :
                return jsonify({'message': 'Please login to reset password.'})
        else :
            return jsonify({'msg': "unauthorized access" })             
 
 
User_view =  UserView.as_view('user_view')
Login_view =  LoginView.as_view('login_view')

app.add_url_rule(
    '/registration/', view_func=User_view, methods=['POST']
)
app.add_url_rule(
    '/users/', view_func=User_view, methods=['GET']
)
app.add_url_rule(
    '/user/<int:id>', view_func=User_view, methods=['GET']
)
app.add_url_rule(
    '/deleteuser/<int:id>', view_func=User_view, methods=['DELETE']
)
app.add_url_rule(
    '/login', view_func=Login_view, methods=['POST']
    )
app.add_url_rule(
    '/changePassword', view_func=Login_view, methods=['PUT']
    )