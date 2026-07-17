import re

with open('d:/project_vps/app.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Add razorpay import and client init
init_code = '''import razorpay

RAZORPAY_KEY_ID = os.environ.get("RAZORPAY_KEY_ID", "")
RAZORPAY_KEY_SECRET = os.environ.get("RAZORPAY_KEY_SECRET", "")

razorpay_client = razorpay.Client(auth=(RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET))

@app.context_processor
def inject_razorpay_key():
    return dict(razorpay_key_id=RAZORPAY_KEY_ID)
'''

content = content.replace('db.init_app(app)', init_code + '\n' + 'db.init_app(app)')

# Stub replacements
create_order_code = '''@app.route('/create-order', methods=['POST'])
def create_order():
    if not session.get('logged_in'):
        return {"error": "Unauthorized"}, 401
    
    user_id = session.get('user_id', 1)
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
            status='PENDING'
        )
        db.session.add(new_transaction)
        db.session.commit()
        
        return {"order_id": razorpay_order['id'], "amount": amount_paise, "currency": "INR"}
    except Exception as e:
        print(f"Razorpay error: {e}")
        return {"error": "Failed to create order"}, 500
'''
content = re.sub(r'@app\.route\(\'/create-order\', methods=\[\'POST\'\]\)[\s\S]*?(?=\n@app\.route\(\'/create-ip-order\')', create_order_code, content)

create_ip_order_code = '''@app.route('/create-ip-order', methods=['POST'])
def create_ip_order():
    if not session.get('logged_in'):
        return {"error": "Unauthorized"}, 401
        
    user_id = session.get('user_id', 1)
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
            status='PENDING'
        )
        db.session.add(new_transaction)
        db.session.commit()
        
        return {"order_id": razorpay_order['id'], "amount": amount_paise, "currency": "INR"}
    except Exception as e:
        print(f"Razorpay IP error: {e}")
        return {"error": "Failed to create order"}, 500
'''
content = re.sub(r'@app\.route\(\'/create-ip-order\', methods=\[\'POST\'\]\)[\s\S]*?(?=\n@app\.route\(\'/check-order\')', create_ip_order_code, content)

create_wallet_order_code = '''@app.route('/create-wallet-order', methods=['POST'])
def create_wallet_order():
    if not session.get('logged_in'):
        return {"error": "Unauthorized"}, 401
        
    user_id = session.get('user_id', 1)
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
            status='PENDING'
        )
        db.session.add(new_transaction)
        db.session.commit()
        
        return {"order_id": razorpay_order['id'], "amount": amount_paise, "currency": "INR"}
    except Exception as e:
        print(f"Razorpay Wallet error: {e}")
        return {"error": "Failed to create order"}, 500
'''
content = re.sub(r'@app\.route\(\'/create-wallet-order\', methods=\[\'POST\'\]\)[\s\S]*?(?=\n@app\.route\(\'/simulate-wallet-success)', create_wallet_order_code, content)

verify_payment_code = '''@app.route('/verify-payment', methods=['POST'])
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
'''

# insert verify_payment after create_wallet_order
content = content.replace("@app.route('/simulate-wallet-success/<order_id>')", verify_payment_code + '\n' + "@app.route('/simulate-wallet-success/<order_id>')")

with open('d:/project_vps/app.py', 'w', encoding='utf-8') as f:
    f.write(content)
