from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)
    
class User(db.Model):
    """User."""
    
    __tablename__ = 'users'
    
    def __repr__(self):
        user = self
        return f"<User id = {user.id} Name = {user.first_name} {user.last_name} Profile pic url = {user.image_url}"
    id = db.Column(db.Integer,
                   primary_key = True,
                   autoincrement = True)
    first_name = db.Column(db.String(50),
                           nullable=False)
    last_name = db.Column(db.String(50),
                          nullable=False)
    
    image_url = db.Column(db.String)
                        
    