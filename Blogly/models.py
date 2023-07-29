from flask_sqlalchemy import SQLAlchemy
import datetime

db = SQLAlchemy()
default_image = "https://cdn.vectorstock.com/i/1000x1000/73/07/profile-portrait-a-white-cat-vector-28437307.webp"


def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)
    
class User(db.Model):
    """User."""
    
    __tablename__ = 'users'
    
    def __repr__(self):
        user = self
        return f"<User ID: {user.id} | First Name: {user.first_name} | Last Name:{user.last_name}"
    id = db.Column(db.Integer,
                   primary_key = True,
                   autoincrement = True)
    first_name = db.Column(db.String(50),
                           nullable=False)
    last_name = db.Column(db.String(50),
                          nullable=False)
    
    image_url = db.Column(db.Text, nullable=False, default = default_image)
                        

class Posts(db.Model):
    """Posts"""

    __tablename__ = 'posts'

    def __repr__(self):
        post = self
        return f"< User ID: {post.user_id} | {post.title} | {post.content}>"
    id = db.Column(db.Integer,
                   primary_key = True,
                   autoincrement = True)
    title = db.Column(db.String(50),
                      nullable = False)
    content = db.Column(db.String(200),
                        nullable = False)
    created_at = db.Column(db.DateTime, 
                           default = datetime.datetime.now)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    user = db.relationship('User', backref = 'posts')
    
    @property
    def friendly_date(self):
        """Return nicely-formatted date."""

        return self.created_at.strftime("%a %b %-d %Y, %-I:%M %p")
    

class Tag(db.Model):
    
    __tablename__ = 'tags'
    
    def __repr__(self):
        tag = self
        return f"<{tag.id} | {tag.name}>"
    id = db.Column(db.Integer,
                   primary_key = True,
                   autoincrement = True)
    name = db.Column(db.String(50),
                          nullable = False)
    posts = db.relationship('Posts', 
                            secondary='post_tags',
                            backref = 'tags')
    

class PostTag(db.Model):
    
    __tablename__ = 'post_tags'

    def __repr__(self):
        tags = self
        return f"<Post_id: {tags.post_id} | Tag_id: {tags.tag_id}>" 
    
    __table_args__ = (db.PrimaryKeyConstraint('post_id', 'tag_id')),
    
    post_id = db.Column(db.Integer,
                        db.ForeignKey('posts.id'),
                        primary_key = True)
    tag_id = db.Column(db.Integer,
                       db.ForeignKey('tags.id'),
                       primary_key = True)
    
   
    
    
    