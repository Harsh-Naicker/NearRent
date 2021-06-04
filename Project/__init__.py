import os
import datetime
from flask import Flask, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager, current_user, login_required
import psycopg2
import razorpay
import json

app=Flask(__name__)

razorpay_client = razorpay.Client(auth=("", ""))

app.config['SECRET_KEY']='mysecret'

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = ''
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy(app, session_options={"autoflush": False})
Migrate(app,db)

login_manager=LoginManager()
login_manager.init_app(app)
login_manager.login_view='users.login'

from Project.core.views import core
from Project.users.views import users

app.register_blueprint(core)
app.register_blueprint(users)
