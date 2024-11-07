from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class Account(db.Model, UserMixin):
    __tablename__ = "Account"
    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(150), unique= True)
    password = db.Column(db.String(150))
    notes = db.relationship('Note')

class Note(db.Model):
    __tablename__ = "Note"
    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey('account.id'))
    data = db.Column(db.String(1000))
    notes = db.relationship('Account')