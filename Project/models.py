from Project import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from datetime import datetime

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class User(db.Model, UserMixin):
    __tablename__='users'
    id=db.Column(db.Integer, primary_key=True)
    first_name=db.Column(db.String(64))
    last_name=db.Column(db.String(64))
    email=db.Column(db.String(64), unique=True, index=True)
    password_hash=db.Column(db.String(128))
    phone=db.Column(db.String(64))
    address=db.Column(db.String(255))

    items=db.relationship('Items', backref='supplier',lazy=True)
    tenants=db.relationship('RentedItems', backref="tenant", lazy=True)

    def __init__(self, fname,lname, email, password, phone, address):
        self.first_name=fname
        self.last_name=lname
        self.email=email
        self.password_hash=generate_password_hash(password)
        self.phone=phone
        self.address=address
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return f"Name {self.first_name} {self.last_name}"

class Items(db.Model):
    users=db.relationship(User)

    id=db.Column(db.Integer, primary_key=True)
    item_name=db.Column(db.String(64))
    image1=db.Column(db.LargeBinary(length=2048))
    image2=db.Column(db.LargeBinary(length=2048))
    image3=db.Column(db.LargeBinary(length=2048))
    price=db.Column(db.Float)
    category=db.Column(db.String(64))
    supplier_id=db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    rented_items=db.relationship('RentedItems', backref='item',lazy=True)

    # def __init__(self, name, img1, img2, img3, price, cat, supp_id):
    #     self.item_name=name,
    #     self.image1=img1
    #     self.image2=img2
    #     self.image3=img3
    #     self.price=price
    #     self.category=cat
    #     self.supplier_id=supp_id
    # def __init__(self,img1, img2, img3, price, cat, supp_id):
    #     # self.item_name=name,
    #     self.image1=img1
    #     self.image2=img2
    #     self.image3=img3
    #     self.price=price
    #     self.category=cat
    #     self.supplier_id=supp_id
    
    def __repr__(self):
        return f"Item {self.item_name} {self.price}"

class RentedItems(db.Model):
    users=db.relationship(User)
    items=db.relationship(Items)

    id=db.Column(db.Integer, primary_key=True)
    item_id=db.Column(db.Integer, db.ForeignKey('items.id'), nullable=False)
    start_date=db.Column(db.DateTime, nullable=False, default=datetime.now())
    end_date=db.Column(db.DateTime, nullable=False)
    tenant_id=db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    amount=db.Column(db.Float)
    payment_id=db.Column(db.String(64))

    # def __init__(self, itemId, sdate, edate, tid, am, pid):
    #     self.item_id=itemId
    #     self.start_date=sdate
    #     self.end_date=edate
    #     self.tenant_id=tid
    #     self.amount=am
    #     self.payment_id=pid
    
    def __repr__(self):
        return f"Item rented from {self.start_date} - {self.end_date}"
