""" models.py by Sebastiaan van der Laan
    for RoboTurtle, final project
    as part of WebApps, Minor Programmeren.

    Contains ORM models for in the SQL database.
"""
    
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Table, Integer, ForeignKey, String, Column
from sqlalchemy.orm import relationship

db = SQLAlchemy()

# (public) playlists
class Playlist(db.Model):
    __tablename__ = 'playlists'
    id = Column(Integer, primary_key=True)
    uri = Column(String, nullable=False, unique=True)
    description = Column(String, nullable=False)

    # link playlists to the user who requested their creation
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    username = relationship("User", back_populates="playlists")

    def __str__(self):
        return self.description

# users (who made a public playlist)
class User(db.Model):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False, unique=True)

    # collect all playlists this user requested to be made
    playlists = relationship("Playlist", back_populates="username")

    def __str__(self):
        return self.username
