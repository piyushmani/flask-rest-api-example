from my_app import db
from sqlalchemy.orm import relationship
 
class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    discription= db.Column(db.String(200))
    quantity=db.Column(db.Integer)

    borrows = relationship("Borrow", backref="book")
 
    def __init__(self, name, discription):
        self.name = name
        self.discription = discription
        self.quantity= 5

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
        return '<discription %s>' % self.discription


