import os
from datetime import datetime, timedelta
import calendar
from flask_mail import Mail, Message
from flask_apscheduler import APScheduler

from flask import Flask, render_template, request, redirect, url_for, session, flash
import os
from dotenv import load_dotenv
from models import db, User, VPSInstance, Transaction, StaticIPNickname, StaticIP
from apscheduler.schedulers.background import BackgroundScheduler

load_dotenv()

app = Flask(__name__)
app.secret_key = 'avpsserver_secret_key'

# Suppress waitress.queue warnings which spam on asset load
import logging
logging.getLogger('waitress.queue').setLevel(logging.ERROR)

app.config['MAIL_SERVER'] = os.environ.get('MAIL_SERVER', 'smtp.gmail.com')
app.config['MAIL_PORT'] = int(os.environ.get('MAIL_PORT', 587))
app.config['MAIL_USE_TLS'] = os.environ.get('MAIL_USE_TLS', 'true').lower() in ['true', 'on', '1']
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME', 'care@avpsserver.in')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD', 'your-app-password')
app.config['MAIL_DEFAULT_SENDER'] = os.environ.get('MAIL_DEFAULT_SENDER', 'care@avpsserver.in')

mail = Mail(app)
scheduler = APScheduler()
scheduler.init_app(app)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'postgresql://postgres:shaikh123@localhost:5432/awsservers')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


import razorpay

RAZORPAY_KEY_ID = os.environ.get("RAZORPAY_KEY_ID", "")
RAZORPAY_KEY_SECRET = os.environ.get("RAZORPAY_KEY_SECRET", "")

razorpay_client = razorpay.Client(auth=(RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET))

@app.context_processor
def inject_razorpay_key():
    return dict(razorpay_key_id=RAZORPAY_KEY_ID)

db.init_app(app)

with app.app_context():
    # Automatically create tables if they don't exist
    db.create_all()
    
    try:
        from sqlalchemy import text
        db.session.execute(text('ALTER TABLE "user" ADD COLUMN wallet_balance FLOAT DEFAULT 0.0'))
        db.session.commit()
    except Exception as e:
        db.session.rollback()

    try:
        from sqlalchemy import text
        db.session.execute(text('ALTER TABLE transaction ADD COLUMN description VARCHAR(255)'))
        db.session.commit()
    except Exception as e:
        db.session.rollback()

    try:
        from sqlalchemy import text
        db.session.execute(text('ALTER TABLE "user" ADD COLUMN razorpay_customer_id VARCHAR(100)'))
        db.session.commit()
    except Exception as e:
        db.session.rollback()

    try:
        from sqlalchemy import text
        db.session.execute(text('ALTER TABLE "user" ADD COLUMN company_name VARCHAR(100)'))
        db.session.commit()
    except Exception as e:
        db.session.rollback()

    try:
        from sqlalchemy import text
        db.session.execute(text('ALTER TABLE "user" ADD COLUMN full_name VARCHAR(100)'))
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        
    try:
        from sqlalchemy import text
        db.session.execute(text('ALTER TABLE "user" ADD COLUMN email VARCHAR(120)'))
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        
    try:
        from sqlalchemy import text
        db.session.execute(text('ALTER TABLE "user" ADD COLUMN phone VARCHAR(20)'))
        db.session.commit()
    except Exception as e:
        db.session.rollback()
    
    # Automatically seed the admin user if it doesn't exist
    admin = User.query.filter_by(username='ismailzst643').first()
    if not admin:
        admin = User(username='ismailzst643')
        admin.set_password('1dsO#eK!y5')
        db.session.add(admin)
        db.session.commit()
        
        # Add a dummy VPS instance to match the UI if it doesn't exist
        vps = VPSInstance.query.filter_by(vps_id='56892AHF').first()
        if not vps:
            vps = VPSInstance(
                user_id=admin.id,
                vps_id='56892AHF',
                name='edge-1',
                plan_name='Pro',
                status='Active',
                billing_date=16,
                due_date=20,
                monthly_price=33783.90
            )
            db.session.add(vps)
            db.session.commit()
            
    # Force update/seed Static IP instances to match the UI and fix dates
    ips_to_seed = [
        {"ip_id": "238JU2", "address": "15.207.89.102", "billing_date": 4, "due_date": 6, "monthly_price": 10.0, "status": "Active", "is_reserved": True, "included_in": "VPS: 56892AHF"}, 
        {"ip_id": "236BG1", "address": "3.108.12.55", "billing_date": 19, "due_date": 23, "monthly_price": 10.0, "status": "Active", "is_reserved": True, "included_in": "VPS: 56892AHF"}, 
        {"ip_id": "8547JW4", "address": "72.60.220.68", "billing_date": 16, "due_date": 18, "monthly_price": 10.0, "status": "Active", "is_reserved": False, "included_in": "Standard Server Plan", "last_billed_month": "2026-07"},
        {"ip_id": "9482KL1", "address": "203.0.113.42", "billing_date": 16, "due_date": 20, "monthly_price": 0.0, "status": "Active", "is_reserved": True, "included_in": "VPS: 56892AHF"}
    ]
    
    nicks_to_seed = [
        {"ip_id": "238JU2", "nickname": "wefewfewf"}
    ]
    
    admin = User.query.filter_by(username='ismailzst643').first()
    if admin:
        if not admin.email:
            admin.email = 'mohammedismailshaikh454@gmail.com'
            ip_236 = StaticIP.query.filter_by(ip_id='236BG1').first()
            if ip_236:
                ip_236.last_billed_month = None
            db.session.commit()
            
        for ip_data in ips_to_seed:
            static_ip = StaticIP.query.filter_by(ip_id=ip_data['ip_id']).first()
            if not static_ip:
                static_ip = StaticIP(
                    user_id=admin.id,
                    **ip_data
                )
                db.session.add(static_ip)
            else:
                for key, value in ip_data.items():
                    setattr(static_ip, key, value)
                    
        for nick_data in nicks_to_seed:
            nick = StaticIPNickname.query.filter_by(ip_id=nick_data['ip_id'], user_id=admin.id).first()
            if not nick:
                nick = StaticIPNickname(
                    user_id=admin.id,
                    **nick_data
                )
                db.session.add(nick)
            else:
                for key, value in nick_data.items():
                    setattr(nick, key, value)
                
        db.session.commit()
        
    try:
        from sqlalchemy import text
        db.session.execute(text('ALTER TABLE vps_instance ADD COLUMN last_billed_month VARCHAR(10)'))
        db.session.execute(text('ALTER TABLE static_ip ADD COLUMN last_billed_month VARCHAR(10)'))
        db.session.commit()
    except Exception as e:
        db.session.rollback()

from datetime import timedelta

@app.template_filter('to_ist')
def to_ist_filter(dt):
    if not dt: return ""
    return dt + timedelta(hours=5, minutes=30)

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            session['logged_in'] = True
            session['user_id'] = user.id
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password', 'error')
            
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    return render_template('dashboard.html')

@app.route('/manage')
def manage():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
        
    user_id = session.get('user_id')
    latest_tx = Transaction.query.filter_by(user_id=user_id, amount=39865.00).order_by(Transaction.created_at.desc()).first()
    
    now = datetime.utcnow()
    due_date = now.replace(day=20, hour=0, minute=0, second=0, microsecond=0)
    
    if now > due_date:
        if now.month == 12:
            due_date = due_date.replace(year=now.year + 1, month=1)
        else:
            due_date = due_date.replace(month=now.month + 1)
            
    gen_date = due_date - timedelta(days=4)
    
    is_paid = False
    is_pending = False
    
    if now < gen_date:
        is_paid = True
    else:
        if latest_tx and latest_tx.created_at >= gen_date:
            if latest_tx.status in ['SUCCESS', 'PAID', 'SIMULATED']:
                is_paid = True
            elif latest_tx.status == 'PENDING':
                is_pending = True
    
    # Check for payment result flash from redirect
    payment_result = session.pop('payment_result', None)
    
    expiration_date = due_date.strftime('%Y-%m-%d')
        
    return render_template('manage.html', is_paid=is_paid, is_pending=is_pending, payment_result=payment_result, expiration_date=expiration_date)


@app.route('/update-ip-nickname', methods=['POST'])
def update_ip_nickname():
    if not session.get('logged_in'):
        return {"error": "Unauthorized"}, 401
        
    req_data = request.json
    ip_id = req_data.get('ip_id')
    nickname = req_data.get('nickname')
    
    if not ip_id:
        return {"error": "ip_id is required"}, 400
        
    user_id = session.get('user_id')
    nick_obj = StaticIPNickname.query.filter_by(user_id=user_id, ip_id=ip_id).first()
    
    if nickname:
        if nick_obj:
            nick_obj.nickname = nickname
        else:
            nick_obj = StaticIPNickname(user_id=user_id, ip_id=ip_id, nickname=nickname)
            db.session.add(nick_obj)
    else:
        # If empty nickname is sent, we can delete the record or set it to empty
        if nick_obj:
            db.session.delete(nick_obj)
            
    db.session.commit()
    return {"status": "success"}

@app.route('/transactions')
def transactions():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
        
    user_id = session.get('user_id')
    user_transactions = Transaction.query.filter_by(user_id=user_id).order_by(Transaction.created_at.desc()).all()
    
    return render_template('transactions.html', transactions=user_transactions)

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/terms')
def terms():
    return render_template('terms.html')

@app.route('/privacy')
def privacy():
    return render_template('privacy.html')

@app.route('/refunds')
def refunds():
    return render_template('refunds.html')

@app.route('/shipping')
def shipping():
    return render_template('shipping.html')

@app.route('/pricing')
def pricing():
    return render_template('pricing.html')

from flask_mail import Mail, Message
from flask_apscheduler import APScheduler
import os
from datetime import datetime, timedelta
import calendar
import calendar

def get_next_dates(day, gen_offset=4, upcoming_offset=8):
    now = datetime.now()
    try:
        due_date = now.replace(day=day)
    except ValueError:
        last_day = calendar.monthrange(now.year, now.month)[1]
        due_date = now.replace(day=last_day)
        
    if now > due_date:
        if now.month == 12:
            new_month = 1
            new_year = now.year + 1
        else:
            new_month = now.month + 1
            new_year = now.year
            
        try:
            due_date = due_date.replace(year=new_year, month=new_month)
        except ValueError:
            last_day = calendar.monthrange(new_year, new_month)[1]
            due_date = due_date.replace(year=new_year, month=new_month, day=last_day)
            
    gen_date = due_date - timedelta(days=gen_offset)
    upcoming_date = due_date - timedelta(days=upcoming_offset)
    
    if now >= gen_date:
        bill_status = "Unpaid"
        can_pay = True
    elif now >= upcoming_date:
        bill_status = "Upcoming"
        can_pay = False
    else:
        bill_status = "Paid"
        can_pay = False
        
    return due_date.strftime("%d %b %Y"), gen_date.strftime("%d %b %Y"), can_pay, bill_status

def get_static_ips():
    user_id = session.get('user_id') if session.get('logged_in') else 1
    db_ips = StaticIP.query.filter_by(user_id=user_id).all()
    
    ips = []
    for db_ip in db_ips:
        billing_date = db_ip.billing_date
        due_date = db_ip.due_date
        
        gen_offset = due_date - billing_date
        if gen_offset <= 0:
            gen_offset = 4
            
        due_date_str, gen_date_str, can_pay, bill_status = get_next_dates(due_date, gen_offset=gen_offset)
        
        if db_ip.monthly_price == 0.0:
            bill_status = "Included in VPS"
            due_date_str = "Included in VPS"
            can_pay = False
            
        ips.append({
            "id": db_ip.ip_id,
            "address": db_ip.address,
            "due_date": due_date_str,
            "gen_date": gen_date_str,
            "monthly_price": db_ip.monthly_price,
            "type": "Reserved Static IP" if db_ip.is_reserved else "Static IP",
            "status": db_ip.status,
            "is_reserved": db_ip.is_reserved,
            "included": db_ip.included_in,
            "bill_status": bill_status,
            "can_pay": can_pay
        })
        
    status_priority = {
        "Unpaid": 1,
        "Pending": 2,
        "Upcoming": 3,
        "Paid": 4,
        "Included in VPS": 5
    }
    ips.sort(key=lambda x: status_priority.get(x['bill_status'], 99))
        
    return ips

@app.route('/static-ips')
def static_ips():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    
    ips = get_static_ips()
    
    user_id = session.get('user_id')
    nicknames = StaticIPNickname.query.filter_by(user_id=user_id).all()
    nickname_map = {n.ip_id: n.nickname for n in nicknames}
    
    for ip in ips:
        if ip['id'] in nickname_map:
            ip['nickname'] = nickname_map[ip['id']]
            
    return render_template('static-ips.html', static_ips=ips)

@app.route('/manage-ip/<ip_id>')
def manage_ip(ip_id):
    if not session.get('logged_in'):
        return redirect(url_for('login'))
        
    ips = get_static_ips()
    ip_data = next((ip for ip in ips if ip['id'] == ip_id), None)
    
    if not ip_data:
        return redirect(url_for('static_ips'))
    
    # Check for payment result flash from redirect
    payment_result = session.pop('payment_result', None)
        
    return render_template('manage-ip.html', ip=ip_data, payment_result=payment_result)

@app.route('/checkout-ip/<ip_id>')
def checkout_ip(ip_id):
    if not session.get('logged_in'):
        return redirect(url_for('login'))
        
    ips = get_static_ips()
    ip_data = next((ip for ip in ips if ip['id'] == ip_id), None)
    
    expiration_date = "2026-07-20"
    if ip_data:
        from datetime import datetime
        try:
            parsed_date = datetime.strptime(ip_data['due_date'], "%d %b %Y")
            expiration_date = parsed_date.strftime("%Y-%m-%d")
        except ValueError:
            pass

    if ip_data and ip_data['id'] == '8547JW4':
        base_amount = "13,966.95"
        tax_amount = "2,514.05"
        total_amount = "16,481.00"
    else:
        base_amount = "14,285.52"
        tax_amount = "2,571.38"
        total_amount = "16,856.90"

    return render_template('ip-checkout.html', ip_id=ip_id, expiration_date=expiration_date, base_amount=base_amount, tax_amount=tax_amount, total_amount=total_amount)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

import requests
import uuid


@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
        
    user = User.query.get(session['user_id'])
    
    if request.method == 'POST':
        user.full_name = request.form.get('full_name')
        user.email = request.form.get('email')
        user.phone = request.form.get('phone')
        user.company_name = request.form.get('company_name')
        
        if not user.razorpay_customer_id:
            try:
                cust = razorpay_client.customer.create({
                    "name": user.full_name,
                    "email": user.email,
                    "contact": user.phone
                })
                user.razorpay_customer_id = cust['id']
            except Exception as e:
                print(f"Failed to create Razorpay customer: {e}")
                
        db.session.commit()
        
        # If they came from checkout, we should let them go back, but for simplicity, just show success.
        flash('Profile updated successfully! You can now proceed to checkout.')
        return redirect(url_for('manage'))
        
    return render_template('profile.html', user=user)

@app.route('/create-order', methods=['POST'])
def create_order():
    if not session.get('logged_in'):
        return {"error": "Unauthorized"}, 401
    
    user_id = session.get('user_id', 1)
    user = User.query.get(user_id)
    if not user.full_name or not user.email or not user.phone:
        return {"error": "profile_incomplete"}, 400
        
    amount_inr = 39865.00
    amount_paise = int(amount_inr * 100)
    
    try:
        order_data = {
            "amount": amount_paise,
            "currency": "INR",
            "receipt": f"receipt_{user_id}_{uuid.uuid4().hex[:6]}"
        }
        razorpay_order = razorpay_client.order.create(data=order_data)
        
        new_transaction = Transaction(
            user_id=user_id,
            order_id=razorpay_order['id'],
            amount=amount_inr,
            status='PENDING',
            description='Cloud Infrastructure Services'
        )
        db.session.add(new_transaction)
        db.session.commit()
        
        return {
            "order_id": razorpay_order['id'],
            "amount": amount_paise,
            "currency": "INR",
            "prefill": {
                "name": user.full_name,
                "email": user.email,
                "contact": user.phone
            },
            "customer_id": user.razorpay_customer_id
        }
    except Exception as e:
        print(f"Razorpay error: {e}")
        return {"error": "Failed to create order"}, 500

@app.route('/create-ip-order', methods=['POST'])
def create_ip_order():
    if not session.get('logged_in'):
        return {"error": "Unauthorized"}, 401
        
    user_id = session.get('user_id', 1)
    user = User.query.get(user_id)
    if not user.full_name or not user.email or not user.phone:
        return {"error": "profile_incomplete"}, 400
        
    req_data = request.json or {}
    ip_id = req_data.get('ip_id', 'unknown')
    
    amount_inr = 16481.00 if ip_id == "8547JW4" else 16856.90
    amount_paise = int(amount_inr * 100)
    
    try:
        order_data = {
            "amount": amount_paise,
            "currency": "INR",
            "receipt": f"ip_{ip_id}_{uuid.uuid4().hex[:4]}",
            "notes": {"ip_id": ip_id}
        }
        razorpay_order = razorpay_client.order.create(data=order_data)
        
        new_transaction = Transaction(
            user_id=user_id,
            order_id=razorpay_order['id'],
            amount=amount_inr,
            status='PENDING',
            description='Cloud Infrastructure Services'
        )
        db.session.add(new_transaction)
        db.session.commit()
        
        return {
            "order_id": razorpay_order['id'],
            "amount": amount_paise,
            "currency": "INR",
            "prefill": {
                "name": user.full_name,
                "email": user.email,
                "contact": user.phone
            },
            "customer_id": user.razorpay_customer_id
        }
    except Exception as e:
        print(f"Razorpay IP error: {e}")
        return {"error": "Failed to create order"}, 500

@app.route('/check-order')
def check_order():
    return {"error": "Payment system under maintenance", "order_status": "UNKNOWN"}, 503

@app.route('/payment-status')
def payment_status():
    session['payment_result'] = {
        'order_id': 'unknown',
        'status': 'UNKNOWN',
        'failure_reason': 'Payment system under maintenance',
        'amount': 0
    }
    session.modified = True
    return redirect(url_for('manage'))

@app.route('/simulate-ip-success/<ip_id>')
def simulate_ip_success(ip_id):
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    
    user_id = session.get('user_id', 1)
    
    # Bug 10 Fix: Update the database, not just the session
    # Find the most recent IP transaction for this ip_id and mark it SUCCESS
    latest_ip_tx = Transaction.query.filter(
        Transaction.user_id == user_id,
        Transaction.order_id.like(f'order_ip_{ip_id}_%')
    ).order_by(Transaction.created_at.desc()).first()
    
    if latest_ip_tx:
        latest_ip_tx.status = 'SUCCESS'
        db.session.commit()
    else:
        # No transaction exists yet (edge case) — create one
        order_amount = 16481.00 if ip_id == "8547JW4" else 16856.90
        
        new_tx = Transaction(
            user_id=user_id,
            order_id=f'order_ip_{ip_id}_sim{uuid.uuid4().hex[:4]}',
            amount=order_amount,
            status='SUCCESS'
        )
        db.session.add(new_tx)
        db.session.commit()
    
    return redirect(url_for('manage_ip', ip_id=ip_id))

@app.route('/simulate-vps-success')
def simulate_vps_success():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
        
    user_id = session.get('user_id')
    latest_tx = Transaction.query.filter_by(user_id=user_id, amount=39865.00).order_by(Transaction.created_at.desc()).first()
    if latest_tx:
        latest_tx.status = 'SUCCESS'
        db.session.commit()
    else:
        # No transaction exists (edge case) — create one
        new_tx = Transaction(
            user_id=user_id,
            order_id=f'order_sim_{uuid.uuid4().hex[:8]}',
            amount=39865.00,
            status='SUCCESS'
        )
        db.session.add(new_tx)
        db.session.commit()
    
    return redirect(url_for('manage'))

import hmac
import hashlib
import base64

@app.route('/cashfree-webhook', methods=['POST'])
def cashfree_webhook():
    return 'OK', 200

@app.route('/wallet')
def wallet():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
        
    user_id = session.get('user_id')
    user = User.query.get(user_id)
    payment_result = session.pop('payment_result', None)
    
    balance = user.wallet_balance if user and user.wallet_balance is not None else 0.0
    
    return render_template('wallet.html', balance=balance, payment_result=payment_result)

@app.route('/create-wallet-order', methods=['POST'])
def create_wallet_order():
    if not session.get('logged_in'):
        return {"error": "Unauthorized"}, 401
        
    user_id = session.get('user_id', 1)
    user = User.query.get(user_id)
    if not user.full_name or not user.email or not user.phone:
        return {"error": "profile_incomplete"}, 400
        
    req_data = request.json or {}
    try:
        amount_inr = float(req_data.get('amount', 0))
    except ValueError:
        return {"error": "Invalid amount"}, 400
        
    if amount_inr < 1:
        return {"error": "Amount must be at least 1 INR"}, 400
        
    amount_paise = int(amount_inr * 100)
    
    try:
        order_data = {
            "amount": amount_paise,
            "currency": "INR",
            "receipt": f"wallet_{user_id}_{uuid.uuid4().hex[:6]}"
        }
        razorpay_order = razorpay_client.order.create(data=order_data)
        
        new_transaction = Transaction(
            user_id=user_id,
            order_id=razorpay_order['id'],
            amount=amount_inr,
            status='PENDING',
            description='Cloud Infrastructure Services'
        )
        db.session.add(new_transaction)
        db.session.commit()
        
        return {
            "order_id": razorpay_order['id'],
            "amount": amount_paise,
            "currency": "INR",
            "prefill": {
                "name": user.full_name,
                "email": user.email,
                "contact": user.phone
            },
            "customer_id": user.razorpay_customer_id
        }
    except Exception as e:
        print(f"Razorpay Wallet error: {e}")
        return {"error": "Failed to create order"}, 500

@app.route('/verify-payment', methods=['POST'])
def verify_payment():
    if not session.get('logged_in'):
        return {"error": "Unauthorized"}, 401
        
    req_data = request.json or {}
    razorpay_payment_id = req_data.get('razorpay_payment_id')
    razorpay_order_id = req_data.get('razorpay_order_id')
    razorpay_signature = req_data.get('razorpay_signature')
    
    if not razorpay_payment_id or not razorpay_order_id or not razorpay_signature:
        return {"error": "Missing signature fields"}, 400
        
    try:
        razorpay_client.utility.verify_payment_signature({
            'razorpay_order_id': razorpay_order_id,
            'razorpay_payment_id': razorpay_payment_id,
            'razorpay_signature': razorpay_signature
        })
    except Exception as e:
        print(f"Signature verification failed: {e}")
        return {"error": "Invalid signature"}, 400
        
    # Signature is valid, update DB
    tx = Transaction.query.filter_by(order_id=razorpay_order_id).first()
    if tx and tx.status != 'SUCCESS':
        tx.status = 'SUCCESS'
        
        # Determine if it was a wallet top-up by notes or amount
        # For our app, we can just check if it was a wallet transaction by checking the user's latest transaction or passing metadata
        # A better way is passing the context from the frontend, but we can also infer:
        # If it was from wallet, we need to add to wallet balance.
        # Actually, let's pass an additional flag from frontend if it was a wallet topup.
        context = req_data.get('context')
        if context == 'wallet':
            user = User.query.get(tx.user_id)
            if user:
                if user.wallet_balance is None: user.wallet_balance = 0.0
                user.wallet_balance += tx.amount
        
        db.session.commit()
        return {"status": "success"}
        
    return {"status": "success", "note": "Already processed"}

@app.route('/simulate-wallet-success/<order_id>')
def simulate_wallet_success(order_id):
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    
    tx = Transaction.query.filter_by(order_id=order_id).first()
    if tx and tx.status != 'SUCCESS':
        user = User.query.get(tx.user_id)
        if user:
            if user.wallet_balance is None: user.wallet_balance = 0.0
            user.wallet_balance += tx.amount
        tx.status = 'SUCCESS'
        db.session.commit()
        
    return redirect(url_for('wallet'))


@app.route('/payment-success/<order_id>')
def payment_success(order_id):
    if not session.get('logged_in'):
        return redirect(url_for('login'))
        
    tx = Transaction.query.filter_by(order_id=order_id).first()
    if not tx:
        flash("Order not found")
        return redirect(url_for('dashboard'))
        
    user = User.query.get(tx.user_id)
    return render_template('success.html', tx=tx, user=user)

@app.route('/download-invoice/<order_id>')
def download_invoice(order_id):
    if not session.get('logged_in'):
        return redirect(url_for('login'))
        
    tx = Transaction.query.filter_by(order_id=order_id).first()
    if not tx:
        flash("Order not found")
        return redirect(url_for('dashboard'))
        
    user = User.query.get(tx.user_id)
    return render_template('invoice.html', tx=tx, user=user)



def send_billing_email(user_name, user_email, item_name, nickname, amount, gen_date_str, due_date_str):
    msg = Message(f"Action Required: Your AVPS Server Bill is Ready", recipients=[user_email])
    
    html_content = render_template('emails/billing.html', 
        user_name=user_name, 
        item_name=item_name, 
        nickname=nickname,
        amount=amount, 
        gen_date=gen_date_str,
        due_date=due_date_str, 
        current_year=datetime.now().year
    )
    msg.html = html_content
    
    try:
        mail.send(msg)
    except Exception as e:
        print(f"Failed to send email to {user_email}: {e}")


@app.route('/payment-link-success/<order_id>')
def payment_link_success(order_id):
    payment_id = request.args.get('razorpay_payment_id')
    payment_link_id = request.args.get('razorpay_payment_link_id')
    
    if not payment_id or not payment_link_id:
        flash('Invalid payment response from Razorpay.', 'error')
        return redirect(url_for('manage'))
        
    try:
        # Fetch payment link details to ensure it's paid
        link = razorpay_client.payment_link.fetch(payment_link_id)
        if link.get('status') == 'paid':
            tx = Transaction.query.filter_by(order_id=order_id).first()
            if tx and tx.status != 'PAID':
                tx.status = 'PAID'
                db.session.commit()
                flash('Payment completed successfully!', 'success')
            elif tx and tx.status == 'PAID':
                flash('Payment already processed.', 'success')
            else:
                flash('Transaction not found.', 'error')
        else:
            flash('Payment link is not marked as paid.', 'error')
            
    except Exception as e:
        print("Error verifying payment link:", str(e))
        flash('Failed to verify payment.', 'error')
        
    return redirect(url_for('manage'))

@scheduler.task('cron', id='daily_billing_check', hour=0, minute=0)
def daily_billing_check():
    with app.app_context():
        current_month = datetime.now().strftime('%Y-%m')
        
        # 1. Check VPS Instances
        vps_instances = VPSInstance.query.all()
        for vps in vps_instances:
            due_date_dt = datetime.now().replace(day=vps.due_date)
            if datetime.now() > due_date_dt:
                due_date_dt = (due_date_dt.replace(day=1) + timedelta(days=32)).replace(day=vps.due_date)
            gen_date_dt = due_date_dt - timedelta(days=4)
            if datetime.now().date() >= gen_date_dt.date() and vps.last_billed_month != current_month:
                user = User.query.get(vps.user_id)
                if user:
                    due_date_str = due_date_dt.strftime('%d %b, %Y')
                    gen_date_str = gen_date_dt.strftime('%d %b, %Y')
                    nickname = vps.name
                    send_billing_email(user.company_name or f"User {user.id}", user.email, f"Cloud Server ({vps.vps_id})", nickname, vps.monthly_price, gen_date_str, due_date_str)
                    vps.last_billed_month = current_month
                    db.session.commit()
                    
        # 2. Check Static IPs
        static_ips = StaticIP.query.all()
        for ip in static_ips:
            if ip.monthly_price == 0.0:
                continue
            due_date_dt = datetime.now().replace(day=ip.due_date)
            if datetime.now() > due_date_dt:
                due_date_dt = (due_date_dt.replace(day=1) + timedelta(days=32)).replace(day=ip.due_date)
            gen_date_dt = due_date_dt - timedelta(days=4)
            if datetime.now().date() >= gen_date_dt.date() and ip.last_billed_month != current_month:
                user = User.query.get(ip.user_id)
                if user:
                    due_date_str = due_date_dt.strftime('%d %b, %Y')
                    gen_date_str = gen_date_dt.strftime('%d %b, %Y')
                    nick_obj = StaticIPNickname.query.filter_by(user_id=ip.user_id, ip_id=ip.ip_id).first()
                    nickname = nick_obj.nickname if nick_obj else ""
                    send_billing_email(user.company_name or f"User {user.id}", user.email, f"Static IP ({ip.address})", nickname, ip.monthly_price, gen_date_str, due_date_str)
                    ip.last_billed_month = current_month
                    db.session.commit()

import threading
if __name__ != '__main__':
    threading.Thread(target=daily_billing_check).start()
