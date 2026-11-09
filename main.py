from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey
from flask_migrate import Migrate
from sqlalchemy.orm import DeclarativeBase, Mapped , mapped_column, relationship
from datetime import datetime
from service import search_song
from typing import List
import enum
import requests
import dotenv
import os




app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False



class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)
migrate = Migrate(app, db)

db.init_app(app)




class Downloadstatus(enum.Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    FAILED = "failed"

class User(db.Model):
    __tablename__ = "user_table"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column()
    password: Mapped[str] = mapped_column()
    date_added = db.Column(db.DateTime, default=datetime.utcnow)
    playlists: Mapped[List["Playlist"]] = relationship(back_populates="user")
    downloads: Mapped[List["Downloads"]] = relationship(back_populates="user")
    listening_history: Mapped[List["ListeningHistory"]] = relationship(back_populates="user")


class Songs(db.Model):
    __tablename__ = "songs_table"

    id: Mapped[int] = mapped_column(primary_key=True)
    video_id: Mapped[str] = mapped_column()
    title: Mapped[str] = mapped_column()
    artist: Mapped[str] = mapped_column()
    genre: Mapped[str] = mapped_column()
    album: Mapped[str] = mapped_column()
    thumbnail: Mapped[str] = mapped_column()
    duration: Mapped[int] = mapped_column()
    playlists: Mapped[List["PlaylistSongs"]] = relationship(back_populates="song")
    


class Playlist(db.Model):
    __tablename__ = "playlist_table"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column()
    description: Mapped[str] = mapped_column()
    date_created: Mapped[datetime] = mapped_column(db.DateTime, default=datetime.utcnow)
    user_id: Mapped[int] = mapped_column(ForeignKey("user_table.id"), nullable=False)
    user: Mapped["User"] = relationship(back_populates="playlists")
    songs: Mapped[List["PlaylistSongs"]] = relationship(back_populates="playlist")
    

class PlaylistSongs(db.Model):
    __tablename__ = "playlist_songs_table"

    id: Mapped[int] = mapped_column(primary_key=True)
    position: Mapped[int] = mapped_column(nullable=False)
    playlist_id: Mapped[int] = mapped_column(ForeignKey("playlist_table.id"), nullable=False)
    song_id: Mapped[int] = mapped_column(ForeignKey("songs_table.id"), nullable=False)
    playlist: Mapped["Playlist"] = relationship(back_populates="songs")
    song: Mapped["Songs"] = relationship(back_populates="playlists")
    

class Downloads(db.Model):
    __tablename__ = "downloads_table"
    id: Mapped[int] = mapped_column(primary_key=True)
    song_id = db.relationship("Songs", backref="playlist_songs")
    status = db.Column(
        db.Enum(Downloadstatus),
        default=Downloadstatus.PENDING, 
        nullable=False
    )
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user: Mapped["User"] = relationship(back_populates="playlists")

class ListeningHistory(db.Model):
    __tablename__ = "listening_history_table"
    id: Mapped[int] = mapped_column(primary_key=True)
    song_id = db.relationship("Songs", backref="playlist_songs")
    played_at = db.Column(db.DateTime, default=datetime.utcnow)
    user: Mapped["User"] = relationship(back_populates="playlists")



@app.route(f"/api/search/<request>", methods=["GET"])
def search(request):
    # query = request.form["query"]

    results = search_song(request)
    return render_template("home.html", results=results)

@app.route("/api/playlist", methods=["POST"])
def get_all_playlist(request):
    playlist = Playlist.query.all()

    return render_template("home.html", results=results)

@app.route(f"/api/playlist/<request>", methods=["POST"])
def get_playlist(request):
    playlist = Playlist.query.filter_by(id=request).first_or_404()


    return render_template("view.html", password=playlist)


@app.route("/api/create/playlist", methods=["POST"])
def create_playlist():
    name = request.form["name"]
    description = request.form["description"]

    playlist = Playlist(name=name, description=description)
    db.session.add(playlist)
    db.session.commit()
    return render_template("home.html", results=results)

@app.route("/api/delete/playlist", methods=["POST"])
def get_all_playlist(request):
    playlist = Playlist.query.filter_by(id=response, user_id=session.get("user_id")).first_or_404()
    db.session.delete(data)
    db.session.commit()
    return redirect(url_for("home"))

   
    

if __name__ == "__main__":
    app.run(debug=True)

    




