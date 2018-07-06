import json
from flask import request, jsonify, Blueprint, abort
from flask.views import MethodView
from my_app import db, app
from my_app.borrow.models import Borrow
from my_app.user.models import User
from my_app.book.models import Book
 
borrow_blueprint = Blueprint('borrow', __name__)
 
 
class BorrowView(MethodView):
 
    def get(self, id):
        auth_header = request.headers.get('Authorization')
        access_token = auth_header.split(" ")[0]
        if access_token:
            user_id = User.decode_token(access_token)
            if user_id :
                user=User.query.get(user_id)
                book_borrowed_byuser=User.query.join(Borrow).filter(Borrow.returned == False ).filter(User.id== user.id)
                books_by_user_sql=str(book_borrowed_byuser)%str(user.id)
                results= db.engine.execute(books_by_user_sql).fetchall()
                user_books=len(results)
                if user_books < 5 :
                    book=Book.query.get(id)
                    book_borrowed=book.query.join(Borrow).filter(Borrow.returned == False ).filter(Book.id== book.id)
                    sqlquery=str(book_borrowed)%str(book.id)
                    results= db.engine.execute(sqlquery).fetchall()
                    avail_book_count= book.quantity-len(results)
                    if avail_book_count > 0 :
                        already_borrowed_sqlquery=str(Borrow.query.join(User).join(Book).filter(Book.id == id ).filter(User.id== 
                             user.id).filter(Borrow.returned==False))%(id , user.id )
                        rslt=db.engine.execute(already_borrowed_sqlquery).fetchall()
                        if len(rslt) > 0 :
                            return jsonify({"msg":'You have already borrowd this book'})
                        else :    
                            brr= Borrow(user.id, book.id)
                            brr.save()
                            return jsonify({"msg":'You have borrowed the book : {}'.format(book.discription)})
                    else :
                        return jsonify({"msg":'book is not available currently '})
                else :
                     return jsonify({"msg":'You are already subscried to maximum 5 books '})           



            else :
                 return jsonify({"msg":'You are not authorized'})       
 
    def delete(self, id):
        # Delete the record for the provided id.
        auth_header = request.headers.get('Authorization')
        access_token = auth_header.split(" ")[0]
        if access_token:
            user_id = User.decode_token(access_token)
            if user_id :
                user=User.query.get(user_id)
                borrowed_book=Borrow.query.join(User).join(Book).filter(Book.id == id ).filter(User.id== 
                             user.id).filter(Borrow.returned==False)
                borrowed_book_sqlquery=str(borrowed_book)%(id , user.id )
                reslt=db.engine.execute(borrowed_book_sqlquery).fetchall()
                if len(reslt) > 0 :
                    borrow_id= reslt[0][0]
                    borrow_obj=Borrow.query.get(borrow_id)
                    borrow_obj.returned = True
                    borrow_obj.save()
                    return jsonify({'msg': 'Yoy have sucessfully returned Book.'})
                else :
                    return jsonify({'msg': 'Yoy have not borrowed this Book.'})        
 
 
Borrow_view =  BorrowView.as_view('Borrow_view')
app.add_url_rule(
    '/borrow/<int:id>', view_func=Borrow_view, methods=['GET']
)
app.add_url_rule(
    '/return/<int:id>', view_func=Borrow_view, methods=['DELETE']
)