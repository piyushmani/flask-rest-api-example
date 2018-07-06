from flask import Flask
from flask_sqlalchemy import SQLAlchemy
 
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@localhost/flaskdb'
db = SQLAlchemy(app)
 
from my_app.user.views import user_blueprint
from my_app.book.views import book_blueprint
from my_app.borrow.views import borrow_blueprint

app.register_blueprint(user_blueprint)
app.register_blueprint(book_blueprint)
app.register_blueprint(borrow_blueprint)

db.create_all()