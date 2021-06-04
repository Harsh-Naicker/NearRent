from flask import Flask, Response, flash, render_template, request, Blueprint, redirect, url_for
from flask_login import login_user, current_user, logout_user, login_required
import time
import requests
import lxml.html as lh
import pandas as pd
import re
from datetime import date
from datetime import datetime
import sqlite3 as sql
from sqlite3 import Error
from Project import db
from werkzeug.utils import secure_filename
import numpy
from PIL import Image as im
from base64 import b64encode
from sqlalchemy.sql import exists
import random


from Project.core.forms import LoginForm, RegistrationForm, UploadForm
from Project.models import User, Items, RentedItems
from Project import razorpay_client

core=Blueprint('core',__name__)

price=0
product_id=0
sdate=0
edate=0

@core.route('/', methods=['GET','POST'])
def index():
    return render_template("home.html")

# @core.route('/login', methods=['GET','POST'])
# def login():
#     form1=LoginForm()
#     if form1.submit1.data and form1.validate():
#         next=url_for('core.index')
#         user=User.query.filter_by(email=form1.email.data).first()
#         if user is not None and user.check_password(form1.password.data):
#             login_user(user)
#             next=request.args.get('next')

#             if next==None or not next[0] == '/':
#                 next=url_for('core.index')
#         else:
#             flash('Wrong login credentials')
#         return redirect(next)
#     return render_template("login.html",form=form1)

# @core.route('/signup', methods=['GET','POST'])
# def signup():
#     form2=RegistrationForm()

#     if form2.submit2.data and form2.validate():
#         if User.query.filter_by(email=form2.email.data).first() == None:
#             user=User(fname=form2.fname.data , lname=form2.lname.data, email=form2.email.data, password=form2.password.data, phone=form2.phone.data, address=form2.address.data)
#             db.session.add(user)
#             db.session.commit()
#         else:
#             flash('An account with this email already exists')
#         return redirect(url_for('core.index'))
    
#     return render_template("signup.html", form=form2)

@core.route('/uploadform', methods=['GET','POST'])
@login_required
def uploadForm():
    return render_template("upload.html")

@core.route('/upload', methods=['POST'])
def upload():
    nm=request.form['item']
    # nm='Computer Chair'
    file1=request.files['file1']
    file2=request.files['file2']
    file3=request.files['file3']
    pr=request.form['price']
    cat=request.form['dropdown']

    item=Items(item_name=nm, image1=file1.read(), image2=file2.read(), image3=file3.read(), price=pr, category=cat,supplier_id=current_user.id)
    db.session.add(item)
    db.session.commit()
    
    return redirect(url_for('core.index'))

@core.route('/available', methods=['GET','POST'])
@login_required
def available():
    # products=Items.query.paginate(per_page=100)
    # products = Items.query.filter(Items.supplier_id != current_user.id).paginate(per_page=100)
    products = Items.query.filter(Items.supplier_id != current_user.id).filter(~exists().where(Items.id == RentedItems.item_id)).paginate(per_page=100)
    for product in products.items:
        product.image1=b64encode(product.image1).decode("utf-8")
    length=len(products.items)
    return render_template('available.html', products=products, length=length)

@core.route('/rent', methods=['GET', 'POST'])
def rentItem():
    product_id=request.form['pid']
    # print(product_id)
    item=Items.query.filter_by(id = product_id).one()
    item.image1=b64encode(item.image1).decode("utf-8")
    item.image2=b64encode(item.image2).decode("utf-8")
    item.image3=b64encode(item.image3).decode("utf-8")

    supplier=User.query.filter_by(id=item.supplier_id).one()
    return render_template('rentitem.html', product=item, supplier=supplier)

@core.route('/checkout', methods=['GET','POST'])
def  checkout():
    global price, product_id, sdate, edate
    product_id=request.form['pid']
    supplier_id=request.form['sid']
    start_date=request.form['start']
    end_date=request.form['end']

    product=Items.query.filter_by(id = product_id).one()
    supplier=User.query.filter_by(id=product.supplier_id).one()

    
    delta=datetime.strptime(end_date, '%Y-%m-%d')-datetime.strptime(start_date, '%Y-%m-%d')
    delta=delta.days
    # print(type(end_date))

    price=int(delta*product.price*100)
    sdate=datetime.strptime(start_date, '%Y-%m-%d').date()
    edate=datetime.strptime(end_date, '%Y-%m-%d').date()
    product_id=product.id

    return render_template('checkout.html', product=product, supplier=supplier, price=price/100, days=delta, start=start_date, end=end_date, order_id=random.randint(1,100))

@core.route('/charge', methods=['POST'])
def charge():
    global price, sdate, edate, product_id
    amount = price
    # print(amount)
    payment_id = request.form['razorpay_payment_id']
    razorpay_client.payment.capture(payment_id, amount)
    # print(payment_id)
    # return json.dumps(razorpay_client.payment.fetch(payment_id))
    ritem=RentedItems(item_id=product_id, start_date=sdate, end_date=edate, tenant_id=current_user.id, amount=price/100,payment_id=payment_id)
    db.session.add(ritem)
    db.session.commit()
    return redirect(url_for('core.index'))

@core.route('/dashboard', methods=['GET','POST'])
@login_required
def dashboard():
    # items_rented = RentedItems.query.join(Items, Items.id == RentedItems.item_id).join(User, User.id == Items.supplier_id).filter(RentedItems.tenant_id == current_user.id).all()
    items_rented = db.session.query(RentedItems, Items, User).join(Items, Items.id == RentedItems.item_id).join(User, User.id == Items.supplier_id).filter(RentedItems.tenant_id == current_user.id).all()
    # items_lent=Items.query.join(RentedItems, Items.id == RentedItems.item_id).join(User, User.id == Items.supplier_id).filter(Items.supplier_id == current_user.id).paginate(per_page=100)
    items_lent = db.session.query(Items, RentedItems, User).join(RentedItems, Items.id == RentedItems.item_id).join(User, User.id == RentedItems.tenant_id).filter(Items.supplier_id == current_user.id).all()
    # ri=len(items_rented.items)
    li=len(items_lent)
    ri=len(items_rented)
    for i in items_rented:
        i.RentedItems.start_date=i.RentedItems.start_date.date()
        i.RentedItems.end_date=i.RentedItems.end_date.date()
    
    for i in items_lent:
        i.RentedItems.start_date=i.RentedItems.start_date.date()
        i.RentedItems.end_date=i.RentedItems.end_date.date()

    return render_template("dashboard.html",rented=items_rented, lent=items_lent, ri=ri, li=li)





