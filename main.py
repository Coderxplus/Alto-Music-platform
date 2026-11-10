from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory
from flask_login import LoginManager, login_required
from flask_migrate import Migrate
from models import User, Playlist, Songs, PlaylistSongs, Downloads, db
from form import LoginForm, RegistrationForm
from flask_login import login_user, logout_user
# import dotenv
# import os




app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'secretkey'


login_manager = LoginManager()
migrate = Migrate(app, db)


db.init_app(app)
login_manager.login_view = "signin"

login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)


# @app.route(f"/search/<request>", methods=["GET"])
# @login_required
# def search(request):
#     # query = request.form["query"]

#     results = search_song(request)
#     return render_template("home.html", results=results)

# @app.route("/playlist", methods=["POST"])
# @login_required
# def get_all_playlist(request):
#     playlist = Playlist.query.all()

#     return render_template("home.html", results=results)

# @app.route(f"/playlist/<request>", methods=["POST"]).
# @login_required
# def get_playlist(request):
#     playlist = Playlist.query.filter_by(id=request).first_or_404()


#     return render_template("view.html", password=playlist)

# @app.route("/create/playlist", methods=["POST"])
# @login_required
# def create_playlist():
#     name = request.form["name"]
#     description = request.form["description"]

#     playlist = Playlist(name=name, description=description)
#     db.session.add(playlist)
#     db.session.commit()
#     return render_template("home.html", results=results)

# @app.route("/delete/playlist", methods=["POST"])
# @login_required
# def get_all_playlist(request):
#     playlist = Playlist.query.filter_by(id=response, user_id=session.get("user_id")).first_or_404()
#     db.session.delete(data)
#     db.session.commit()
#     return redirect(url_for("home"))


# @app.route("/register", methods=["POST"])
# def register():
#     name = request.form.get("username")
#     email = request.form.get("email")
#     password = request.form.get("password")

#     if User.query.filter_by(email=email).first():
#         return "Email already registered"
#     else:
#         user = User(name=name, email=email)
#         user.set_password(password)
#         db.session.add(user)
#         db.session.commit()
#         login_user(user)

#     return redirect(url_for("home"))


@app.route("/login", methods=["POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        remember_me = form.remember_me.data

        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            login_user(user, remember=remember_me)
            return redirect(url_for("home"))
    else:
        return "Invalid credentials"
    return render_template("login.html", form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug=True)

    




