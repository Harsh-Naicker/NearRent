from flask import Flask, flash, render_template, request, Blueprint, redirect, url_for
from flask_login import login_user, current_user, logout_user, login_required
import time
import requests
import lxml.html as lh
import pandas as pd
import re
from datetime import date
from Project.core.forms import LoginForm, RegistrationForm
from Project.models import User
from Project import db

users=Blueprint('users',__name__)

@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("core.index"))

@users.route('/login', methods=['GET','POST'])
def login():
    form1=LoginForm()
    if form1.submit1.data and form1.validate():
        next=url_for('core.index')
        user=User.query.filter_by(email=form1.email.data).first()
        if user is not None and user.check_password(form1.password.data):
            login_user(user)
            next=request.args.get('next')

            if next==None or not next[0] == '/':
                next=url_for('core.index')
        else:
            flash('Wrong login credentials')
        return redirect(next)
    return render_template("login.html",form=form1)

@users.route('/signup', methods=['GET','POST'])
def signup():
    form2=RegistrationForm()

    if form2.submit2.data and form2.validate():
        if User.query.filter_by(email=form2.email.data).first() == None:
            user=User(fname=form2.fname.data , lname=form2.lname.data, email=form2.email.data, password=form2.password.data, phone=form2.phone.data, address=form2.address.data)
            db.session.add(user)
            db.session.commit()
        else:
            flash('An account with this email already exists')
        return redirect(url_for('core.index'))
    
    return render_template("signup.html", form=form2)
