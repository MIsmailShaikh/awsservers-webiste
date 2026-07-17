import re

with open('d:/project_vps/app.py', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Add migration
migration = '''    try:
        from sqlalchemy import text
        db.session.execute(text('ALTER TABLE transaction ADD COLUMN description VARCHAR(255)'))
        db.session.commit()
    except Exception as e:
        db.session.rollback()'''

content = re.sub(r'(db\.session\.rollback\(\))', r'\1\n\n' + migration, content, count=1)

# 2. Update create-order (VPS)
content = content.replace("order_id=razorpay_order['id'],\n            amount=amount_inr,\n            status='PENDING'",
"order_id=razorpay_order['id'],\n            amount=amount_inr,\n            status='PENDING',\n            description='Cloud Infrastructure Services'")

# 3. Update create-ip-order
content = content.replace("order_id=razorpay_order['id'],\n            amount=amount_inr,\n            status='PENDING'\n        )",
"order_id=razorpay_order['id'],\n            amount=amount_inr,\n            status='PENDING',\n            description=f'Static IP: {ip_id}'\n        )")

# 4. Update create-wallet-order
content = content.replace("order_id=razorpay_order['id'],\n            amount=amount,\n            status='PENDING'\n        )",
"order_id=razorpay_order['id'],\n            amount=amount,\n            status='PENDING',\n            description='Wallet Topup'\n        )")

with open('d:/project_vps/app.py', 'w', encoding='utf-8') as f:
    f.write(content)
