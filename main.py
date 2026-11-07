from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped , mapped_column
from datetime import datetime
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

db.init_app(app)




class Downloadstatus(enum.Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    FAILED = "failed"


class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column()
    password: Mapped[str] = mapped_column()
    date_added = db.Column(db.DateTime, default=datetime.utcnow)


class Songs(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    video_id: Mapped[str] = mapped_column()
    title: Mapped[str] = mapped_column()
    artist: Mapped[str] = mapped_column()
    album: Mapped[str] = mapped_column()
    thumbnail: Mapped[str] = mapped_column()
    duration: Mapped[int] = mapped_column()

class Playlist(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column()
    description: Mapped[str] = mapped_column()
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    passwords = db.relationship('Password', backref='owner', lazy=True)

class PlaylistSongs(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    playlist_id = db.relationship("Playlist", backref="playlist_songs")
    song_id = db.relationship("Songs", backref="playlist_songs")
    position: Mapped[int] = mapped_column()

class Downloads(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    song_id = db.relationship("Songs", backref="playlist_songs")
    status = db.Column(
        db.Enum(Downloadstatus),
        default=Downloadstatus.PENDING, 
        nullable=False
    )
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class ListeningHistory(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    song_id = db.relationship("Songs", backref="playlist_songs")
    played_at = db.Column(db.DateTime, default=datetime.utcnow)



if __name__ == "__main__":
    app.run(debug=True)

    




