from flask_login import UserMixin
from sqlalchemy.sql import func
from flashapp.database.database import db


class Deck(db.Model):
    deck_id = db.Column(db.Integer, primary_key=True)
    deck_name = db.Column(db.String(100), nullable=False)
    cards = db.relationship('Card')
    review_dt = db.Column(db.DateTime(timezone=True))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    crt_dt = db.Column(db.DateTime(timezone=True), default=func.now())
    updt_dt = db.Column(db.DateTime(timezone=True), default=func.now())


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    decks = db.relationship('Deck')
    crt_dt = db.Column(db.DateTime(timezone=True), default=func.now())
    updt_dt = db.Column(db.DateTime(timezone=True), default=func.now())


class Card(db.Model):
    card_id = db.Column(db.Integer, primary_key=True)
    deck_id = db.Column(db.Integer, db.ForeignKey('deck.deck_id'))
    card_ques = db.Column(db.String(1500), nullable=False)
    card_ans = db.Column(db.String(1500), nullable=False)
    diff_level = db.Column(db.String(10), nullable=False)
    score = db.Column(db.Integer, default=0)
    crt_dt = db.Column(db.DateTime(timezone=True), default=func.now())
    updt_dt = db.Column(db.DateTime(timezone=True), default=func.now())
