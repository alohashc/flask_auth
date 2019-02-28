from flask_bcrypt import Bcrypt
from flask import Flask
import config
from flask_sqlalchemy import SQLAlchemy


DB_URL_POSTGRES = config.POSTGREDB['PATTERN'].format(**config.POSTGREDB)
DB_URL = config.SQLITEDB


app = Flask(__name__)
bcrypt = Bcrypt(app)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = DB_URL
db = SQLAlchemy(app)
