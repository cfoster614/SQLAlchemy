from flask import Flask, request, redirect, render_template, flash
from models import db, connect_db, User

app = Flask(__name__)


app.config['SECRET_KEY'] = "scamp"
app.app_context().push() #<-------- WHY WAS THIS SO DIFFICULT TO FIGURE OUT!!!!!!!!!!!

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///users'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)



@app.route("/")
def home():
    
    return redirect("/users")


@app.route("/users")
def user_list():
    """List pets and show add form."""
    users = User.query.all()
    
    return render_template("users.html", users=users)


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
        return render_template("new-user.html")
        
        
@app.route("/users/<int:user_id>", methods=['GET', 'POST'])
def user_info(user_id):
    """Show details about user"""
    
    user = User.query.get_or_404(user_id)

    if request.method == 'POST':
        changed_first_name = request.form.get('first-name')
        changed_last_name = request.form.get('last-name')
        changed_image = request.form.get('image')

        if changed_first_name:
            user.first_name = changed_first_name
        if changed_last_name:
            user.last_name = changed_last_name 
        if changed_image:
            user.image_url = changed_image
            
        db.session.commit()
        return render_template("user-details.html", user=user)
    
    else:
        return render_template("user-details.html", user=user)

    
@app.route("/users/<int:user_id>/edit", methods=['GET', 'POST']) 
def edit_user(user_id):
 
    user = User.query.get_or_404(user_id)
    return render_template("edit-user.html", user=user)  

@app.route("/users/<int:user_id>/delete")
def delete_user(user_id):
    """Delete a user"""
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    
    return redirect("/users")
    