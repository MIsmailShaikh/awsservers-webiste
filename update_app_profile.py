import re

with open('d:/project_vps/app.py', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Add /profile route
profile_route = '''@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
        
    user = User.query.get(session['user_id'])
    
    if request.method == 'POST':
        user.full_name = request.form.get('full_name')
        user.email = request.form.get('email')
        user.phone = request.form.get('phone')
        db.session.commit()
        
        # If they came from checkout, we should let them go back, but for simplicity, just show success.
        flash('Profile updated successfully! You can now proceed to checkout.')
        return redirect(url_for('manage'))
        
    return render_template('profile.html', user=user)

'''

# Insert profile route before @app.route('/create-order'...)
content = re.sub(r'(@app\.route\(\'/create-order\', methods=\[\'POST\'\]\))', profile_route + r'\1', content)


# 2. Update create-order endpoints to enforce profile and return prefill
def replace_create_order(match):
    code = match.group(0)
    # Check if user has profile
    profile_check = '''    user = User.query.get(user_id)
    if not user.full_name or not user.email or not user.phone:
        return {"error": "profile_incomplete"}, 400
        
    amount_inr = '''
    code = code.replace("    amount_inr = ", profile_check, 1)
    
    # Return prefill data
    prefill_ret = '''        return {
            "order_id": razorpay_order['id'],
            "amount": amount_paise,
            "currency": "INR",
            "prefill": {
                "name": user.full_name,
                "email": user.email,
                "contact": user.phone
            }
        }'''
    code = re.sub(r'        return \{"order_id": razorpay_order\[\'id\'\], "amount": amount_paise, "currency": "INR"\}', prefill_ret, code)
    return code

content = re.sub(r'@app\.route\(\'/create-order\', methods=\[\'POST\'\]\)[\s\S]*?(?=\n@app\.route\(\'/create-ip-order\')', replace_create_order, content)

# 3. Update create-ip-order
def replace_ip_order(match):
    code = match.group(0)
    profile_check = '''    user = User.query.get(user_id)
    if not user.full_name or not user.email or not user.phone:
        return {"error": "profile_incomplete"}, 400
        
    req_data = '''
    code = code.replace("    req_data = ", profile_check, 1)
    
    prefill_ret = '''        return {
            "order_id": razorpay_order['id'],
            "amount": amount_paise,
            "currency": "INR",
            "prefill": {
                "name": user.full_name,
                "email": user.email,
                "contact": user.phone
            }
        }'''
    code = re.sub(r'        return \{"order_id": razorpay_order\[\'id\'\], "amount": amount_paise, "currency": "INR"\}', prefill_ret, code)
    return code

content = re.sub(r'@app\.route\(\'/create-ip-order\', methods=\[\'POST\'\]\)[\s\S]*?(?=\n@app\.route\(\'/check-order\')', replace_ip_order, content)

# 4. Update create-wallet-order
def replace_wallet_order(match):
    code = match.group(0)
    profile_check = '''    user = User.query.get(user_id)
    if not user.full_name or not user.email or not user.phone:
        return {"error": "profile_incomplete"}, 400
        
    req_data = '''
    code = code.replace("    req_data = ", profile_check, 1)
    
    prefill_ret = '''        return {
            "order_id": razorpay_order['id'],
            "amount": amount_paise,
            "currency": "INR",
            "prefill": {
                "name": user.full_name,
                "email": user.email,
                "contact": user.phone
            }
        }'''
    code = re.sub(r'        return \{"order_id": razorpay_order\[\'id\'\], "amount": amount_paise, "currency": "INR"\}', prefill_ret, code)
    return code

content = re.sub(r'@app\.route\(\'/create-wallet-order\', methods=\[\'POST\'\]\)[\s\S]*?(?=\n@app\.route\(\'/verify-payment\')', replace_wallet_order, content)


with open('d:/project_vps/app.py', 'w', encoding='utf-8') as f:
    f.write(content)
