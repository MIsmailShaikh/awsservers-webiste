import re

with open('d:/project_vps/app.py', 'r') as f:
    content = f.read()

# 1. Remove inject_cashfree_env context processor
content = re.sub(r'@app\.context_processor\s+def inject_cashfree_env\(\):[\s\S]*?return dict\(cashfree_env=os\.environ\.get\([^)]+\)\.lower\(\)\)\n', '', content)

# 2. Replace payment functions with maintenance error
def replace_func(func_name, replacement):
    global content
    pattern = r'@app\.route\(' + func_name + r'[\s\S]*?(?=\n@app\.route)'
    content = re.sub(pattern, replacement, content)

content = re.sub(r'# Cashfree Sandbox Credentials.*?CASHFREE_ENV = .*?\n', '', content, flags=re.DOTALL)

payment_stub = '''@app.route('/create-order', methods=['POST'])
def create_order():
    return {"error": "Payment system under maintenance"}, 503
'''
content = re.sub(r'@app\.route\(\'/create-order\', methods=\[\'POST\'\]\)[\s\S]*?(?=\n@app\.route\(\'/create-ip-order\')', payment_stub, content)

ip_stub = '''@app.route('/create-ip-order', methods=['POST'])
def create_ip_order():
    return {"error": "Payment system under maintenance"}, 503
'''
content = re.sub(r'@app\.route\(\'/create-ip-order\', methods=\[\'POST\'\]\)[\s\S]*?(?=\n@app\.route\(\'/check-order\')', ip_stub, content)

check_stub = '''@app.route('/check-order')
def check_order():
    return {"error": "Payment system under maintenance", "order_status": "UNKNOWN"}, 503
'''
content = re.sub(r'@app\.route\(\'/check-order\'\)[\s\S]*?(?=\n@app\.route\(\'/payment-status\')', check_stub, content)

status_stub = '''@app.route('/payment-status')
def payment_status():
    session['payment_result'] = {
        'order_id': 'unknown',
        'status': 'UNKNOWN',
        'failure_reason': 'Payment system under maintenance',
        'amount': 0
    }
    session.modified = True
    return redirect(url_for('manage'))
'''
content = re.sub(r'@app\.route\(\'/payment-status\'\)[\s\S]*?(?=\n@app\.route\(\'/simulate-ip-success)', status_stub, content)

webhook_stub = '''@app.route('/cashfree-webhook', methods=['POST'])
def cashfree_webhook():
    return 'OK', 200
'''
content = re.sub(r'@app\.route\(\'/cashfree-webhook\', methods=\[\'POST\'\]\)[\s\S]*?(?=\n@app\.route\(\'/wallet\')', webhook_stub, content)

wallet_stub = '''@app.route('/create-wallet-order', methods=['POST'])
def create_wallet_order():
    return {"error": "Payment system under maintenance"}, 503
'''
content = re.sub(r'@app\.route\(\'/create-wallet-order\', methods=\[\'POST\'\]\)[\s\S]*?(?=\n@app\.route\(\'/simulate-wallet-success)', wallet_stub, content)

with open('d:/project_vps/app.py', 'w') as f:
    f.write(content)
