from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect

app = Flask(__name__)
app.config.from_object('config')
CSRFProtect(app)
db = SQLAlchemy(app)
login = LoginManager(app)

from app import views,models