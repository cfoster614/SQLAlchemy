from flask import Flask, request, redirect, render_template, flash, url_for
from models import db, connect_db, User, Posts, Tag, PostTag
import logging
from sqlalchemy import and_
logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

app = Flask(__name__)


app.config['SECRET_KEY'] = "scamp"
app.app_context().push() #<-------- WHY WAS THIS SO DIFFICULT TO FIGURE OUT!!!!!!!!!!!

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///users'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)



@app.route("/")
def home():
    posts = Posts.query.all()
    return render_template('homepage.html', posts = posts)


@app.route("/users")
def user_list():
    """List pets and show add form."""
    users = User.query.all()
    
    return render_template("Users/users.html", users=users)


@app.route("/users/new", methods=['GET', 'POST'])
def add_user():
    if request.method =='POST':
        first_name = request.form.get('first-name')
        last_name = request.form.get('last-name')
        image = request.form.get('image')

        if not first_name and not last_name:
            flash('Missing first and last name')
            return redirect('/users/new')
        elif not first_name or not last_name:
            if not first_name:
                flash('Missing first name')
            if not last_name:
                flash('Missing last name')
            return redirect('/users/new')
        else:
            if not image:
                new_user = User(first_name=first_name, last_name=last_name, image_url = "https://cdn.vectorstock.com/i/1000x1000/73/07/profile-portrait-a-white-cat-vector-28437307.webp")
                db.session.add(new_user)
                db.session.commit()
            else:
                new_user = User(first_name=first_name, last_name=last_name, image_url=image)
                db.session.add(new_user)
                db.session.commit()

            return redirect("/users")
    
    else:
        return render_template("Users/new-user.html")
        
        
@app.route("/users/<int:user_id>")
def user_info(user_id):
    """Show details about user"""
    
    user = User.query.get(user_id)
    posts = Posts.query.filter(Posts.user_id == user_id).all()
    return render_template("Users/user-details.html", user = user, posts = posts)

    
@app.route("/users/<int:user_id>/edit", methods=['GET', 'POST']) 
def edit_user(user_id):
    user = User.query.get_or_404(user_id)
    if request.method == 'POST':
        changed_first_name = request.form.get('first-name')
        changed_last_name = request.form.get('last-name')
        changed_image = request.form.get('image')
        if changed_first_name:
            user.user.first_name = changed_first_name
        if changed_last_name:
            user.user.last_name = changed_last_name 
        if changed_image:
            user.user.image_url = changed_image
        db.session.commit()
        return redirect(url_for("user_info", user_id = user.id))
    else:
        return render_template("Users/edit-user.html", user=user)  


@app.route("/users/<int:user_id>/delete")
def delete_user(user_id):
    """Delete a user"""
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return redirect("/users")


@app.route("/users/<int:user_id>/posts/new", methods=['POST', 'GET'])
def new_post(user_id):
    tags = db.session.query(Tag).all()
    user = User.query.get(user_id)
    
    if request.method == 'POST':
        tags_used = request.form.getlist('tags-used', type=None)
        title = request.form.get('title')
        content = request.form.get('content')
        new_post = Posts(title = title, content = content, user_id = user.id)
        db.session.add(new_post)
        db.session.commit()
        
        last_post = Posts.query.order_by(Posts.id.desc()).first()
        for tag in tags_used:
            print(tag)
            post_tag = PostTag(post_id = last_post.id, tag_id = tag)
            db.session.add(post_tag)
        db.session.commit()
        return redirect(url_for("view_post", post_id = last_post.id))
    
    else:
        
        return render_template("Posts/post-form.html", tags = tags, user = user)
    

@app.route("/post/<int:post_id>")
def view_post(post_id):
    post = Posts.query.get(post_id)
    tags = (db.session.query(Tag)
            .join(PostTag, PostTag.tag_id == Tag.id)
            .join(Posts, Posts.id == PostTag.post_id)
            .filter(Posts.id == post_id)
            .all())
    
        
    return render_template("Posts/post.html", post = post, tags = tags)
    


@app.route("/post/<int:post_id>/edit", methods = ['GET', 'POST'])
def edit_post(post_id):
    post = Posts.query.get(post_id)
    tags = db.session.query(Tag).all()
   
    
    if request.method == 'POST':
        changed_title = request.form.get('title')
        changed_content = request.form.get('content')
        changed_tags = request.form.getlist('tags-used')

        if changed_title:
            post.title = changed_title
        if changed_content:
            post.content = changed_content
        if changed_tags:
            last_post = Posts.query.order_by(Posts.id.desc()).first()
        for tag in changed_tags:
            post_tag = PostTag(post_id = post_id, tag_id = tag)
            db.session.add(post_tag)
        
        db.session.commit()
        return redirect(url_for("view_post", post_id = post.id))
    else:
        return render_template('Posts/edit-post.html', post = post, tags=tags)


@app.route("/post/<int:post_id>/delete")
def delete_post(post_id):
    post = Posts.query.get(post_id)
    
    db.session.delete(post)
    db.session.commit()

    return redirect(url_for("user_info", user_id = post.user_id))


@app.route('/tags')
def show_tags():
    tags = db.session.query(Tag).all()
    
    return render_template('/Tags/tags.html', tags = tags)

@app.route('/tags/new')
def new_tag():
    return render_template('/Tags/new-tag.html')

@app.route('/tags/<int:tag_id>')
def tag_info(tag_id):
    tag = Tag.query.get(tag_id)
    posts = (db.session.query(Posts)
            .join(PostTag, PostTag.post_id == Posts.id)
            .join(Tag, Tag.id == PostTag.tag_id)
            .filter(Tag.id == tag_id)
            .all())
    
    return render_template('/Tags/tag-details.html', tag = tag, posts = posts)
    
    
@app.route('/tags/<int:tag_id>/edit', methods=['POST', 'GET'])
def edit_tag(tag_id):
    tag = Tag.query.get(tag_id)
  
    if request.method == 'POST':
        changed_name = request.form.get('tag-name')

        if changed_name:
            tag_name = changed_name
            db.session.add(tag_name)
            
        db.session.commit()
        return redirect(url_for("tag_info", tag_id = tag.id))
    
    else:
        return render_template('/Tags/edit-tag.html', tag = tag)
    