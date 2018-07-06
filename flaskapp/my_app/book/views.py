import json
from flask import request, jsonify, Blueprint, abort
from flask.views import MethodView
from flask import make_response
from my_app import db, app
from my_app.book.models import Book
from my_app.user.models import User
from my_app.borrow.models import Borrow
 
book_blueprint = Blueprint('book', __name__)
 


@book_blueprint.route('/books')
def books():
    auth_header = request.headers.get('Authorization')
    access_token = auth_header.split(" ")[0]

    if access_token:
     # Attempt to decode the token and get the User ID
        user_id = User.decode_token(access_token)
        if user_id :
            books=Book.query.all()
            response={}
            for book in books :
                book_borrowed=Book.query.join(Borrow).filter( Borrow.returned == False ).filter(Book.id== book.id)
                sqlquery=str(book_borrowed)%str(book.id)
                results= db.engine.execute(sqlquery).fetchall()
                avail_book_count= book.quantity-len(results)
                response[book.id] = {
                                'name': book.name,
                                'discription': book.discription,
                                'quantity' : book.quantity,
                                'available':avail_book_count                  
                                    }
            return jsonify(response)
        else :
            res={'msg':"no books found"}                
            return jsonify(res)

@book_blueprint.route('/mybooks')
def mybooks():
    auth_header = request.headers.get('Authorization')
    access_token = auth_header.split(" ")[0]

    if access_token:
     # Attempt to decode the token and get the User ID
        user_id = User.decode_token(access_token)
        if user_id :
            response={}
            book_borrowed=Book.query.join(Borrow).join(User).filter( Borrow.returned ==
                            False ).filter(User.id== user_id)
            sqlquery=str(book_borrowed)%str(user_id)
            results= db.engine.execute(sqlquery).fetchall()
            for book in results: 
                response[book[0]] = {
                            'name': book[1],
                            'discription': book[2],                 
                                }
            return jsonify(response)
        else :
            res={'msg':"no books found"}                
            return jsonify(res)            

class BookOperationView(MethodView):
 
    def post(self):
        if User.isAdmin(request) :
            name = request.form.get('name')
            discription = request.form.get('discription')
            book = Book(name, discription)
            book.save()
            return jsonify({book.id: {

                'name': book.name,
                'discription': book.discription,
            }})

        else :
            response = {
                 'message': 'you are not allowed for book modification.'
             }

            return jsonify(response)
                 
 
    def put(self, id):
        # Udate the book record for the provided id.
        if User.isAdmin(request) :
            name = request.form.get('name')
            discription = request.form.get('discription')
            quantity = request.form.get('quantity')
            book = Book.query.filter_by(id=id).first()
            if discription :
                book.discription= discription
            if name :
                book.name= name
            if quantity :    
                book.quantity = quantity
            book.save()
            return jsonify({book.id: {

                'name': book.name,
                'discription': book.discription,
            }})

        else :
            response = {
                 'message': 'you are not allowed for book modification.'
             }

            return jsonify(response)
 
    def delete(self, id):
        # Delete the record for the provided id.
        if User.isAdmin(request) :
            book = Book.query.filter_by(id=id).first()
            book.delete()
            return jsonify({'msg': 'deleted'})

        else :
            response = {
                 'message': 'you are not allowed for book modification.'
             }

            return jsonify(response)

BookOperation_view =  BookOperationView.as_view('book_opration')

app.add_url_rule(
    '/add_book', view_func=BookOperation_view, methods=['POST']
)
app.add_url_rule(
    '/update_book/<int:id>', view_func=BookOperation_view, methods=['PUT']
)                    
app.add_url_rule(
    '/delete_book/<int:id>', view_func=BookOperation_view, methods=['DELETE']
)

 