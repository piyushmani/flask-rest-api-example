from my_app import db
from sqlalchemy.orm import relationship
import jwt
import datetime
from datetime import timedelta
 
SECRET_KEY="piyush_raj"

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    username = db.Column(db.String(10))
    password = db.Column(db.String(10))
    isAdmint = db.Column(db.Boolean)
    borrows = relationship("Borrow", backref="user")
 
    def __init__(self, name, username,password):
        self.name = name
        self.username = username
        self.password= password

    def save(self):
        """Save a student to the database.
        This includes creating a new user and editing one.
        """
        db.session.add(self)
        db.session.commit() 

    def delete(self):
        """Delete a user from the database.
        """
        db.session.delete(self)
        db.session.commit()    

    def generate_token(self, user_id):
        """ Generates the access token"""

        try:
            # set up a payload with an expiration time
            payload = {
                'exp': datetime.datetime.now() + timedelta(minutes=10),
                'iat': datetime.datetime.now(),
                'sub': user_id
            }
            # create the byte string token using the payload and the SECRET key
            jwt_string = jwt.encode(
                payload,
                SECRET_KEY,
                algorithm='HS256'
            )
            return jwt_string

        except Exception as e:
            # return an error in string format if an exception occurs
            return str(e)

    @staticmethod
    def decode_token(token):
        """Decodes the access token from the Authorization header."""
        try:
            # try to decode the token using our SECRET variable
            payload = jwt.decode(token, SECRET_KEY)
            return payload['sub']
        except jwt.ExpiredSignatureError:
            # the token is expired, return an error string
            return "Expired token. Please login to get a new token"
        except jwt.InvalidTokenError:
            # the token is invalid, return an error string
            return "Invalid token. Please register or login" 
    
    @staticmethod
    def isAdmin(request):
        auth_header = request.headers.get('Authorization')
        access_token = auth_header.split(" ")[0]

        if access_token:
         # Attempt to decode the token and get the User ID
            user_id = User.decode_token(access_token)
            user=User.query.filter_by(id=user_id).first()
            if user.isAdmint == True :
                return True    
                     
 
    def __repr__(self):
        return '<username %s>' % self.username