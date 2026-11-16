from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory
from flask_login import LoginManager, login_required
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect
from models import User, Playlist, Songs, PlaylistSongs, Downloads, db
from form import LoginForm, RegistrationForm
from flask_login import login_user, logout_user
# import dotenv
# import os





app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'secretkey'
csrf = CSRFProtect(app)


login_manager = LoginManager()
migrate = Migrate(app, db)


db.init_app(app)
login_manager.login_view = "signin"

login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


@app.route("/")
@login_required
def home():
    return render_template("home.html")

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


@app.route("/register", methods=["POST", "GET"])
def register():
    form = RegistrationForm()
    
    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        password = form.password.data
        confirm_password = form.confirm_password.data

        if password == confirm_password:
            if User.query.filter_by(email=email).first():
                return "Email already registered"
            else:
                user = User(username=name, email=email, password=confirm_password)
                user.set_password(password)
                db.session.add(user)
                db.session.commit()
                login_user(user)
        else:
            return "Password not the same"

    return render_template("register.html", form=form)


@app.route("/login", methods=["POST", "GET"])
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
            
            
        print("Error it didnt work")
        return "Invalid credentials"

    return render_template("login.html", form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug=True)

    




