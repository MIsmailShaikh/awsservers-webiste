from flask import Flask, render_template, request, redirect, url_for, session, flash
import os
from dotenv import load_dotenv
from datetime import datetime
import calendar
from models import db, User, VPSInstance, Transaction

load_dotenv()

app = Flask(__name__)
app.secret_key = 'super_secret_key_change_in_production'
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'postgresql://postgres:shaikh123@localhost:5432/awsservers')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

@app.context_processor
def inject_cashfree_env():
    # Provide cashfree_env globally to all templates
    return dict(cashfree_env=os.environ.get('CASHFREE_ENV', 'SANDBOX').lower())

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
    
    # Automatically seed the admin user if it doesn't exist
    admin = User.query.filter_by(username='ismailzst643').first()
    if not admin:
        admin = User(username='ismailzst643')
        admin.set_password('1dsO#eK!y5')
        db.session.add(admin)
        db.session.commit()
        
        # Add a dummy VPS instance to match the UI
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
    
    is_paid = False
    is_pending = False
    if latest_tx:
        if latest_tx.status in ['SUCCESS', 'PAID', 'SIMULATED']:
            is_paid = True
        elif latest_tx.status == 'PENDING':
            is_pending = True
    
    # Check for payment result flash from redirect
    payment_result = session.pop('payment_result', None)
        
    return render_template('manage.html', is_paid=is_paid, is_pending=is_pending, payment_result=payment_result)

@app.route('/transactions')
def transactions():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
        
    user_id = session.get('user_id')
    user_transactions = Transaction.query.filter_by(user_id=user_id).order_by(Transaction.created_at.desc()).all()
    
    return render_template('transactions.html', transactions=user_transactions)

from datetime import datetime, timedelta
import calendar

def get_next_dates(day):
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
            
    gen_date = due_date - timedelta(days=4)
    upcoming_date = due_date - timedelta(days=8)
    
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
    due_6, gen_6, pay_6, status_6 = get_next_dates(6)
    due_23, gen_23, pay_23, status_23 = get_next_dates(23)
    due_20, gen_20, pay_20, status_20 = get_next_dates(20)
    
    ips = [
        {
            "id": "238JU2", 
            "address": "15.207.89.102",
            "due_date": due_6,
            "gen_date": gen_6,
            "can_pay": pay_6,
            "type": "Reserved Static IP",
            "is_reserved": True,
            "bill_status": status_6,
            "pointed_to": "Assigned to VPS: 56892AHF"
        },
        {
            "id": "236BG1", 
            "address": "3.108.12.55",
            "due_date": due_23,
            "gen_date": gen_23,
            "can_pay": pay_23,
            "type": "Reserved Static IP",
            "is_reserved": True,
            "bill_status": status_23,
            "pointed_to": "Assigned to VPS: 56892AHF"
        },
        {
            "id": "56892AHF", 
            "address": "72.60.220.68",
            "due_date": due_20,
            "gen_date": gen_20,
            "can_pay": pay_20,
            "type": "Static IP",
            "is_reserved": False,
            "included": "Assigned to VPS",
            "bill_status": status_20,
            "pointed_to": "Assigned to VPS: 56892AHF"
        },
        {
            "id": "Included in VPS", 
            "address": "15.207.90.111",
            "due_date": "Included in VPS",
            "gen_date": "Included in VPS",
            "can_pay": False,
            "type": "Reserved Static IP",
            "is_reserved": True,
            "included": "Included in VPS",
            "bill_status": "Paid",
            "pointed_to": "Assigned to VPS: 56892AHF"
        }
    ]
    
    # Determine IP bill status from database (most recent transaction wins)
    user_id = session.get('user_id')
    ip_status_map = {}  # ip_id -> 'Paid' or 'Pending'
    
    if user_id:
        ip_transactions = Transaction.query.filter(
            Transaction.user_id == user_id, 
            Transaction.order_id.like('order_ip_%')
        ).order_by(Transaction.created_at.desc()).all()
        
        for tx in ip_transactions:
            # Extract ip_id from order_id format: order_ip_{ip_id}_{uuid} or order_ip_{uuid}
            parts = tx.order_id.split('_')
            tx_ip_id = parts[2] if len(parts) > 3 else "238JU2"
            
            # Only use the MOST RECENT transaction for each IP (skip if already determined)
            if tx_ip_id in ip_status_map:
                continue
            
            if tx.status in ['SUCCESS', 'PAID', 'SIMULATED']:
                ip_status_map[tx_ip_id] = 'Paid'
            elif tx.status == 'PENDING':
                ip_status_map[tx_ip_id] = 'Pending'
    
    for ip in ips:
        if ip['id'] in ip_status_map:
            ip['bill_status'] = ip_status_map[ip['id']]
            ip['can_pay'] = False
            
    return ips

@app.route('/static-ips')
def static_ips():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    
    ips = get_static_ips()
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
        
    expiration_date = "2026-03-06"
    return render_template('ip-checkout.html', ip_id=ip_id, expiration_date=expiration_date)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

import requests
import uuid

# Cashfree Sandbox Credentials
CASHFREE_APP_ID = os.environ.get("CASHFREE_APP_ID", "TEST10893622f660c5a84a25452445ec22639801")
CASHFREE_SECRET_KEY = os.environ.get("CASHFREE_SECRET_KEY", "dummy_secret_key_from_env")
CASHFREE_ENV = os.environ.get("CASHFREE_ENV", "SANDBOX")

@app.route('/create-order', methods=['POST'])
def create_order():
    if not session.get('logged_in'):
        return {"error": "Unauthorized"}, 401
    
    user_id = session.get('user_id', 1)
    
    # Bug 1 Fix: Prevent duplicate VPS payments
    existing_pending = Transaction.query.filter(
        Transaction.user_id == user_id,
        Transaction.amount == 39865.00,
        Transaction.status.in_(['PENDING', 'ACTIVE'])
    ).first()
    if existing_pending:
        return {"error": "A payment is already in progress. Please wait for it to complete."}, 409
    
    # Generate a unique order ID
    order_id = f"order_{uuid.uuid4().hex[:10]}"
    
    url = "https://sandbox.cashfree.com/pg/orders"
    if CASHFREE_ENV == "PRODUCTION":
        url = "https://api.cashfree.com/pg/orders"
        
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "X-Api-Version": "2023-08-01",
        "X-Client-Id": CASHFREE_APP_ID,
        "X-Client-Secret": CASHFREE_SECRET_KEY
    }
    
    return_url = request.host_url + "payment-status?order_id=" + order_id
    if CASHFREE_ENV == "PRODUCTION":
        return_url = return_url.replace("http://", "https://")
        
    # Payload for the order
    payload = {
        "order_amount": 39865.00,
        "order_currency": "INR",
        "order_id": order_id,
        "customer_details": {
            "customer_id": f"cust_{user_id}",
            "customer_phone": "9999999999",
            "customer_name": "Test User",
            "customer_email": "test@example.com"
        },
        "order_meta": {
            "return_url": return_url
        }
    }
    
    try:
        response = requests.post(url, json=payload, headers=headers, timeout=15)
        data = response.json()
    except (requests.exceptions.RequestException, ValueError) as e:
        print(f"Cashfree API error: {e}")
        return {"error": "Payment gateway unreachable"}, 503
    
    if response.status_code == 200:
        # Save transaction to database
        new_transaction = Transaction(
            user_id=user_id,
            order_id=order_id,
            amount=39865.00,
            status='PENDING'
        )
        db.session.add(new_transaction)
        db.session.commit()
        
        return {"payment_session_id": data.get("payment_session_id"), "order_id": order_id}
    else:
        print("Cashfree Error:", data)
        return {"error": data.get('message', 'Error creating payment session')}, 400

@app.route('/create-ip-order', methods=['POST'])
def create_ip_order():
    if not session.get('logged_in'):
        return {"error": "Unauthorized"}, 401
        
    user_id = session.get('user_id', 1)
    req_data = request.json or {}
    ip_id = req_data.get('ip_id', 'unknown')
    
    # Bug 2 Fix: Prevent duplicate IP payments
    existing_pending = Transaction.query.filter(
        Transaction.user_id == user_id,
        Transaction.order_id.like(f'order_ip_{ip_id}_%'),
        Transaction.status.in_(['PENDING', 'ACTIVE'])
    ).first()
    if existing_pending:
        return {"error": "A payment for this IP is already in progress. Please wait for it to complete."}, 409
    
    # Generate a unique order ID including ip_id
    order_id = f"order_ip_{ip_id}_{uuid.uuid4().hex[:6]}"
    
    url = "https://sandbox.cashfree.com/pg/orders"
    if CASHFREE_ENV == "PRODUCTION":
        url = "https://api.cashfree.com/pg/orders"
        
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "X-Api-Version": "2023-08-01",
        "X-Client-Id": CASHFREE_APP_ID,
        "X-Client-Secret": CASHFREE_SECRET_KEY
    }
    
    return_url = request.host_url + f"payment-status?order_id={order_id}&ip_id={ip_id}"
    if CASHFREE_ENV == "PRODUCTION":
        return_url = return_url.replace("http://", "https://")
        
    # Payload for the IP order
    payload = {
        "order_amount": 16856.90,
        "order_currency": "INR",
        "order_id": order_id,
        "customer_details": {
            "customer_id": f"cust_{user_id}",
            "customer_phone": "9999999999",
            "customer_name": "Test User",
            "customer_email": "test@example.com"
        },
        "order_meta": {
            "return_url": return_url
        }
    }
    
    try:
        response = requests.post(url, json=payload, headers=headers, timeout=15)
        data = response.json()
    except (requests.exceptions.RequestException, ValueError) as e:
        print(f"Cashfree IP API error: {e}")
        return {"error": "Payment gateway unreachable"}, 503
    
    if response.status_code == 200:
        # Save transaction to database
        new_transaction = Transaction(
            user_id=user_id,
            order_id=order_id,
            amount=16856.90,
            status='PENDING'
        )
        db.session.add(new_transaction)
        db.session.commit()
        
        return {"payment_session_id": data.get("payment_session_id"), "order_id": order_id}
    else:
        print("Cashfree IP Error:", data)
        return {"error": data.get('message', 'Error creating payment session')}, 400

@app.route('/check-order')
def check_order():
    order_id = request.args.get('order_id')
    if not order_id:
        return {"error": "Missing order_id"}, 400
        
    url = f"https://sandbox.cashfree.com/pg/orders/{order_id}"
    headers = {
        "X-Api-Version": "2023-08-01",
        "X-Client-Id": CASHFREE_APP_ID,
        "X-Client-Secret": CASHFREE_SECRET_KEY
    }
    
    # Bug 8 Fix: Error handling on Cashfree API
    try:
        response = requests.get(url, headers=headers, timeout=15)
        if response.status_code == 200:
            data = response.json()
            order_status = data.get("order_status")
            
            # Update database if necessary
            tx = Transaction.query.filter_by(order_id=order_id).first()
            if tx and tx.status != order_status:
                if order_status in ['SUCCESS', 'PAID'] and tx.order_id.startswith('order_wallet_'):
                    user = User.query.get(tx.user_id)
                    if user:
                        if user.wallet_balance is None: user.wallet_balance = 0.0
                        user.wallet_balance += tx.amount
                tx.status = order_status
                db.session.commit()
                
            return {"order_status": order_status}
        return {"error": "Failed to fetch order", "order_status": "UNKNOWN"}, 400
    except (requests.exceptions.RequestException, ValueError) as e:
        print(f"Cashfree check-order error: {e}")
        # Return the DB status as fallback
        tx = Transaction.query.filter_by(order_id=order_id).first()
        if tx:
            return {"order_status": tx.status}
        return {"error": "Payment gateway unreachable", "order_status": "UNKNOWN"}, 503

@app.route('/payment-status')
def payment_status():
    order_id = request.args.get('order_id')
    if not order_id:
        return redirect(url_for('manage'))
        
    tx = Transaction.query.filter_by(order_id=order_id).first()
    
    url = f"https://sandbox.cashfree.com/pg/orders/{order_id}"
    headers = {
        "X-Api-Version": "2023-08-01",
        "X-Client-Id": CASHFREE_APP_ID,
        "X-Client-Secret": CASHFREE_SECRET_KEY
    }
    
    api_status = "UNKNOWN"
    failure_reason = ""
    payment_amount = tx.amount if tx else 0
    
    # Bug 7 Fix: Wrap all Cashfree API calls in try/except
    try:
        response = requests.get(url, headers=headers, timeout=15)
        
        if response.status_code == 200:
            data = response.json()
            api_status = data.get("order_status")
            
            # If order is ACTIVE, check if there was a failed or pending payment attempt
            if api_status == "ACTIVE":
                try:
                    payments_url = f"https://sandbox.cashfree.com/pg/orders/{order_id}/payments"
                    pay_response = requests.get(payments_url, headers=headers, timeout=15)
                    if pay_response.status_code == 200:
                        payments_data = pay_response.json()
                        if payments_data and len(payments_data) > 0:
                            for p in payments_data:
                                p_status = p.get("payment_status")
                                if p_status in ["FAILED", "USER_DROPPED"]:
                                    api_status = "FAILED"
                                    failure_reason = p.get("payment_message", "Transaction was cancelled or failed.")
                                    break
                                elif p_status == "PENDING":
                                    api_status = "PENDING"
                                    break
                except (requests.exceptions.RequestException, ValueError):
                    pass  # Keep api_status as ACTIVE if payments check fails
            
            # Update DB with latest status from Cashfree
            if tx and tx.status != api_status:
                if api_status in ['SUCCESS', 'PAID'] and tx.order_id.startswith('order_wallet_'):
                    user = User.query.get(tx.user_id)
                    if user:
                        if user.wallet_balance is None: user.wallet_balance = 0.0
                        user.wallet_balance += tx.amount
                tx.status = api_status
                db.session.commit()
                
    except (requests.exceptions.RequestException, ValueError) as e:
        print(f"Cashfree payment-status error: {e}")
        # Fallback: use whatever status is in the database
        if tx:
            api_status = tx.status
            failure_reason = "Could not reach payment gateway. Showing last known status."
        else:
            api_status = "UNKNOWN"
            failure_reason = "Payment gateway is currently unreachable. Please try again later."
    
    # Store payment result in session for display on redirect target
    session['payment_result'] = {
        'order_id': order_id,
        'status': api_status,
        'failure_reason': failure_reason,
        'amount': payment_amount
    }
    session.modified = True
    
    ip_id = request.args.get('ip_id')
    if ip_id:
        return redirect(url_for('manage_ip', ip_id=ip_id))
    if order_id.startswith('order_wallet_'):
        return redirect(url_for('wallet'))
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
        new_tx = Transaction(
            user_id=user_id,
            order_id=f'order_ip_{ip_id}_sim{uuid.uuid4().hex[:4]}',
            amount=16856.90,
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
    timestamp = request.headers.get('x-webhook-timestamp')
    signature = request.headers.get('x-webhook-signature')
    raw_body = request.get_data(as_text=True)
    
    if not timestamp or not signature:
        return {"error": "Missing headers"}, 400
        
    # Verify signature
    message = timestamp + raw_body
    computed = hmac.new(
        CASHFREE_SECRET_KEY.encode('utf-8'),
        message.encode('utf-8'),
        hashlib.sha256
    ).digest()
    computed_b64 = base64.b64encode(computed).decode('utf-8')
    
    if computed_b64 != signature:
        print("Webhook signature verification failed.")
        return {"error": "Invalid signature"}, 401
        
    try:
        data = request.json
    except Exception:
        return {"error": "Invalid JSON"}, 400
        
    event_type = data.get('type')
    
    if event_type == 'PAYMENT_SUCCESS_WEBHOOK':
        order_data = data.get('data', {}).get('order', {})
        payment_data = data.get('data', {}).get('payment', {})
        
        order_id = order_data.get('order_id')
        payment_status = payment_data.get('payment_status')
        
        if order_id and payment_status in ['SUCCESS', 'PAID']:
            tx = Transaction.query.filter_by(order_id=order_id).first()
            if tx and tx.status not in ['SUCCESS', 'PAID']:
                if order_id.startswith('order_wallet_'):
                    user = User.query.get(tx.user_id)
                    if user:
                        if user.wallet_balance is None: user.wallet_balance = 0.0
                        user.wallet_balance += tx.amount
                tx.status = payment_status
                db.session.commit()
                print(f"Webhook processed successful payment for order {order_id}")
                
    elif event_type in ['PAYMENT_FAILED_WEBHOOK', 'PAYMENT_USER_DROPPED_WEBHOOK']:
        order_id = data.get('data', {}).get('order', {}).get('order_id')
        if order_id:
            tx = Transaction.query.filter_by(order_id=order_id).first()
            if tx and tx.status not in ['SUCCESS', 'PAID']:
                tx.status = 'FAILED'
                db.session.commit()
                print(f"Webhook processed failed payment for order {order_id}")
                
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
    req_data = request.json or {}
    try:
        amount = float(req_data.get('amount', 0))
    except ValueError:
        return {"error": "Invalid amount"}, 400
        
    if amount <= 0:
        return {"error": "Amount must be greater than 0"}, 400
        
    order_id = f"order_wallet_{uuid.uuid4().hex[:8]}"
    
    url = "https://sandbox.cashfree.com/pg/orders"
    if CASHFREE_ENV == "PRODUCTION":
        url = "https://api.cashfree.com/pg/orders"
        
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "X-Api-Version": "2023-08-01",
        "X-Client-Id": CASHFREE_APP_ID,
        "X-Client-Secret": CASHFREE_SECRET_KEY
    }
    
    return_url = request.host_url + f"payment-status?order_id={order_id}"
    if CASHFREE_ENV == "PRODUCTION":
        return_url = return_url.replace("http://", "https://")
        
    # Payload for the order
    payload = {
        "order_amount": float(amount),
        "order_currency": "INR",
        "order_id": order_id,
        "customer_details": {
            "customer_id": f"cust_{user_id}",
            "customer_phone": "9999999999",
            "customer_name": "Test User",
            "customer_email": "test@example.com"
        },
        "order_meta": {
            "return_url": return_url
        }
    }
    
    try:
        response = requests.post(url, json=payload, headers=headers, timeout=15)
        data = response.json()
    except (requests.exceptions.RequestException, ValueError) as e:
        print(f"Cashfree Wallet API error: {e}")
        return {"error": "Payment gateway unreachable"}, 503
    
    if response.status_code == 200:
        new_transaction = Transaction(
            user_id=user_id, order_id=order_id,
            amount=amount, status='PENDING'
        )
        db.session.add(new_transaction)
        db.session.commit()
        return {"payment_session_id": data.get("payment_session_id"), "order_id": order_id}
    else:
        print("Cashfree Wallet Error:", data)
        return {"error": data.get('message', 'Error creating payment session')}, 400

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

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
