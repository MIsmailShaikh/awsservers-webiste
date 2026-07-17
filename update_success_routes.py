import re

with open('d:/project_vps/app.py', 'r', encoding='utf-8') as f:
    content = f.read()

success_routes = '''
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

'''

# Insert before if __name__ == '__main__':
content = content.replace("if __name__ == '__main__':", success_routes + "\nif __name__ == '__main__':")

with open('d:/project_vps/app.py', 'w', encoding='utf-8') as f:
    f.write(content)

# Update static/app.js to redirect to /payment-success/
with open('d:/project_vps/static/app.js', 'r', encoding='utf-8') as f:
    app_js = f.read()
    
app_js = app_js.replace("window.location.href = '/simulate-vps-success';", "window.location.href = '/payment-success/' + data.order_id;")

with open('d:/project_vps/static/app.js', 'w', encoding='utf-8') as f:
    f.write(app_js)
    
# Update wallet.html
with open('d:/project_vps/templates/wallet.html', 'r', encoding='utf-8') as f:
    wallet = f.read()
    
wallet = wallet.replace("window.location.href = '/simulate-wallet-success/' + data.order_id;", "window.location.href = '/payment-success/' + data.order_id;")

with open('d:/project_vps/templates/wallet.html', 'w', encoding='utf-8') as f:
    f.write(wallet)
    
# Update ip-checkout.html
with open('d:/project_vps/templates/ip-checkout.html', 'r', encoding='utf-8') as f:
    ip_chk = f.read()
    
ip_chk = ip_chk.replace("window.location.href = '/simulate-ip-success/{{ ip_id }}';", "window.location.href = '/payment-success/' + data.order_id;")

with open('d:/project_vps/templates/ip-checkout.html', 'w', encoding='utf-8') as f:
    f.write(ip_chk)

