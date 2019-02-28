from models.base import db, bcrypt
from config import os


class UserCred(db.Model):
    __tablename__ = 'cred'
    user_id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(20), unique=True)
    pw_hash = db.Column(db.String(180), unique=True)
    info = db.relationship('UserInfo', uselist=False, back_populates="cred") # NOT USE

    def __init__(self, login, password):
        self.login = login
        self.pw_hash = bcrypt.generate_password_hash(password).decode('utf8')

    def create_auth_token(self):
        try:
            return os.urandom(24).hex()
        except Exception as e:
            return e


class UserInfo(db.Model):
    __tablename__ = 'info'
    info_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    surname = db.Column(db.String(20))
    age = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('cred.user_id')) # NOT USE
    cred = db.relationship('UserCred', uselist=False, back_populates="info") # NOT USE

    def __init__(self, id, name=None, surname=None, age=None):
        self.name = name
        self.surname = surname
        self.age = age
        self.user_id = id

    def update_fields(self, fields):
        keys = ['name', 'surname', 'age']
        for key in keys:
            if fields.get(key) is not None:
                setattr(self, key, fields[key])

class TokenList(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String(500), unique=True)
    user_id = db.Column(db.Integer, unique=True)

    def __init__(self, token, id):
        self.token = token
        self.user_id = id

db.create_all()