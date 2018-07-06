from my_app import db

 
class Borrow(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'),
        nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'),
        nullable=False)
    returned=db.Column(db.Boolean)
 
    def __init__(self,user_id,book_id):
        self.returned = False
        self.user_id = user_id
        self.book_id=book_id

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
 
    def __repr__(self):
        return '<user_id %d>' % self.user_id