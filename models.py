from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import datetime

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    wallet_balance = db.Column(db.Float, default=0.0)
    full_name = db.Column(db.String(100), nullable=True)
    email = db.Column(db.String(120), nullable=True)
    phone = db.Column(db.String(20), nullable=True)
    company_name = db.Column(db.String(100), nullable=True)
    razorpay_customer_id = db.Column(db.String(100), nullable=True)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
        
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class VPSInstance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    vps_id = db.Column(db.String(20), unique=True, nullable=False) # e.g. 56892AHF
    name = db.Column(db.String(100), nullable=False)
    plan_name = db.Column(db.String(50), nullable=False)
    status = db.Column(db.String(20), default='Pending') # Active, Pending, Overdue
    billing_date = db.Column(db.Integer, default=16)
    due_date = db.Column(db.Integer, default=20)
    monthly_price = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)

class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    order_id = db.Column(db.String(100), unique=True, nullable=False)
    amount = db.Column(db.Float, nullable=False)
    currency = db.Column(db.String(10), default='INR')
    status = db.Column(db.String(20), default='PENDING') # PENDING, PAID, FAILED, ACTIVE
    description = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)

class StaticIPNickname(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    ip_id = db.Column(db.String(50), nullable=False)
    nickname = db.Column(db.String(100), nullable=False)
    
    # Ensure a user can only have one nickname per IP
    __table_args__ = (db.UniqueConstraint('user_id', 'ip_id', name='_user_ip_uc'),)
