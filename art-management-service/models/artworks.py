from flask_sqlalchemy import SQLAlchemy
from __main__ import db


class Artworks(db.Model):
    __tablename__ = 'artworks'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Float)
    category = db.Column(db.String(255))
    image_url = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())