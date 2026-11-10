from sqlalchemy import ForeignKey
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from flask_login import UserMixin
from typing import List
import enum


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)


class Downloadstatus(enum.Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    FAILED = "failed"


class User(UserMixin, db.Model):
    __tablename__ = "user_table"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(unique=True, nullable=False)
    email: Mapped[str] = mapped_column(unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)

    date_added = db.Column(db.DateTime, default=datetime.utcnow)

    playlists: Mapped[List["Playlist"]] = relationship(back_populates="user")
    downloads: Mapped[List["Downloads"]] = relationship(back_populates="user")
    listening_history: Mapped[List["ListeningHistory"]] = relationship(back_populates="user")

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)


class Songs(db.Model):
    __tablename__ = "songs_table"

    id: Mapped[int] = mapped_column(primary_key=True)
    video_id: Mapped[str] = mapped_column(unique=True, nullable=False)
    title: Mapped[str] = mapped_column(nullable=False)
    artist: Mapped[str] = mapped_column(nullable=False)
    genre: Mapped[str] = mapped_column()
    album: Mapped[str] = mapped_column()
    thumbnail: Mapped[str] = mapped_column()
    duration: Mapped[int] = mapped_column()

    playlists: Mapped[List["PlaylistSongs"]] = relationship(back_populates="song")

    listening_history: Mapped[List["ListeningHistory"]] = relationship(back_populates="song")

    downloads: Mapped[List["Downloads"]] = relationship(back_populates="song")


class Playlist(db.Model):
    __tablename__ = "playlist_table"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column()

    date_created: Mapped[datetime] = mapped_column(db.DateTime, default=datetime.utcnow)

    user_id: Mapped[int] = mapped_column(ForeignKey("user_table.id"),nullable=False)

    user: Mapped["User"] = relationship(back_populates="playlists")

    songs: Mapped[List["PlaylistSongs"]] = relationship(back_populates="playlist")


class PlaylistSongs(db.Model):
    __tablename__ = "playlist_songs_table"

    id: Mapped[int] = mapped_column(primary_key=True)

    position: Mapped[int] = mapped_column(nullable=False)

    playlist_id: Mapped[int] = mapped_column(ForeignKey("playlist_table.id"), nullable=False)

    song_id: Mapped[int] = mapped_column(ForeignKey("songs_table.id"),nullable=False)

    playlist: Mapped["Playlist"] = relationship(back_populates="songs" )

    song: Mapped["Songs"] = relationship(back_populates="playlists")


class Downloads(db.Model):
    __tablename__ = "downloads_table"

    id: Mapped[int] = mapped_column(primary_key=True)

    song_id: Mapped[int] = mapped_column(ForeignKey("songs_table.id"), nullable=False)

    user_id: Mapped[int] = mapped_column(ForeignKey("user_table.id"),nullable=False)

    status: Mapped[Downloadstatus] = mapped_column(db.Enum(Downloadstatus), default=Downloadstatus.PENDING, nullable=False)

    created_at: Mapped[datetime] = mapped_column(db.DateTime, default=datetime.utcnow)

    song: Mapped["Songs"] = relationship( back_populates="downloads")

    user: Mapped["User"] = relationship(back_populates="downloads")


class ListeningHistory(db.Model):
    __tablename__ = "listening_history_table"

    id: Mapped[int] = mapped_column(primary_key=True)

    song_id: Mapped[int] = mapped_column(ForeignKey("songs_table.id"),nullable=False)

    user_id: Mapped[int] = mapped_column(ForeignKey("user_table.id"), nullable=False)

    played_at: Mapped[datetime] = mapped_column(db.DateTime,default=datetime.utcnow)

    user: Mapped["User"] = relationship( back_populates="listening_history")

    song: Mapped["Songs"] = relationship(
        back_populates="listening_history"
    ) 